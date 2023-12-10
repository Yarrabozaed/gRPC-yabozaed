import grpc
from concurrent import futures
import logging
import os
import sys

# Generated with an LLM -> needed to access files in proto dir
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from proto import Reddit_pb2, Reddit_pb2_grpc

class MockRedditService(Reddit_pb2_grpc.MockRedditServicer):
    def createPost(self, request, context):
        return Reddit_pb2.Post()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    Reddit_pb2_grpc.add_MockRedditServicer_to_server(
        MockRedditService(), 
        server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Server started on port 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        #GRACEFULLY exit without panic stopping the server
        server.stop(0)
        print("Server has been stopped")

if __name__ == "__main__":
    logging.basicConfig()
    print("Starting the server...")
    serve()
