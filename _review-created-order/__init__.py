import anki
from aqt import mw
from aqt.qt import *
# from anki.sched import *
from anki.schedv2 import * 

old_fillRev = anki.schedv2.Scheduler._fillRev
is_old_fillRev = True


def  new_fillRev(self, recursing=False) -> bool:
        "True if a review card can be fetched."
        if self._revQueue:
            return True
        if not self.revCount:
            return False

        lim = min(self.queueLimit, self._currentRevLimit())
        if lim:
            self._revQueue = self.col.db.list(
                f"""
select id from cards where
did in %s and queue = {QUEUE_TYPE_REV} and due <= ?
order by nid
limit ?"""
# order by due, random()
                % self._deckLimit(),
                self.today,
                lim,
            )

            if self._revQueue:
                # preserve order
                self._revQueue.reverse()
                return True

        return False

def created_order_on_off():
    if is_old_fillRev == True:
        anki.schedv2.Scheduler._fillRev = new_fillRev
        is_old_fillRev == False
    else:
        anki.schedv2.Scheduler._fillRev = old_fillRev
        is_old_fillRev == True

created_order_on_off()
# create a new menu item, "test"
action = QAction("On - Off Review Created Order", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(created_order_on_off)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


# def onSetupMenus(browser):
#     menu = browser.form.menuEdit
#     menu.addSeparator()
#     a = menu.addAction('On - Off Review Created Order')
#     a.setCheckable(True)
#     a.setChecked(anki.latex.build)
#     a.triggered.connect(on_off)

# addHook("browser.setupMenus", onSetupMenus)
