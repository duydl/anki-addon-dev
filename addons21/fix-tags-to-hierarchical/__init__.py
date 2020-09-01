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
from anki.utils import intTime, ids2str
import sqlite3


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.


class TagEditWindow(QWidget):

    def renameTag(self):
    # get the number of cards in the current collection, which is stored in
    # the main window
        # show a message box
        # for cid in mw.col.findCards("Deck:"+self.deck_name.text()):
        #     card = mw.col.getCard(cid)
        deck_id = mw.col.decks.selected()
        deck_cids = mw.col.decks.cids(deck_id)
        str_cids = ids2str(deck_cids)

        for row in mw.col.db.execute(
            "SELECT tags, id FROM notes WHERE id in (SELECT nid FROM cards WHERE id in " + str_cids +")"):
            
            a = row[0].split(" ")[1:-1]
            for i in range(len(a)):
                a[i]=  self.lineEdit.text() + "::" + a[i]
            mw.col.db.execute('UPDATE notes SET tags= ? WHERE id = ? ', " "+" ".join(a)+" ", row[1])
        
        mw.requireReset()

    # main window of Quizlet plugin
    def __init__(self):
        super(TagEditWindow, self).__init__()

        self.results = None
        self.thread = None

        self.setupUi()

    # create GUI skeleton
    def setupUi(self):
        self.setObjectName("self")
        self.resize(400, 300)
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(120, 90, 111, 41))
        font = QFont()
        font.setPointSize(8)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.renameTag)

        self.label = QLabel(self)
        self.label.setGeometry(QRect(30, 20, 91, 41))
        font = QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(120, 20, 221, 41))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi()
        
        self.show()
    def retranslateUi(self):
        self.label.setText("Parent Tag")
        self.pushButton.setText("Change Tag")
    # def setupUi(self):
    #     self.setObjectName("self")
    #     self.resize(400, 300)
    #     self.textEdit = QLineEdit(self)
    #     self.textEdit.setGeometry(QRect(140, 30, 241, 31))
    #     self.textEdit.setObjectName("textEdit")

    #     self.textEdit_2 = QLineEdit(self)
    #     self.textEdit_2.setGeometry(QRect(140, 70, 241, 31))
    #     self.textEdit_2.setObjectName("textEdit_2")

    #     self.label = QLabel(self)
    #     self.label.setGeometry(QRect(30, 39, 81, 21))
    #     font = QFont()
    #     font.setPointSize(8)
    #     self.label.setFont(font)
    #     self.label.setObjectName("label")

    #     self.label_2 = QLabel(self)
    #     self.label_2.setGeometry(QRect(30, 70, 81, 41))
    #     font = QFont()
    #     font.setPointSize(8)
    #     self.label_2.setFont(font)
    #     self.label_2.setObjectName("label_2")

    #     self.pushButton = QPushButton(self)
    #     self.pushButton.setGeometry(QRect(120, 160, 111, 41))
    #     font = QFont()
    #     font.setPointSize(8)
    #     self.pushButton.setFont(font)
    #     self.pushButton.setObjectName("pushButton")
    #     self.pushButton.clicked.connect(self.testFunction)

    #     self.retranslateUi()
        
    #     self.show()
    # def retranslateUi(self):
    #     self.label.setText("Deck")
    #     self.label_2.setText("Parent Tag")
    #     self.pushButton.setText("Change Tag")

# plugin was called from Anki
def runPlugin():
    global __window
    __window = TagEditWindow()

# create a new menu item, "test"
action = QAction("Change Tag", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(runPlugin)
# and add it to the tools menu
mw.form.menuTools.addAction(action)


