"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging

import os
import grpc
import transactionProducer_pb2
import transactionProducer_pb2_grpc



class MeuCoelhoMQ(transactionProducer_pb2_grpc.GreeterServicer):
    directoryDataMessages = 'dataMessages/'
    queesRunning = {}
    subscribedQuee = {}

    def SendMessage(self, request, context):
        return transactionProducer_pb2.MessageReply(ack="ok")
    
    def CountMessages(self, fileName):
        line_count=0

        with open(fileName,'r') as file:
            for line in file:
                line_count+=1
            file.close()
        return line_count
    
    def LoadAndListQuees(self):
        files = os.listdir(self.directoryDataMessages)
        if len(files) > 0:
            for file in files:
                channel = file[:-4]
                self.queesRunning[channel]=self.CountMessages(self.directoryDataMessages+file)
                print("The channel "+channel+" has "+str(self.queesRunning[channel]))
        return files
    
    def SaveMessage(self, channel ,message):
        try:
            file = open(self.directoryDataMessages+channel+".txt", "a")
            if channel not in self.queesRunning:
                file.write(message)
                self.queesRunning[channel]=1
                print("New quee added: "+channel)
            else:
                file.write("\n"+message)
        finally:
            file.close()

    def KillQuee(self, channel):
        print("Trying to kill "+channel)
        try:
            os.remove(self.directoryDataMessages+channel+".txt")
            del self.queesRunning[channel]
            print(channel+" was killed.")
        except Exception as e:
            print(f'Fail to kill the quee {channel}, an error occurred: {e}')

    def SubscribeQuee(self,channel,subscribe):
        if channel in self.queesRunning:
            self.subscribedQuee[channel]=subscribe

def serve():
    portProducer = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transactionProducer_pb2_grpc.add_GreeterServicer_to_server(MeuCoelhoMQ(), server)
    server.add_insecure_port("[::]:" + portProducer)
    server.start()
    print("Server started, listening on " + portProducer)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()