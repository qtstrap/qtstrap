from qtstrap import *


class LinkLabel(QLabel):
    def __init__(self, text='', link='', both=None, parent=None):
        super().__init__(parent=parent)

        if both:
            self._text = both
            self._link = both
        else:
            self._text = text
            self._link = link

        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)

        self._update_text()

    def setText(self, text):
        self._text = text
        self._update_text()

    def setLink(self, link):
        self._link = link
        self._update_text()

    def _update_text(self):
        super().setText(f'<a href="{self._text}">{self._link}</a>')