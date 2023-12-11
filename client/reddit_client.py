import grpc
import os
import sys
import argparse


# Generated with an LLM -> needed to access files in proto dir
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from proto import Reddit_pb2, Reddit_pb2_grpc


class MockRedditClient:
    
    def __init__(self, host='localhost', port=50051):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = Reddit_pb2_grpc.MockRedditStub(self.channel) 
    
    # handler 1 - create a post with user input
    def create_post(self):
        post = Reddit_pb2.Post(
            author=Reddit_pb2.User(id="U001"), 
            title="Sample Title",
            text="This is a sample post text.",
            media_url="http://example.com/sample.jpg"
        )
        
        response = self.stub.CreatePost(post)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Post created: {response.id}")


    # handler 2 - upvote/downvote a post
    def vote_post(self):
        vote_request = Reddit_pb2.VoteRequest(
            id="P001",
            upvote=True
        )
        response = self.stub.VotePost(vote_request)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Current score for post {response.id}: {response.score}")

        
    # handler 3 - upvote/downvote a comment
    def vote_comment(self):
        vote_request = Reddit_pb2.VoteRequest(
            id="C001",
            upvote=False
        )
        response = self.stub.VoteComment(vote_request)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Current score for comment {response.id}: {response.score}")
        
    # handler 4 - upvote/downvote a comment
    def retrieve_post(self):
        post_request = Reddit_pb2.PostRequest(
            id = "P005"
        )
        
        response = self.stub.RetrievePost(post_request)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Here's the requested post {response.id}: ")
            print(f"           Author: {response.author}")
            print(f"            Score: {response.score}")
            print(f"            State: {response.state}")
            print(f" Publication Date: {response.publication_date}")
            print(f"            Title: {response.title}")
            print(f"             Text: {response.text}")
            print(f"        Media URL: {response.media_url}")
            
    # handler 5 - create a new comment with user input
    def create_comment(self):
        comment = Reddit_pb2.Comment(
            author=Reddit_pb2.User(id="U001"), 
            content = "Is this thing on?",
            associated_comment = Reddit_pb2.Comment(id="C009"),
            associated_post = None
            
        )
        
        response = self.stub.CreateComment(comment)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Comment created: {response.id}")

    # handler 6 - get top comments
    def get_top_comments(self):
        top_comment_request = Reddit_pb2.TopCommentsRequest(
            postID = "P001",
            n = 1
        )
        
        response = self.stub.GetTopComments(top_comment_request)
        
        print(response.comments)
        
        print()
        
        print(f"Are there more comments? {response.hasResponses}")


    def expand_comment_branch(self):
        exoand_comment_request = Reddit_pb2.ExpandCommentBranchRequest(
            commentID = "C001",
            n = 3
        )
        
        response = self.stub.ExpandCommentBranch(exoand_comment_request)
        
        print(response.comments)

    def close(self):
        self.channel.close()
            
          

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MockReddit gRPC client')
    
    parser.add_argument('--port', type=int, default=50051, help='Port to listen on (default: 50051)')
    
    args = parser.parse_args()
    
    client = MockRedditClient(host='localhost', port=args.port)
    
    print("----------create_post()---------")
    client.create_post()
            
    print("----------vote_post()---------")
    client.vote_post()
            
    print("----------vote_comment()---------")
    client.vote_comment()
            
    print("----------retrieve_post()---------")
    client.retrieve_post()
            
    print("----------create_comment()---------")
    client.create_comment()
            
    print("----------get_top_comments()---------")
    client.get_top_comments()
            
    print("----------expand_comment_branch()---------")
    client.expand_comment_branch()
