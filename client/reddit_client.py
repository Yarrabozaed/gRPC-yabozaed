import grpc
import os
import sys

# Generated with an LLM -> needed to access files in proto dir
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from proto import Reddit_pb2, Reddit_pb2_grpc

# handler 1 - create a post with user input
def create_post(stub):
    post = Reddit_pb2.Post(
        author=Reddit_pb2.User(id="U001"), 
        title="Sample Title",
        text="This is a sample post text.",
        media_url="http://example.com/sample.jpg"
    )
    
    response = stub.CreatePost(post)
    
    if response.id == "0000":
        print(f"Failed to process request")
    else:
        print(f"Post created: {response.id}")


# handler 2 - upvote/downvote a post
def vote_post(stub):
    vote_request = Reddit_pb2.VoteRequest(
        id="P001",
        upvote=True
    )
    response = stub.VotePost(vote_request)
    
    if response.id == "0000":
        print(f"Failed to process request")
    else:
        print(f"Current score for post {response.id}: {response.score}")

    
    
    

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = Reddit_pb2_grpc.MockRedditStub(channel=channel)
        
        print("----------create_post()---------")
        create_post(stub)
        
        print("----------vote_post()---------")
        vote_post(stub)
        

if __name__ == '__main__':
    run()
