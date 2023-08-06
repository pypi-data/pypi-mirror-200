import os
import time

from datetime import datetime

from hash_calc.HashCalc import HashCalc

class Controller():
    def __init__(self, filePath) -> None:
        self.startTime = time.time()
        self.filePath = filePath
        self.hash = HashCalc(self.filePath)

    def printHeader(self):
        print("################################################################################")
        print("")
        print("lineident by 5f0")
        print("Searches files line by line for given words")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("-->    Path: " + self.filePath)
        print("-->     MD5: " + self.hash.md5)
        print("-->  SHA256: " + self.hash.sha256)
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printOptions(self, words, method):
        print("Search Options:")
        print("---")
        print("")
        print("Method: " + method)
        print(" Words: " + str(words))
        print("")

    def printResults(self, results, format):
        print("")
        print("Result:")
        print("---")
        print("Hits: " + str(len(results)))
        print("---")
        print("")
        if(len(results) > 0):
            for result in results:
                if(format == "std"):
                    print("Line Nr: " + str(result[0]))
                    print("     --> " + result[1])
                elif(format=="ol"):
                    print("Line Nr: " + str(result[0]) + " --> " + result[1])
        else:
            print("No lines matched")
        print("")

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")