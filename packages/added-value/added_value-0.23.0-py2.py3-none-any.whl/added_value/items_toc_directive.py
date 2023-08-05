from collections.abc import Mapping

from sphinx.directives.other import TocTree, glob_re
from sphinx.util import url_re, docname_join
from sphinx.util.matching import Matcher, patfilter

from added_value.importer import import_object
from added_value.non_string_iterable import NonStringIterable


class ItemsTableOfContentsDirective(TocTree):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def parse_content(self, toctree):
        # We override parse_content to retrieve information about the linked pages
        # from the argument object, rather than from the content of the directive.

        obj_name = self.arguments[0]

        obj, prefixed_name = import_object(obj_name, context=self)

        if isinstance(obj, Mapping):
            # Explicit mapping of titles to document links ("Some Title <document>")
            ret = self.parse_mapping(obj, toctree)
        elif isinstance(obj, NonStringIterable):
            # Series of document links. Titles extracted from documents
            ret = self.parse_iterable(obj, toctree)
        else:
            raise self.error("Cannot make a list from object {!r}".format(obj))

        # entries contains all entries (self references, external links etc.)
        if 'reversed' in self.options:
            toctree['entries'] = list(reversed(toctree['entries']))

        return ret

    def parse_mapping(self, titled_references, toctree):
        """Build a TOC from a mapping of titles to document references.

        Args:
            titled_references: A mapping of titles to document names or URLs
            toctree: The toctree node.
        """
        all_docnames = self.env.found_docs.copy()
        all_docnames.remove(self.env.docname)  # remove current document

        warnings = []
        for title, ref in titled_references.items():
            self.make_entry(
                title=title,
                ref=ref,
                toctree=toctree,
                all_docnames=all_docnames,
                warnings=warnings
        )
        return warnings

    def parse_iterable(self, references, toctree):
        """Build a TOC from a series of document links.

        Args:
            references: An iterable series of document links
            toctree: The toctree node.
        """

        # glob target documents
        all_docnames = self.env.found_docs.copy()
        all_docnames.remove(self.env.docname)  # remove current document

        warnings = []

        for ref in references:
            if not ref:
                continue
            if toctree['glob'] and glob_re.match(ref) and not url_re.match(ref):
                patname = docname_join(self.env.docname, ref)
                docnames = sorted(patfilter(all_docnames, patname))
                for docname in docnames:
                    all_docnames.remove(docname)  # don't include it again
                    toctree['entries'].append((None, docname))
                    toctree['includefiles'].append(docname)
                if not docnames:
                    warnings.append(self.state.document.reporter.warning(
                        'toctree glob pattern %r didn\'t match any documents'
                        % ref, line=self.lineno))
            else:
                self.make_entry(title=None, ref=ref, toctree=toctree, all_docnames=all_docnames, warnings=warnings)
        return warnings

    def make_entry(self, title, ref, toctree, all_docnames, warnings):
        """Make a single toctree entry.

        Args:
            title: The optional title of the entry to be displayed. If None, the
                title will be extracted from the referred document

            ref: A reference to the linked document; a filename or URL

            toctree: The toctree to which the entry will be added

            all_docnames: A sequence of all docnames excluding the document containing
                this directive.

            warnings: A sequence of warnings to which additional warnings may be appended
        """
        docname = ref
        suffixes = self.config.source_suffix
        excluded = Matcher(self.config.exclude_patterns)
        # remove suffixes (backwards compatibility)
        for suffix in suffixes:
            if docname.endswith(suffix):
                docname = docname[:-len(suffix)]
                break
        # absolutize filenames
        docname = docname_join(self.env.docname, docname)
        if url_re.match(ref) or ref == 'self':
            toctree['entries'].append((title, ref))
        elif docname not in self.env.found_docs:
            if excluded(self.env.doc2path(docname, None)):
                message = 'toctree contains reference to excluded document %r'
            else:
                message = 'toctree contains reference to nonexisting document %r'

            warnings.append(self.state.document.reporter.warning(message % docname,
                                                                 line=self.lineno))
            self.env.note_reread()
        else:
            all_docnames.discard(docname)
            toctree['entries'].append((title, docname))
            toctree['includefiles'].append(docname)