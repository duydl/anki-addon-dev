# import necessary module
# Loop through all decks, get deck with certain name, set the value of that 
# with the preset value depend on the day
# 

def loadConf(self):
        self.conf = self.mw.col.decks.confForDid(self.deck["id"])
        # new
        c = self.conf["new"]
        f = self.form
        f.lrnSteps.setText(self.listToUser(c["delays"]))
        f.lrnGradInt.setValue(c["ints"][0])
        f.lrnEasyInt.setValue(c["ints"][1])
        f.lrnFactor.setValue(c["initialFactor"] / 10.0)
        f.newOrder.setCurrentIndex(c["order"])
        f.newPerDay.setValue(c["perDay"])
        f.bury.setChecked(c.get("bury", True))
        f.newplim.setText(self.parentLimText("new"))
        # rev
        c = self.conf["rev"]
        f.revPerDay.setValue(c["perDay"])
        f.easyBonus.setValue(c["ease4"] * 100)
        f.fi1.setValue(c["ivlFct"] * 100)
        f.maxIvl.setValue(c["maxIvl"])
        f.revplim.setText(self.parentLimText("rev"))
        f.buryRev.setChecked(c.get("bury", True))
        f.hardFactor.setValue(int(c.get("hardFactor", 1.2) * 100))
        if self.mw.col.schedVer() == 1:
            f.hardFactor.setVisible(False)
            f.hardFactorLabel.setVisible(False)






            self.setWindowTitle(_("Options for %s") % self.deck["name"])
        restoreGeom(self, "dyndeckconf")
        self.initialSetup()