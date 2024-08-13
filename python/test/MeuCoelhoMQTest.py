import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import MeuCoelhoMQ

#prepering for test
directoryDataMessages = '../src/dataMessages/'

def generateFileTest(lines, namefile):
    testFile = open(directoryDataMessages+namefile,"a")
    i=0
    testFile.write("Test"+str(i))
    while i<lines:
        i+=1
        testFile.write("\nTest"+str(i))
    testFile.close()

def deleteFileTest(file):
    try:
        os.remove(directoryDataMessages+file)
        print(f'{directoryDataMessages} was deleted successfully.')
    except FileNotFoundError:
        print(f'The file {directoryDataMessages} does not exist.')
    except PermissionError:
        print(f'Permission denied: Unable to delete {directoryDataMessages}.')
    except Exception as e:
        print(f'An error occurred: {e}')

#start the tests
def countMessagesTest():
    meuCoelho = MeuCoelhoMQ()
    numeroLinhas = meuCoelho.CountMessages(directoryDataMessages+"testFile.txt")
    print(numeroLinhas)
    assert numeroLinhas == 11

def LoadAndListQueesTest():
    meuCoelho = MeuCoelhoMQ()
    meuCoelho.LoadAndListQuees()
    print(meuCoelho.queesRunning)
    assert meuCoelho.queesRunning["testFile1"] == 8
    assert meuCoelho.queesRunning["testFile2"] == 6
    assert meuCoelho.queesRunning["testFile3"] == 13


#init all    
if __name__ == "__main__":
    logging.basicConfig()
    try:
        #for countMessagesTest
        generateFileTest(10,"testFile.txt")
        #for LoadQueesTest
        generateFileTest(7,"testFile1.txt")
        generateFileTest(5,"testFile2.txt")
        generateFileTest(12,"testFile3.txt")

        countMessagesTest()
        LoadAndListQueesTest()
    finally:
        deleteFileTest("testFile.txt")
        deleteFileTest("testFile1.txt")
        deleteFileTest("testFile2.txt")
        deleteFileTest("testFile3.txt")
