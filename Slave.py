import random
import time
import grpc
import ReplicatedLog_pb2
import ReplicatedLog_pb2_grpc
from concurrent import futures


logs = []

class SlaveLogger(ReplicatedLog_pb2_grpc.PostRequestServiceServicer):
    def PostRequest(self, request, context):
        logs.append(request.msg)
        time.sleep(random.randint(0, 7))
        return ReplicatedLog_pb2.POSTResponse(msg='1')

class SlaveSendLogs(ReplicatedLog_pb2_grpc.GetRequestServiceServicer):
    def GetRequest(self, request, context):
        return ReplicatedLog_pb2.GETResponse(data=logs)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    ReplicatedLog_pb2_grpc.add_PostRequestServiceServicer_to_server(SlaveLogger(), server)
    ReplicatedLog_pb2_grpc.add_GetRequestServiceServicer_to_server(SlaveSendLogs(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()



if __name__ == "__main__":
    serve()
