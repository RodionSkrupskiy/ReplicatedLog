import os
import grpc
import ReplicatedLog_pb2
import ReplicatedLog_pb2_grpc
from concurrent import futures

logs = []
slave_host = os.getenv('SLAVE_HOST', 'localhost')
class Logger(ReplicatedLog_pb2_grpc.PostRequestServiceServicer):
    def PostRequest(self, request, context):
        logs.append(request.msg)
        with grpc.insecure_channel(f'{slave_host}:50052') as channel:
            client = ReplicatedLog_pb2_grpc.PostRequestServiceStub(channel)
            slave_request = ReplicatedLog_pb2.POST(msg=request.msg)
            if client.PostRequest(slave_request).msg == '1':
                return ReplicatedLog_pb2.POSTResponse(msg='Master and Slaves have recived msg')

class SendLogs(ReplicatedLog_pb2_grpc.GetRequestServiceServicer):
    def GetRequest(self, request, context):
        with grpc.insecure_channel(f'{slave_host}:50052') as channel:
            client = ReplicatedLog_pb2_grpc.GetRequestServiceStub(channel)
            slave_request = ReplicatedLog_pb2.GET(msg='1')

            return ReplicatedLog_pb2.GETResponse(data=client.GetRequest(slave_request).data)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    ReplicatedLog_pb2_grpc.add_PostRequestServiceServicer_to_server(Logger(), server)
    ReplicatedLog_pb2_grpc.add_GetRequestServiceServicer_to_server(SendLogs(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()



if __name__ == "__main__":
    serve()
