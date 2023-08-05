import json
from pathlib import Path

from bs4 import BeautifulSoup

dir_name = Path("test_literal_block_directive")
html_filename = "test_json_literal.html"




def test_base_name_in_html(app, values):
    app.build()
    html_doc = Path(app.outdir / dir_name / html_filename).read_text()
    text = extract_pre_from_html(html_doc)
    d = json.loads(text)
    assert d == json.loads(values.json_month_lengths)


def extract_pre_from_html(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    pre = soup.find('pre')
    return pre.get_text()

