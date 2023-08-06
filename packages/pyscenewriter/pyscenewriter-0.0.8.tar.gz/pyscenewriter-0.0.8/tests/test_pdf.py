import pyscenewriter
from io import BytesIO
from pypdf import PdfReader
from textwrap import dedent


def test_fountain_to_pdf(fountain_sample):
    pdf_bytes = pyscenewriter.fountain_to_pdf(fountain_sample)
    reader = PdfReader(BytesIO(pdf_bytes), strict=True)
    assert len(reader.pages) == 1
    (page,) = reader.pages
    text = page.extract_text()
    expected_text = dedent(
        """
        DAVE
        Hi Philip
        PHILIP
        Hello David
        Dave and Philip stand in silence for three hours
    """
    ).strip()
    assert text == expected_text
