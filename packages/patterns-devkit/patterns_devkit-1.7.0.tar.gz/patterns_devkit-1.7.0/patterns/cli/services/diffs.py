import difflib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Dict
from zipfile import ZipFile

from rich.markdown import Markdown

from patterns.cli.helpers import directory_contents_to_upload
from patterns.cli.services.output import sprint


@dataclass
class DiffResult:
    added: List[str]
    removed: List[str]
    changed: Dict[str, Iterator[str]]

    @property
    def is_not_empty(self) -> bool:
        return bool(self.added or self.removed or self.changed)

    @property
    def is_empty(self) -> bool:
        return not self.is_not_empty


def get_diffs_between_zip_and_dir(
    zf: ZipFile, root: Path, from_remote: bool
) -> DiffResult:
    """Return a map of {filename: diff} where the contents differ between zf and root"""
    result = DiffResult([], [], {})
    all_in_zip = set()
    for zipinfo in zf.infolist():
        dst = root / zipinfo.filename
        if zipinfo.is_dir():
            continue
        all_in_zip.add(zipinfo.filename)
        if not dst.is_file():
            (result.added if from_remote else result.removed).append(zipinfo.filename)
            continue
        zip_bytes = zf.read(zipinfo)
        try:
            zip_content = zip_bytes.decode().splitlines(keepends=False)
            fs_content = dst.read_text().splitlines(keepends=False)
        except UnicodeDecodeError:
            if zip_bytes != dst.read_bytes():
                result.changed[zipinfo.filename] = [
                    f"--- <remote> {zipinfo.filename}",
                    f"+++ <local>  {zipinfo.filename}",
                    "Binary contents differ",
                ]
        else:
            if zip_content != fs_content:
                if from_remote:
                    zip_content, fs_content = fs_content, zip_content
                diff = difflib.unified_diff(
                    zip_content,
                    fs_content,
                    fromfile=f"<remote> {zipinfo.filename}",
                    tofile=f"<local>  {zipinfo.filename}",
                    lineterm="",
                )
                result.changed[zipinfo.filename] = diff
    for path in directory_contents_to_upload(root):
        file_name = path.relative_to(root).as_posix()
        if file_name not in all_in_zip:
            (result.removed if from_remote else result.added).append(file_name)

    return result


def print_diffs(diffs: DiffResult, context: bool, full: bool):
    if full:
        if diffs.added:
            sprint("Added:")
            sprint(Markdown("\n".join(f"- {a}" for a in diffs.added), style="success"))
            print()
        if diffs.removed:
            sprint("Deleted:")
            sprint(Markdown("\n".join(f"- {a}" for a in diffs.removed), style="error"))
            print()
    if not diffs.changed:
        return
    sprint("Modified:")
    if not context:
        sprint(Markdown("\n".join(f"- {a}" for a in diffs.changed), style="info"))
        return

    print()
    diff = "\n\n".join("\n".join(d) for d in diffs.changed.values())
    sprint(
        Markdown(
            f"""
```diff
{diff}
```
""",
            code_theme="vim",
        )
    )
