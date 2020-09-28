import anki
from aqt import mw
from aqt.qt import *
from anki.sched import *

old_fillRev = anki.sched.Scheduler._fillRev
is_old_fillRev = True

def new_fillRev(self, recursing=False) -> bool:
    "True if a review card can be fetched."
    if self._revQueue:
        return True
    if not self.revCount:
        return False
    while self._revDids:
        did = self._revDids[0]
        lim = min(self.queueLimit, self._deckRevLimit(did))
        if lim:
            # fill the queue with the current did
            self._revQueue = self.col.db.list(
                f"""
select id from cards where
did = ? and queue = {QUEUE_TYPE_REV} and due <= ? limit ?""",
                did,
                self.today,
                lim,)
            if self._revQueue:
                # ordering
                if self.col.decks.get(did)["dyn"]:
                    # dynamic decks need due order preserved
                    self._revQueue.reverse()
                else:
                    # random order for regular reviews
                    # r = random.Random()
                    # r.seed(self.today)
                    # r.shuffle(self._revQueue)
                    self._revQueue.sort(reverse=True)
                    print(self._revQueue)
                # is the current did empty?
                if len(self._revQueue) < lim:
                    self._revDids.pop(0)
                return True
        # nothing left in the deck; move to next
        self._revDids.pop(0)

    # if we didn't get a card but the count is non-zero,
    # we need to check again for any cards that were
    # removed from the queue but not buried
    if recursing:
        print("bug: fillRev()")
        return False
    self._resetRev()
    return self._fillRev(recursing=True)


def created_order_on_off():
    if is_old_fillRev == True:
        anki.sched.Scheduler._fillRev = new_fillRev
        is_old_fillRev == False
    else:
        anki.sched.Scheduler._fillRev = old_fillRev
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
