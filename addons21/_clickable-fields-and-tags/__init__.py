# Copyright 2013 Abdolmahdi Saravi <amsaravi@yahoo.com>
# Copyright 2020 Damien Elmes <https://apps.ankiweb.net/>
# Copyright 2019-2020 Joseph Lorimer <joseph@lorimer.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from anki import hooks
from anki.template import TemplateRenderContext
from aqt import dialogs, gui_hooks, mw
from aqt.browser import PreviewDialog
from aqt.clayout import CardLayout
from aqt.qt import Qt
from aqt.reviewer import Reviewer
from aqt.utils import tooltip

# conf = mw.addonManager.getConfig(__name__)
# CSS = str(conf['CSS'])
# JS = str(conf['JS'])

CSS = """
<style>
  .xbutton {
  font-size: 1.25vw !important;
  border: 0px solid gray;
  background-color: white;
  color: black;
  padding: 0.25vw ;
  }
</style>

"""
# <style>
#   kbd {
#     box-shadow: inset 0 1px 0 0 white;
#     background:
#       gradient(
#         linear,
#         left top,
#         left bottom,
#         color-stop(0.05, #f9f9f9),
#         color-stop(1, #e9e9e9)
#       );
#     background-color: #f9f9f9;
#     border-radius: 4px;
#     border: 1px solid gainsboro;
#     display: inline-block;
#     font-size: 15px;
#     height: 15px;
#     line-height: 15px;
#     padding: 4px 4px;
#     margin: 5px;
#     text-align: center;
#     text-shadow: 1px 1px 0 white;
#     cursor: pointer;
#     cursor: hand;
#   }
#   .nightMode kbd {
#     color: black;
#   }
# </style>

# kbd {
# font-family: serif;
# text-align: left;
# color: black;
# padding: 0 ;
# }
# 

JS = """
<script type="text/javascript"> 
function ct_click(fieldname, fieldcontent) { 
    pycmd("ct_click_" + fieldname +"|" + fieldcontent)}
</script>
"""


def handle_click(handled, msg, context):
    if isinstance(context, CardLayout) and (
        msg.startswith('ct_click_') or msg.startswith('ct_dblclick_')
    ):
        tooltip("Can't be used in card layout screen.")
        return handled

    if not isinstance(context, Reviewer) and not isinstance(
        context, PreviewDialog
    ):
        return handled

    if msg.startswith('ct_click_'):
        fieldcontent, fieldname = msg.replace('ct_click_', '').split('|')
        browser = dialogs.open('Browser', mw)
        browser.setFilter('"{0}:{1}"'.format(fieldname, fieldcontent))
        return True, None
    # elif msg.startswith('ct_dblclick_'):
    #     tag, deck = msg.replace('ct_dblclick_', '').split('|')
    #     browser = dialogs.open('Browser', mw)
    #     browser.setFilter('"tag:%s" "deck:%s"' % (tag, deck))
    #     browser.setWindowState(
    #         browser.windowState() & ~Qt.WindowMinimized | Qt.WindowActive
    #     )
    #     return True, None
    return handled


def append_to_card(output, context):
    output.question_text += CSS + JS
    output.answer_text += CSS + JS


def on_field_filter(text, field, filter, context: TemplateRenderContext):
    if filter != 'clickable':
        return text
    # if field == "Tags":
    #     kbd = """
    #     <kbd onclick="ct_click('{fieldcontent}', '{fieldname}')">
    #     {fieldcontent}
    #     </kbd>
    #     """
    #     return ''.join(
    #     [
    #         kbd.format(fieldname = field[:-1], fieldcontent=fieldcontent)
    #         for fieldcontent in context.fields()['Tags'].split()
    #     ]
    # )
    kbd = """
<button class="xbutton" onclick="ct_click('{fieldcontent}', '{fieldname}')"><span id = "button-{fieldname}">※</span></button>{fieldcontent}  
"""
    
    return kbd.format(fieldname = field ,fieldcontent=context.fields()[field])
          
        


gui_hooks.webview_did_receive_js_message.append(handle_click)
hooks.card_did_render.append(append_to_card)
hooks.field_filter.append(on_field_filter)
