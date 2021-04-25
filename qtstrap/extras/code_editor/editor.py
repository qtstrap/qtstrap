from qtstrap import *
from .highlighters import PythonHighlighter


class CodeEditor(QTextEdit):
    def __init__(self, *args, highlighter=PythonHighlighter, **kwargs):
        super().__init__(*args, **kwargs)
        
        set_font_options(self, {
            'setFamily': 'Courier',
            'setStyleHint': QFont.Monospace,
            'setFixedPitch': True,
        })

        # font = QFont();
        # font.setFamily("Courier");
        # font.setStyleHint(QFont.Monospace);
        # font.setFixedPitch(True);
        # self.setFont(font)
        
        self.setTabStopWidth(QFontMetricsF(self.font()).width(' ') * 4)
        self.syntax = highlighter(self)