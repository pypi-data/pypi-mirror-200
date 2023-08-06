import pyscenewriter
import lxml.html


def test_fountain_to_html(fountain_sample):
    html = pyscenewriter.fountain_to_html(fountain_sample)
    root = lxml.html.document_fromstring(html)
    (body,) = root.getchildren()
    e1, e2, e3 = body.getchildren()
    assert e1.attrib["class"] == "element-dialogue"
    assert e1.text_content().strip() == "DAVE\nHi Philip"

    assert e2.attrib["class"] == "element-dialogue"
    assert e2.text_content().strip() == "PHILIP\nHello David"

    assert e3.attrib["class"] == "element-action"
    assert (
        e3.text_content().strip() == "Dave and Philip stand in silence for three hours"
    )
