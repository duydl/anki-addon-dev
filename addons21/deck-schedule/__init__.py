from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
import datetime

today = datetime.datetime.today().weekday()
user_config = mw.addonManager.getConfig(__name__)
def deckconfigsetup(deckbrowser):
    print(user_config)
    for name in user_config:
        day = user_config[name]
        for config in mw.col.decks.allConf():
            if name == config["name"]:
                if today in day:
                    config["rev"]["perDay"] = 1000
                    new_config = config
                    print(new_config)
                    mw.col.decks.setConf(new_config, config["id"])
                else:
                    config["rev"]["perDay"] = 0
                    new_config = config
                    print(new_config)
                    mw.col.decks.setConf(new_config, config["id"])

# gui_hooks.main_window_did_init.append(deckconfigsetup)
gui_hooks.deck_browser_did_render.append(deckconfigsetup)

