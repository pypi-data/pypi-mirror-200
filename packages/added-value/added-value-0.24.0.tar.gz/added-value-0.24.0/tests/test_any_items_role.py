from pathlib import Path

basename = "test_any_items_role"
html_filename = basename + ".html"


def test_base_name_in_html(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert basename in html


def test_any_items_items_html_contains_value(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert "I would choose any of cherry, chocolate or pear." in html
