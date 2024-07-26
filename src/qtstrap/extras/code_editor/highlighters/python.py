from qtstrap import *


def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _format = QTextCharFormat()
    _format.setForeground(QColor(color))
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# modeled off the default VSCode themes
STYLES = {
    'light': {
        'keyword': format('#0000FF'),
        'control_flow': format('#AF00DB'),
        'function_call': format('#795E26'),
        'brace': format('black'),
        'type': format('#267F99'),
        'string': format('#A31515'),
        'comment': format('#008000'),
        'numbers': format('#098658'),
    },
    'dark': {
        'keyword': format('#569cd6'),
        'control_flow': format('#C586C0'),
        'function_call': format('#DCDCAA'),
        'brace': format('#d4d4d4'),
        'type': format('#4EC9B0'),
        'string': format('#ce9178'),
        'comment': format('#6A9955'),
        'numbers': format('#b5cea8'),
    },
}


def get_style(kind):
    return STYLES[OPTIONS.theme][kind]


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for the Python language."""

    # Python keywords
    keywords = [
        'and',
        'class',
        'def',
        'global',
        'in',
        'is',
        'lambda',
        'not',
        'or',
        'self',
        'None',
        'True',
        'False',
    ]

    control_flow = [
        'assert',
        'break',
        'continue',
        'del',
        'elif',
        'else',
        'except',
        'finally',
        'for',
        'from',
        'if',
        'import',
        'pass',
        'raise',
        'return',
        'try',
        'while',
        'yield',
    ]

    # Python braces
    braces = [
        '\{',
        '\}',
        '\(',
        '\)',
        '\[',
        '\]',
    ]

    def __init__(self, document):
        super().__init__(document)
        self.build_rules()

        App().theme_changed.connect(self._rehighlight)

    def _rehighlight(self):
        self.build_rules()
        self.rehighlight()

    def build_rules(self):
        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegularExpression("'''"), 1, get_style('string'))
        self.tri_double = (QRegularExpression('"""'), 2, get_style('string'))

        _rules = []

        def rule(pattern, index, style) -> None:
            _rules.append((QRegularExpression(pattern), index, get_style(style)))

        [rule(r'\b%s\b' % w, 0, 'keyword') for w in self.keywords]
        [rule(r'\b%s\b' % w, 0, 'control_flow') for w in self.control_flow]
        # [rule(r'\b%s\b' % w, 0, 'function_call') for w in self.builtins]
        [rule(r'%s' % w, 0, 'brace') for w in self.braces]
        rule(r'\b\w+\s*(?:\()', 0, 'function_call')  # identifier followed by a (
        rule(r'\bclass\b\s*(\w+)', 1, 'type')  # 'class' followed by an identifier
        rule(r'"[^"\\]*(\\.[^"\\]*)*"', 0, 'string')  # Double-quoted string
        rule(r"'[^'\\]*(\\.[^'\\]*)*'", 0, 'string')  # Single-quoted string
        rule(r'#[^\n]*', 0, 'comment')  # From '#' until a newline
        # Numeric literals
        rule(r'\b[+-]?[0-9]+[lL]?\b', 0, 'numbers')
        rule(r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, 'numbers')
        rule(r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, 'numbers')

        # Build a QRegularExpression for each pattern
        self.rules = _rules

    def highlightBlock(self, text):
        """Apply syntax highlighting to the given block of text."""
        # Do other syntax formatting
        for regex, nth, fmt in self.rules:
            i = regex.globalMatch(text)
            while i.hasNext():
                match = i.next()
                if match.hasMatch():
                    start = match.capturedStart(nth)
                    length = match.capturedLength(nth)
                    self.setFormat(start, length, fmt)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(text, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``QRegularExpression`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            match = delimiter.match(text)
            start = match.capturedStart()
            add = match.capturedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            match = delimiter.match(text, start + add)
            end = match.capturedStart()
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + match.capturedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add
            # Apply formatting
            self.setFormat(start, length, style)
            # Look for the next match
            match = delimiter.match(text, start + length)
            start = match.capturedStart()

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
