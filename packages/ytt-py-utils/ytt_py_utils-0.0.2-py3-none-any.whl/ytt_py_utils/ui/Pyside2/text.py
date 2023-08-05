"""
Text
"""
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QTextEdit



class TextEditAbstract(QTextEdit):
    """
    TextEditAbstract
    """
    def __init__(self):
        """

        """
        super(TextEditAbstract).__init__()
        self.text_color = QColor('grey')
        self.setTextColor(self.text_color)

    def set_text(self, text):
        """

        :param text:
        :return:
        """
        raise NotImplementedError


class DocTextEdit(TextEditAbstract):
    """
    DocTextEdit
    """
    def __init__(self):
        """

        """
        super(DocTextEdit).__init__()

    def set_text(self, text):
        """

        :param text:
        :return:
        """
        self.setText(text)


class HighlighterTextEdit(TextEditAbstract):
    """
    SourceTextEdit
    """
    def __init__(self):
        """

        """
        super(SourceTextEdit).__init__()

        # Set highlighter
        self.highlighter = misc_widgets_cls.Highlighter(self.document())

    def set_text(self, text):
        """

        :param text:
        :return:
        """
        self.setPlainText(text)
