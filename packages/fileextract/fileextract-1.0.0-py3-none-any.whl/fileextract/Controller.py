import os
import time

from datetime import datetime

class Controller():
    def __init__(self) -> None:
        self.startTime = time.time()

    def printHeader(self):
        print("################################################################################")
        print("")
        print("fileextract by 5f0")
        print("Extracts files from .raw/.dd images by using sleuthkit")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printExecutionTime(self):
        end = time.time()
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")