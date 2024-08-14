from concurrent import futures
import logging
import os

import grpc
import transactionProducer_pb2
import transactionProducer_pb2_grpc
import transactionConsumer_pb2
import transactionConsumer_pb2_grpc


directoryDataMessages = 'dataMessages/'
queesRunning = {}
subscribedQuee = {}

class MeuCoelhoMQSender(transactionConsumer_pb2_grpc.ConsumerServicer):
    
    def ListQuees(self, AskForQuees,context):
        print(AskForQuees)
        listQuees=list(queesRunning.keys())
        return transactionConsumer_pb2.AskForQueesReplay(listQuees=listQuees)

    def ConsumeMessage(self, AskForMessage, context):
        channel=AskForMessage.channel
        consumer=AskForMessage.consumerName
        if subscribedQuee.get(channel)==consumer:
            message = self.ReadAndDeleteMessage(channel)
            return transactionConsumer_pb2.AskForMessageReplay(ack=message)
        return transactionConsumer_pb2.AskForMessageReplay(ack="Not subscribed")
        
    def ReadAndDeleteMessage(self, channel):
        print("Trying to consume a message")
        message = "No Messages"
        if queesRunning.get(channel)>0:
            try:
                file = open(directoryDataMessages+channel+".txt", "r")
                lines = file.readlines()
                message = lines[0]
                lines = lines[1:]
            finally:
                file.close()
            try: 
                file = open(directoryDataMessages+channel+".txt", "w")
                file.writelines(lines)
                queesRunning[channel]=queesRunning.get(channel)-1
                print("Message deleted, now are "+str(queesRunning.get(channel)))
            finally:
                file.close()
        return message


    def Subscribe(self,AskForSubscribe, context):
        channel=AskForSubscribe.channel
        subscribe=AskForSubscribe.consumerName
        print(f'The {subscribe} is trying to subscribe the {channel}')
        if channel in queesRunning and subscribe not in subscribedQuee:
            subscribedQuee[channel]=subscribe
            print(f'The channel {channel} have an new subscriber, {subscribe}')
            return transactionConsumer_pb2.AskForSubscribeReplay(ack="ok")
        return transactionConsumer_pb2.AskForSubscribeReplay(ack="Already sub")

class MeuCoelhoMQReciver(transactionProducer_pb2_grpc.GreeterServicer):

    def SendMessage(self,SendMessageRequest,context ):
        self.SaveMessage(SendMessageRequest.channel,SendMessageRequest.message)
        return transactionProducer_pb2.MessageReply(ack="ok")
    
    def CountMessages(self, fileName):
        line_count=0

        with open(fileName,'r') as file:
            for line in file:
                line_count+=1
            file.close()
        return line_count
    
    def LoadQuees(self):
        files = os.listdir(directoryDataMessages)
        if len(files) > 0:
            for file in files:
                channel = file[:-4]
                queesRunning[channel]=self.CountMessages(directoryDataMessages+file)
                print("Quees loaded")
    
    def SaveMessage(self, channel ,message):
        try:
            file = open(directoryDataMessages+channel+".txt", "a")
            if channel not in queesRunning:
                file.write(message)
                queesRunning[channel]=1
                print("New quee added: "+channel)
            else:
                file.write("\n"+message)
                queesRunning[channel]=queesRunning.get(channel)+1
        finally:
            file.close()

    def KillQuee(self, channel):
        print("Trying to kill "+channel)
        try:
            os.remove(directoryDataMessages+channel+".txt")
            del queesRunning[channel]
            print(channel+" was killed.")
        except Exception as e:
            print(f'Fail to kill the quee {channel}, an error occurred: {e}')

def serve():
    portProducer = "50051"
    portConsumer = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transactionProducer_pb2_grpc.add_GreeterServicer_to_server(MeuCoelhoMQReciver(), server)
    transactionConsumer_pb2_grpc.add_ConsumerServicer_to_server(MeuCoelhoMQSender(), server)
    server.add_insecure_port("[::]:" + portProducer)
    server.add_insecure_port("[::]:" + portConsumer)
    server.start()
    print("Server started, listening on " + portProducer)
    print("Server started, listening on " + portConsumer)
    MeuCoelhoMQReciver().LoadQuees()
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig()
    serve()