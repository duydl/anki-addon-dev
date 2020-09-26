import html
import os
import re
import anki
from aqt import mw
# from typing import Any, List, Optional, Tuple
from aqt.utils import showInfo # import the "show info" tool from utils.py
from aqt.qt import * # import all of the Qt GUI library
from aqt.utils import showInfo, shortcut
from anki.hooks import runHook, addHook
# from aqt.editor import Editor,EditorWebView
# from anki.utils import intTime, ids2str
# from anki.rsbackend import ExtractedLatex
# from anki.latex import svgCommands, _errMsg



anki.latex.build = False
def on_off():
    if anki.latex.build == False:
        anki.latex.build = True
    else:
        anki.latex.build = False


# create a new menu item, "test"
action = QAction("On - Off Latex", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(on_off)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


def onSetupMenus(browser):
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('On - Off Latex')
    a.setCheckable(True)
    a.setChecked(anki.latex.build)
    a.triggered.connect(on_off)

addHook("browser.setupMenus", onSetupMenus)














# def _save_latex_image_mine(
#     col: anki.storage._Collection,
#     extracted: ExtractedLatex,
#     header: str,
#     footer: str,
#     svg: bool,
# ) -> Optional[str]:
#     # add header/footer
#     latex = header + "\n" + extracted.latex_body.replace(r"<br>","") + "\n" + footer
#     # it's only really secure if run in a jail, but these are the most common
#     tmplatex = latex.replace("\\includegraphics", "")
#     for bad in (
#         "\\write18",
#         "\\readline",
#         "\\input",
#         "\\include",
#         "\\catcode",
#         "\\openout",
#         "\\write",
#         "\\loop",
#         "\\def",
#         "\\shipout",
#     ):
#         # don't mind if the sequence is only part of a command
#         bad_re = "\\" + bad + "[^a-zA-Z]"
#         if re.search(bad_re, tmplatex):
#             return (
#                 _(
#                     """\
# For security reasons, '%s' is not allowed on cards. You can still use \
# it by placing the command in a different package, and importing that \
# package in the LaTeX header instead."""
#                 )
#                 % bad
#             )

#     # commands to use
#     if svg:
#         latexCmds = svgCommands
#         ext = "svg"
#     else:
#         latexCmds = pngCommands
#         ext = "png"

#     # write into a temp file
#     log = open(namedtmp("latex_log.txt"), "w")
#     texpath = namedtmp("tmp.tex")
#     texfile = open(texpath, "w", encoding="utf8")
#     texfile.write(latex)
#     texfile.close()
#     oldcwd = os.getcwd()
#     png_or_svg = namedtmp("tmp.%s" % ext)
#     try:
#         # generate png/svg
#         os.chdir(tmpdir())
#         for latexCmd in latexCmds:
#             if call(latexCmd, stdout=log, stderr=log):
#                 return _errMsg(latexCmd[0], texpath)
#         # add to media
#         data = open(png_or_svg, "rb").read()
#         col.media.write_data(extracted.filename, data)
#         os.unlink(png_or_svg)
#         return None
#     finally:
#         os.chdir(oldcwd)
#         log.close()




# _save_latex_image_origin = anki.latex._save_latex_image
# anki.latex._save_latex_image = _save_latex_image_mine
# def on_off():
#     if anki.latex._save_latex_image != _save_latex_image_mine:
#         anki.latex._save_latex_image = _save_latex_image_mine
#     else:
#         anki.latex._save_latex_image = _save_latex_image_origin


# # from anki.rsbackend import ExtractedLatex

# # ExtractedLatex.latex_body = ExtractedLatex.latex_body.replace(r"<br>","")

# # create a new menu item, "test"
# action = QAction("Remove <br> - Default On", mw)
# # set it to call testFunction when it's clicked
# action.triggered.connect(on_off)
# # and add it to the tools menu
# mw.form.menuTools.addAction(action)