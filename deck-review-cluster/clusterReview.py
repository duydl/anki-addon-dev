from anki.find import Finder
from anki.hooks import addHook
from aqt import mw
from aqt.qt import QAction
from aqt.utils import getText, showWarning, tooltip
from anki.lang import _
import time



def RepresentsInt(s):
    try:
        return int(s)
    except ValueError:
        return None


def getDelay():
    return getUserInput()[0]


def getUserInput():
    (s, _) = getText("Clustering review base on field? (Default: Section")
    if s == "":
        return "Section"
    return s



def clusterCards(cids, minivl = 21):
    # print(cids)
    field = getUserInput()
    cingroup = {}


    mw.checkpoint("Clustering")
    mw.progress.start()

    for cid in cids:
        c = mw.col.getCard(cid)
        # c.due = 1: due in the past. Give the hell of confusing error. 
        if c.ivl == 0 or c.ivl < minivl or c.due <30:
            continue

        n = mw.col.getNote(c.nid)
        if n[field] not in cingroup:
            cingroup[n[field]] = []
        cingroup[n[field]].append(cid)
    
    # Divide cards into groups. Cluster Them.
    
    text = "========================\n"
    print(cingroup)
    for key in dict( sorted(cingroup.items()) ):
        newdue = 0

        for cid in cingroup[key]:
            card = mw.col.getCard(cid)
            # print (card)
            newdue += card.due
            # print(card.due)
        newdue = newdue // len(cingroup[key])
        # print("len:", len(cingroup[key]))
        # print("new", newdue)


        for cid in cingroup[key]:
            card = mw.col.getCard(cid)
            # card.ivl = card.ivl - card.due + newdue 
            print(card.due)
            card.due = newdue 
            print(card.due, card.ivl)
            card.flush()
        datedue = time.strftime(r"%Y-%m-%d", time.localtime(time.time() + (newdue-408) * 86400))
        text += f"{key}: {len(cingroup[key])} cards due {datedue} \n"

    # export out the schedule of differen section. maybe add them to description of deck. 
    text += "========================\n"

    mw.progress.finish()
    mw.col.reset()
    mw.reset()

    tooltip(_("""Clustering."""))
    return text

def changeDeckDesc(did, text):
    # f.desc.setPlainText(self.deck["desc"])
    # config = mw.col.decks.confForDid(did)
    # There is no deck.flush
    # deck.flush
    deck = mw.col.decks.get(did)
    newdesc = deck["desc"].split("========================\n")
    if len(newdesc) < 2:
        deck["desc"] += text
        mw.col.decks.update(deck)
    else: 
        newdesc[1] = text
        deck["desc"] = "\n".join(newdesc)
        mw.col.decks.update(deck)
    # print(text)
    # print(mw.col.decks.get(did))


def addActionToGear(fun, text):
    """fun -- takes an argument, the did
    text -- what's written in the gear."""
    def aux(m, did):
        a = m.addAction(text)
        a.triggered.connect(lambda b, did=did: fun(did))
    addHook("showDeckOptions", aux)


def cidsInDid(did):
    deck = mw.col.decks.get(did)
    deckName = deck['name']
    return mw.col.findCards(f"\"deck:{deckName}\"")


def clusterReviews(did):
    cids = cidsInDid(did)
    text = clusterCards(cids)
    changeDeckDesc(did, text)

addActionToGear(clusterReviews, _("Cluster Reviews"))

# def getReviewCards():
#     finder = Finder(mw.col)
#     cids = finder.findCards("is:review")
#     return cids