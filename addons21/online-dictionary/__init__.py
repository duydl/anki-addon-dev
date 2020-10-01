import os
import re
from anki.hooks import addHook
from aqt import mw, gui_hooks


def selectedText(page):    
    text = page.selectedText()
    if not text:
        return False
    else:
        return text


def searchTerm(page):
    text = selectedText(page)
    if text:
        text = re.sub(r'\[[^\]]+?\]', '', text)
        text = text.strip()
    print(r'start chrome https://www.mazii.net/search?dict=javi&type=w&query=' + text + r'&hl=vi-VN')
    os.system(r'start chrome https://www.mazii.net/search?dict=javi&type=w&query=' + text + r'&hl=vi-VN')


def add_to_context(view, menu):    
    a = menu.addAction("Search term")
    a.triggered.connect(lambda _, page=view: searchTerm(page))

addHook("EditorWebView.contextMenuEvent", add_to_context)


