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

def searchTerm(text):
    os.system(f'start chrome "https://www.mazii.net/search?dict=javi&type=w&query={text}&hl=vi-VN"')

def add_to_context(page, menu):
    text = selectedText(page)
    if text:
        text = re.sub(r'\[[^\]]+?\]', '', text)
        text = text.strip()
    a = menu.addAction(f"Search Term '{text}'")
    a.triggered.connect(lambda _, text=text: searchTerm(text))
      
## Equal Expression to add Hook
# addHook("EditorWebView.contextMenuEvent", add_to_context)
gui_hooks.editor_will_show_context_menu.append(add_to_context)
# addHook("AnkiWebView.contextMenuEvent", add_to_context)
gui_hooks.webview_will_show_context_menu.append(add_to_context)