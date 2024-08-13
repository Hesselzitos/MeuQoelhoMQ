import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import MeuCoelhoMQ

#prepering for test
directoryTestDataMessages = '../src/dataMessages/'

def generateFileTest(lines, namefile):
    testFile = open(directoryTestDataMessages+namefile,"a")
    i=0
    testFile.write("Test"+str(i))
    while i<lines:
        i+=1
        testFile.write("\nTest"+str(i))
    testFile.close()

def deleteFileTest(file):
    try:
        os.remove(directoryTestDataMessages+file)
    except FileNotFoundError:
        print(f'The file {directoryTestDataMessages} does not exist.')
    except PermissionError:
        print(f'Permission denied: Unable to delete {directoryTestDataMessages}.')
    except Exception as e:
        print(f'An error occurred: {e}')

#start the tests
def countMessagesTest():
    meuCoelho = MeuCoelhoMQ()
    numeroLinhas = meuCoelho.CountMessages(directoryTestDataMessages+"testFile.txt")
    assert numeroLinhas == 11
    print("countMessagesTest=ok")

def LoadAndListQueesTest():
    meuCoelho = MeuCoelhoMQ()
    meuCoelho.LoadAndListQuees()
    assert meuCoelho.queesRunning["testFile1"] == 8
    assert meuCoelho.queesRunning["testFile2"] == 6
    assert meuCoelho.queesRunning["testFile3"] == 13
    print("LoadAndListQueesTest=ok")

def SaveMessageTest():
    channel = "Test"
    message = "SaveMessageTest"
    meuCoelho = MeuCoelhoMQ()
    meuCoelho.SaveMessage(channel,message)

    try:
        file = open(MeuCoelhoMQ.directoryDataMessages+channel+".txt","r")
        messageRead = file.read()
    finally:
        file.close()

    assert meuCoelho.queesRunning["Test"] == 1
    assert messageRead == message
    print("SaveMessageTest=ok")

def KillQueeTest():
    channel = "KillQueeTest"
    lines = 2
    generateFileTest(lines,channel+".txt")

    meuCoelho = MeuCoelhoMQ()
    meuCoelho.queesRunning[channel]=lines
    meuCoelho.KillQuee(channel)
    print("KillQueeTest=ok")

def SubscribeQueeTest():
    meuCoelho = MeuCoelhoMQ()
    quee = "SubscribeQueeTest"
    meuCoelho.queesRunning[quee]=1

    assert quee not in meuCoelho.subscribedQuee
    meuCoelho.SubscribeQuee(quee,"ConsumerTest")
    assert quee in meuCoelho.subscribedQuee
    assert meuCoelho.subscribedQuee[quee] == "ConsumerTest"
    print("SubscribeQueeTest=ok")

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
        SaveMessageTest()
        KillQueeTest()
        SubscribeQueeTest()
    finally:
        deleteFileTest("testFile.txt")
        deleteFileTest("testFile1.txt")
        deleteFileTest("testFile2.txt")
        deleteFileTest("testFile3.txt")
        deleteFileTest("Test.txt")
