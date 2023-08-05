from pathlib import Path

basename = "test_all_items_role"
html_filename = basename + ".html"

def test_base_name_in_html(app):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert basename in html


def test_all_items_html_contains_value(app):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert "The answer to life, the Universe and everything is six times seven." in html
