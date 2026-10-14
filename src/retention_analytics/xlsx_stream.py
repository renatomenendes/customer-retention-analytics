"""Read large XLSX worksheets incrementally without spreadsheet mutation.

The standard ZIP/XML representation is read-only. A worksheet's complete
sheetData is streamed, independently of any named range in the workbook.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from zipfile import ZipFile

from lxml import etree

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def excel_column_index(cell_ref: str) -> int:
    """Return the zero-based column index from an Excel address."""
    index = 0
    for char in cell_ref:
        if not char.isalpha():
            break
        index = index * 26 + ord(char.upper()) - ord("A") + 1
    return index - 1


def load_shared_strings(archive: ZipFile) -> list[str]:
    """Materialize the shared-string dictionary (not worksheet cells)."""
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    strings = []
    with archive.open("xl/sharedStrings.xml") as stream:
        for _, element in etree.iterparse(stream, events=("end",), tag=f"{NS}si"):
            strings.append("".join(element.itertext()))
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    return strings


def iter_worksheet_rows(path: str | Path) -> Iterator[dict[str, str | None]]:
    """Yield each data row by header name, preserving absent cells as None.

    Supports the first worksheet stored as ``xl/worksheets/sheet1.xml``.
    Validates header uniqueness rather than silently overwriting columns.
    """
    with ZipFile(path) as archive:
        shared = load_shared_strings(archive)
        headers: list[str] | None = None
        with archive.open("xl/worksheets/sheet1.xml") as stream:
            for _, element in etree.iterparse(
                stream, events=("end",), tag=f"{NS}row"
            ):
                cells: dict[int, str | None] = {}
                for cell in element:
                    if cell.tag != f"{NS}c":
                        continue
                    value_element = cell.find(f"{NS}v")
                    text: str | None = (
                        value_element.text if value_element is not None else None
                    )
                    if cell.get("t") == "s" and text is not None:
                        text = shared[int(text)]
                    elif cell.get("t") == "inlineStr":
                        inline = cell.find(f"{NS}is")
                        text = (
                            "".join(inline.itertext())
                            if inline is not None
                            else None
                        )
                    cells[excel_column_index(cell.get("r", "A1"))] = text
                if headers is None:
                    headers = [cells.get(i) or "" for i in range(max(cells) + 1)]
                    if any(not h for h in headers) or len(set(headers)) != len(headers):
                        raise ValueError("Missing or repeated column headers")
                else:
                    yield {name: cells.get(i) for i, name in enumerate(headers)}
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
