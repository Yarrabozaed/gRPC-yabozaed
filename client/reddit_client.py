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
    
class MockRedditResolvers:
    
    def __init__(self, stub):
        self.stub = stub
    
    # handler 1 - create a post with user input
    def create_post(self, userID="U001", post_title="Sample title", post_text = "This is a sample post text.", url = "http://fake.com"):
        post = Reddit_pb2.Post(
            author = Reddit_pb2.User(id=userID), 
            title = post_title,
            text = post_text,
            media_url= url
        )
        
        response = self.stub.CreatePost(post)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Post created: {response.id}")


    # handler 2 - upvote/downvote a post
    def vote_post(self, req_id = "P001", upvote_tf=True):
        vote_request = Reddit_pb2.VoteRequest(
            id= req_id,
            upvote=upvote_tf
        )
        response = self.stub.VotePost(vote_request)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Current score for post {response.id}: {response.score}")

        
    # handler 3 - upvote/downvote a comment
    def vote_comment(self, req_id = "C001", upvote_tf = False):
        vote_request = Reddit_pb2.VoteRequest(
            id= req_id,
            upvote= upvote_tf
        )
        response = self.stub.VoteComment(vote_request)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Current score for comment {response.id}: {response.score}")
        
    # handler 4 - upvote/downvote a comment
    def retrieve_post(self, post_id="P005"):
        post_request = Reddit_pb2.PostRequest(
            id = post_id
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
    def create_comment(self, author_id="U001", input_content="Is this thing on?", comment_id = "C009", associated_post_id = None):
        comment = Reddit_pb2.Comment(
            author=Reddit_pb2.User(id=author_id), 
            content = input_content,
            associated_comment = Reddit_pb2.Comment(id= comment_id),
            associated_post = associated_post_id
        )
        
        response = self.stub.CreateComment(comment)
        
        if response.id == "0000":
            print(f"Failed to process request")
        else:
            print(f"Comment created: {response.id}")

    # handler 6 - get top comments
    def get_top_comments(self, id="P001", inp_n = 1):
        top_comment_request = Reddit_pb2.TopCommentsRequest(
            postID = id,
            n = inp_n
        )
        
        response = self.stub.GetTopComments(top_comment_request)
        
        print(response.comments)
        
        print()
        
        print(f"Are there more comments? {response.hasResponses}")


    def expand_comment_branch(self, id = "C001", inp_n = 3):
        exoand_comment_request = Reddit_pb2.ExpandCommentBranchRequest(
            commentID = id,
            n = inp_n
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
    
    resolver = MockRedditResolvers(client.stub)
    
    print("----------create_post()---------")
    resolver.create_post()
            
    print("----------vote_post()---------")
    resolver.vote_post()
            
    print("----------vote_comment()---------")
    resolver.vote_comment()
            
    print("----------retrieve_post()---------")
    resolver.retrieve_post()
            
    print("----------create_comment()---------")
    resolver.create_comment()
            
    print("----------get_top_comments()---------")
    resolver.get_top_comments()
            
    print("----------expand_comment_branch()---------")
    resolver.expand_comment_branch()
