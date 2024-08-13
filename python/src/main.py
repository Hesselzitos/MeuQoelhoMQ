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
        file = open(channel+".txt", "a")
        file.write(message)
        file.close
        if self.queesRunning[channel]==None:
            self.queesRunning[channel]=self.CountMessages(channel)
    #def KillQuee():

    #def SubscribeQuee():
        
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transactionProducer_pb2_grpc.add_GreeterServicer_to_server(MeuCoelhoMQ(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()