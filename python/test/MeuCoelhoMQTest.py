import sys
import os
import logging

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import MeuCoelhoMQReciver,MeuCoelhoMQSender,queesRunning,subscribedQuee

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
    meuCoelho = MeuCoelhoMQReciver()
    numeroLinhas = meuCoelho.CountMessages(directoryTestDataMessages+"testFile.txt")
    assert numeroLinhas == 11
    print("countMessagesTest=ok")

def LoadAndListQueesTest():
    meuCoelho = MeuCoelhoMQReciver()
    meuCoelho.LoadAndListQuees()
    assert queesRunning["testFile1"] == 8
    assert queesRunning["testFile2"] == 6
    assert queesRunning["testFile3"] == 13
    print("LoadAndListQueesTest=ok")

def SaveMessageTest():
    channel = "Test"
    message = "SaveMessageTest"
    meuCoelho = MeuCoelhoMQReciver()
    meuCoelho.SaveMessage(channel,message)

    try:
        file = open(directoryTestDataMessages+channel+".txt","r")
        messageRead = file.read()
    finally:
        file.close()

    assert queesRunning["Test"] == 1
    assert messageRead == message
    print("SaveMessageTest=ok")

def KillQueeTest():
    channel = "KillQueeTest"
    lines = 2
    generateFileTest(lines,channel+".txt")

    meuCoelho = MeuCoelhoMQReciver()
    queesRunning[channel]=lines
    meuCoelho.KillQuee(channel)
    print("KillQueeTest=ok")

def SubscribeTest():
    meuCoelho = MeuCoelhoMQSender()
    quee = "SubscribeTest"
    queesRunning[quee]=1

    assert quee not in subscribedQuee
    meuCoelho.Subscribe(quee,"ConsumerTest")
    assert quee in subscribedQuee
    assert subscribedQuee[quee] == "ConsumerTest"
    print("SubscribeTest=ok")

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
        SubscribeTest()
    finally:
        deleteFileTest("testFile.txt")
        deleteFileTest("testFile1.txt")
        deleteFileTest("testFile2.txt")
        deleteFileTest("testFile3.txt")
        deleteFileTest("Test.txt")
