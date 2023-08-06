from platform import system

from tools import iltools
from pypanelxsworker import serviceworker
from meditor import meditor

import os
import datetime

# In Honor Of prettyIL short life and inspiration for a bigger project.
class PyPanelX:
    def __init__(self):
        self.notSystemSet = True
        self.hostClearCW = None
        self.option = None
        self.system = system()
        self.targetUserName = str
        self.tools = iltools
        self.meditor = meditor
        self.serviceworker = serviceworker

    def clear(self):
        if self.notSystemSet == True:
            if self.system == "Windows":
                self.hostClearCW = "cls"
            elif self.system == "Linux":
                self.hostClearCW = "clear"
            elif self.system == "Darwin":
                self.hostClearCW = "clear"
            else:
                print("What the dog using?")
        os.system(f"{self.hostClearCW}")
        return 0

    def mainMenu(self):
        print("[PyPanelX CLI]")
        print()
        print(f"Today is {datetime.date.today()}, Local DB is up to date: Unknown")
        print()
        print("Options:")
        print()
        print("[1]. Single Mode")
        print("[2]. Database / Batch Mode")
        print("[3]. Just Update Data Base")
        print("[4]. MEditor and Flask Server")
        print()

    def singleModeMenu(self):
        username = input("Username used to download data: ")
        self.clear()
        print("[Single Mode Selected]")
        print()
        print(f"Username used: {username}")
        print()
        print("Options:")
        print()
        print("[1]. Database of a specific target")
        print("[2]. Stories")
        print("[3]. Highlights")
        print("[4]. Posts")
        print("[5]. Tagged")
        print("[6]. Reels (Not Implemented Yet)")
        print()

        self.option = int(input("Option: "))

        if self.option == 1:
            self.clear()
            targetUsername = input("Target Username: ")
            iltools.Tools(username, targetUsername).writeUserMD()
            pass
        elif self.option == 2:
            self.clear()
            targetUsername = str(input("Target Username: "))
            iltools.Tools(username, targetUsername).downloadStories()
            pass
        elif self.option == 3:
            self.clear()
            targetUsername = input("Target Username: ")
            iltools.Tools(username, targetUsername).downloadHighLights()
            pass
        elif self.option == 4:
            self.clear()
            targetUsername = input("Target Username: ")
            iltools.Tools(username, targetUsername).downloadPosts()
            pass
        elif self.option == 5:
            self.clear()
            # Option 5 logic
            pass
        elif self.option == 6:
            self.clear()
            # Option 6 logic
            pass
        else:
            print("Invalid option selected. Please try again.")

    def databaseBatchModeMenu(self):
        print("[Database Options:]")
        print()
        print("[1]. Database Update")
        print("[2]. Database Export")
        print("[3]. Database Import")
        print("[4]. Configure a new Database")
        print("[5]. Destroy Database (Not Implemented Yet)")
        print()
        self.option = int(input())

    def batchDownloadMenu(self):
        print("[Batch Download Selected]")
        print()
        print("[1]. Profiles")
        print("[2]. Logged user stories")
        print("[3]. Logger user saves")
        print("[4]. Logged user profile")
        print("[5]. Destroy Database (Not Implemented Yet)")

    def batchModePrints(self):
        print("[Batch Mode Selected]")
        print()
        print("Options:")
        print()
        print("[1]. Database")
        print("[2]. Batch Download")
        print()
        self.option = int(input())
        if self.option == 1:
            self.databaseBatchModeMenu()
        elif self.option == 2:
            self.batchDownloadMenu()
        else:
            print(f"Option {self.option} not recognized.")
        return 0

    def meditorExecute(self):
        pass
    
    def access(self):
        self.clear()
        self.mainMenu()
        self.option = int(input())
        if self.option == 1:
            self.clear()
            self.singleModeMenu()
        elif self.option == 2:
            self.clear()
            self.batchModePrints()
        elif self.option == 3:
            pass
        elif self.option == 4:
            self.meditor.main()
            self.serviceworker.app.run()
        else:
            self.clear()
            print()
            print("Goodbye.")
            print()

def main():
    pypanel = PyPanelX()
    pypanel.access()

if __name__ == "__main__":
    main()