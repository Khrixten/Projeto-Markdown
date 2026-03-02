from typing_extensions import override
from markdown_backend import MarkdownBackend


class LatexBackend(MarkdownBackend):
    def __init__(self, out):
        self._out = out
        self._inside_par = False
        self._first_par_line = True
    #:

    def close(self):
        pass
    #:

    @override
    def open_document(self, title=''):
        self._out.write("\\documentclass{article}\n")
        self._out.write("\\usepackage[utf8]{inputenc}\n")
        if title:
            self._out.write(f"\\title{{{title}}}\n")
        self._out.write("\\begin{document}\n")
        if title:
            self._out.write("\\maketitle\n\n")
    #:

    @override
    def close_document(self):
        self._out.write("\n\\end{document}\n")
    #:

    _HEADING_MAP = {1: 'section', 2: 'subsection', 3: 'subsubsection'}

    @override
    def open_heading(self, level: int):
        cmd = self._HEADING_MAP.get(level, 'paragraph')
        self._out.write(f"\\{cmd}{{")
    #:

    @override
    def close_heading(self, level: int):
        self._out.write("}\n")
    #:

    @override
    def new_text_line(self, line: str):
        self._out.write(line)
    #:

    @override
    def open_par(self):
        self._inside_par = True
        self._first_par_line = True
    #:

    @override
    def close_par(self):
        self._out.write("\n\n")
        self._inside_par = False
    #:

    @override
    def new_par_line(self, line: str):
        if self._inside_par and not self._first_par_line:
            self._out.write('\n')
        self._first_par_line = False
        self._out.write(line)
    #:

    @override
    def open_list(self):
        self._out.write("\\begin{itemize}\n")
        self._inside_par = False
        self._first_par_line = True
    #:

    @override
    def close_list(self):
        self._out.write("\\end{itemize}\n")
    #:

    @override
    def open_ordered_list(self):
        self._out.write("\\begin{enumerate}\n")
        self._inside_par = False
        self._first_par_line = True
    #:

    @override
    def close_ordered_list(self):
        self._out.write("\\end{enumerate}\n")
    #:

    @override
    def open_list_item(self):
        self._out.write("  \\item ")
        self._inside_par = False
        self._first_par_line = True
    #:

    @override
    def close_list_item(self):
        self._out.write("\n")
    #:

    @override
    def process_inline(self, text: str) -> str:
        return text
    #:
