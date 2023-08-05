from pathlib import Path

basename = "test_literal_repr_role"
html_filename = basename + ".html"


def test_base_name_in_html(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert basename in html


def test_literal_repr_html_contains_value(app, status, warning):
    app.build()
    html = Path(app.outdir / html_filename).read_text()
    assert '<p>The <code class="docutils literal notranslate"><span class="pre">\'JSR\'</span></code> opcode perform Jump to Sub-Routine.</p>' in html
