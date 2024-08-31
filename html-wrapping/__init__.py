# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
# import all of the Qt GUI library
from aqt.qt import *
from aqt.utils import showInfo, shortcut
from anki.hooks import addHook
from aqt.editor import Editor,EditorWebView
from anki.hooks import runHook,addHook
import bs4
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def wrapspan(editor):
    editor.web.eval("wrap('<span style=\"color: blue;\" class=\"headword-example\">', '</span>');")
# def unwrapspan(editor):
#     soup1 = bs4.BeautifulSoup(htm1, 'html.parser')
#     for match in soup1.findAll('span'):
#         match.unwrap()

def addMyButton(buttons, editor):
    editor._links['strike'] = wrapspan

    return buttons + [editor._addButton(
        "1824986.png", # "/full/path/to/icon.png",
        "strike", # link name
        "Ctrl+Shift+Alt+Q")]
def cs_editor_setupShortcuts(self):
    # if a third element is provided, enable shortcut even when no field selected
    cuts = [
            ("Ctrl+L", self.onCardLayout, True),
            ("Ctrl+B", self.toggleBold),
            ("Ctrl+I", self.toggleItalic),
            ("Ctrl+U", self.toggleUnderline),
            ("Ctrl++", self.toggleSuper),
            ("Ctrl+=", self.toggleSub),
            ("Ctrl+R", self.removeFormat),
            ("F7", self.onForeground),
            ("F8", self.onChangeCol),
            ("Ctrl+Shift+C", self.onCloze),
            ("Ctrl+Shift+Alt+C", self.onCloze),
            ("F3", self.onAddMedia),
            ("F5", self.onRecSound),
            ("Ctrl+T, T", self.insertLatex),
            ("Ctrl+T, E", self.insertLatexEqn),
            ("Ctrl+T, M", self.insertLatexMathEnv),
            ("Ctrl+M, M", self.insertMathjaxInline),
            ("Ctrl+M, E", self.insertMathjaxBlock),
            ("Ctrl+M, C", self.insertMathjaxChemistry),
            ("Ctrl+Shift+X", self.onHtmlEdit),
            ("Ctrl+Shift+T", self.onFocusTags, True)
    ]
    cuts.append(("Ctrl+Shift+Alt+Q", lambda: self.web.eval("wrap('<span style=\"color: blue;\" class=\"headword-example\">', '</span>');")))
    runHook("setupEditorShortcuts", cuts, self)
    for row in cuts:
        if len(row) == 2:
            keys, fn = row
            fn = self._addFocusCheck(fn)
        else:
            keys, fn, _ = row
        QShortcut(QKeySequence(keys), self.widget, activated=fn)

    
addHook("setupEditorButtons", addMyButton)
Editor.setupShortcuts = cs_editor_setupShortcuts
