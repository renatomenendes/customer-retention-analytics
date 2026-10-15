"""Guard public research documents against obsolete editorial stage directions."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]

STAGE_MARKERS = (
    "objetivo do case.docx",
    "ciclo de desenvolvimento do repositório",
    "itens disfarçados de análise concluída",
    "versão inicial",
    "repositório privado",
    "primeiro ciclo de modelagem",
    "análise anterior",
    "nenhum push ou criação automatizada",
    "apresentação atual preliminar",
    "não inventar valores",
)


def test_public_scientific_documents_avoid_editorial_stage_language():
    for document in DOCS:
        body = document.read_text(encoding="utf-8").casefold()
        for phrase in STAGE_MARKERS:
            assert phrase not in body, f"{document.relative_to(ROOT)}: {phrase}"


def test_research_report_ends_with_conclusions():
    report = (ROOT / "docs" / "study_report.md").read_text(encoding="utf-8")
    headings = [line for line in report.splitlines() if line.startswith("## ")]
    assert headings[-1] == "## 8. Conclusão e alcance dos resultados"


def test_readme_presents_only_public_facing_presentation_link():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    section = readme.split("## Apresentação executiva", 1)[1].split(
        "## Como consultar as evidências", 1
    )[0]
    assert "Apresentação — resultados e recomendações" in section
    assert "Roteiro para apresentação oral" not in section
