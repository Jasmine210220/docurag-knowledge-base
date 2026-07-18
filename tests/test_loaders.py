from pathlib import Path

import pytest

from docurag.loaders.factory import get_loader
from docurag.loaders.file_loaders import (
    CsvDocumentLoader,
    JsonDocumentLoader,
    PdfDocumentLoader,
    TextDocumentLoader,
)


@pytest.mark.parametrize(
    ("file_name", "expected_loader"),
    [
        ("sample.txt", TextDocumentLoader),
        ("sample.md", TextDocumentLoader),
        ("sample.json", JsonDocumentLoader),
        ("sample.csv", CsvDocumentLoader),
        ("sample.pdf", PdfDocumentLoader),
    ],
)
def test_get_loader_dispatches_by_suffix(file_name: str, expected_loader: type) -> None:
    loader = get_loader(Path(file_name))
    assert isinstance(loader, expected_loader)


def test_get_loader_rejects_unsupported_suffix() -> None:
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_loader(Path("sample.unsupported"))
