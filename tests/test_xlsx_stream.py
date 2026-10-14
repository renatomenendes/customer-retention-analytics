"""Synthetic XLSX fixture: no real data or customer identifiers."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from retention_analytics.xlsx_stream import iter_worksheet_rows


SHEET_XML = """<?xml version="1.0" encoding="UTF-8"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <sheetData>
    <row r="1"><c r="A1" t="s"><v>0</v></c>
    <c r="B1" t="s"><v>1</v></c>
    <c r="C1" t="s"><v>2</v></c></row>
    <row r="2"><c r="A2" t="s"><v>3</v></c>
    <c r="C2"><v>9</v></c></row>
  </sheetData>
</worksheet>"""

STRINGS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
<si><t>id_cliente</t></si><si><t>FLAG_ORIGEM</t></si>
<si><t>VALOR_BL_M0</t></si><si><t>example-synthetic</t></si>
</sst>"""


def test_stream_synthetic_sparse_worksheet(tmp_path: Path):
    filename = tmp_path / "fixture.xlsx"
    with ZipFile(filename, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("xl/worksheets/sheet1.xml", SHEET_XML)
        archive.writestr("xl/sharedStrings.xml", STRINGS_XML)

    rows = list(iter_worksheet_rows(filename))
    assert rows == [{
        "id_cliente": "example-synthetic",
        "FLAG_ORIGEM": None,
        "VALOR_BL_M0": "9",
    }]
