from pathlib import Path

basename = "test_str_role_with_callable"
html_filename = basename + ".html"


def test_base_name_in_html(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert basename in html


def test_str_literal_integer_from_method_html_contains_value(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert "The method call returns 978." in html
