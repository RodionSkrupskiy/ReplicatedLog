import os
import grpc
import ReplicatedLog_pb2
import ReplicatedLog_pb2_grpc

slave_host = os.getenv('SLAVE_HOST', 'localhost')
master_host = os.getenv('MASTER_HOST', 'localhost')
print(slave_host, master_host)

def post():
    with grpc.insecure_channel(f'{master_host}:50051') as channel:
        client = ReplicatedLog_pb2_grpc.PostRequestServiceStub(channel)
        request = ReplicatedLog_pb2.POST(msg=input('Enter values to log'))
        response = client.PostRequest(request)
        print(response)

def get():
    with grpc.insecure_channel(f'{master_host}:50051') as channel:
        client = ReplicatedLog_pb2_grpc.GetRequestServiceStub(channel)
        request = ReplicatedLog_pb2.GET(msg='1')
        response = client.GetRequest(request)
        print(response.data)

user_input = input('Enter POST, GET or q').lower()
while user_input != 'q':
    if user_input == 'post':
        print('Calling POST')
        post()
    elif user_input == 'get':
        print('calling GET')
        get()
    else:
        print('Wrong input')
    user_input = input('Enter POST, GET or q').lower()
