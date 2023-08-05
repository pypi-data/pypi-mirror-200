import logging

from docutils import nodes
from docutils.parsers.rst.directives import unchanged, flag, unchanged_required, class_option
from sphinx.directives.code import dedent_lines, container_wrapper
from sphinx.util import parselinenos
from sphinx.util.docutils import SphinxDirective
from sphinx.util.nodes import set_source_info
from sphinx.locale import __

from added_value.common_options import CLASS_OPTION, NAME_OPTION
from added_value.importer import import_object

logger = logging.getLogger(__name__)

CAPTION_OPTION = 'caption'
EMPHASIZE_LINES_OPTION = 'emphasize-lines'
LINENOS_START_OPTION = 'lineno-start'
DEDENT_OPTION = 'dedent'
LINENOS_OPTION = 'linenos'
LANGUAGE_OPTION = 'language'


class LiteralBlockDirective(SphinxDirective):

    has_content = False
    required_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        LINENOS_OPTION: flag,
        DEDENT_OPTION: int,
        LINENOS_START_OPTION: int,
        EMPHASIZE_LINES_OPTION: unchanged_required,
        CAPTION_OPTION: unchanged_required,
        CLASS_OPTION: class_option,
        NAME_OPTION: unchanged,
        LANGUAGE_OPTION: unchanged_required
    }

    def run(self):
        obj_name = self.arguments[0]

        obj, prefixed_name = import_object(obj_name, context=self)

        document = self.state.document
        code = str(obj)
        location = self.state_machine.get_source_and_line(self.lineno)

        linespec = self.options.get('emphasize-lines')
        if linespec:
            try:
                nlines = len(self.content)
                hl_lines = parselinenos(linespec, nlines)
                if any(i >= nlines for i in hl_lines):
                    logger.warning(__('line number spec is out of range(1-%d): %r') %
                                   (nlines, self.options['emphasize-lines']),
                                   location=location)

                hl_lines = [x + 1 for x in hl_lines if x < nlines]
            except ValueError as err:
                return [document.reporter.warning(str(err), line=self.lineno)]
        else:
            hl_lines = None

        if 'dedent' in self.options:
            location = self.state_machine.get_source_and_line(self.lineno)
            lines = code.split('\n')
            lines = dedent_lines(lines, self.options['dedent'], location=location)
            code = '\n'.join(lines)

        literal = nodes.literal_block(code, code)
        literal['language'] = self.options[LANGUAGE_OPTION]
        literal['linenos'] = 'linenos' in self.options or \
                             'lineno-start' in self.options
        literal['classes'] += self.options.get('class', [])
        extra_args = literal['highlight_args'] = {}
        if hl_lines is not None:
            extra_args['hl_lines'] = hl_lines
        if 'lineno-start' in self.options:
            extra_args['linenostart'] = self.options['lineno-start']
        set_source_info(self, literal)

        caption = self.options.get('caption')
        if caption:
            try:
                literal = container_wrapper(self, literal, caption)
            except ValueError as exc:
                return [document.reporter.warning(str(exc), line=self.lineno)]

        # literal will be note_implicit_target that is linked from caption and numref.
        # when options['name'] is provided, it should be primary ID.
        self.add_name(literal)

        return [literal]