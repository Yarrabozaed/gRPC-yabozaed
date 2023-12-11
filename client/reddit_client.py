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

    
# handler 3 - upvote/downvote a comment
def vote_comment(stub):
    vote_request = Reddit_pb2.VoteRequest(
        id="C001",
        upvote=False
    )
    response = stub.VoteComment(vote_request)
    
    if response.id == "0000":
        print(f"Failed to process request")
    else:
        print(f"Current score for comment {response.id}: {response.score}")
    
# handler 4 - upvote/downvote a comment
def retrieve_post(stub):
    post_request = Reddit_pb2.PostRequest(
        id = "P005"
    )
    
    response = stub.RetrievePost(post_request)
    
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
def create_comment(stub):
    comment = Reddit_pb2.Comment(
        author=Reddit_pb2.User(id="U001"), 
        content = "Is this thing on?",
        associated_comment = Reddit_pb2.Comment(id="C009"),
        associated_post = None
        
    )
    
    response = stub.CreateComment(comment)
    
    if response.id == "0000":
        print(f"Failed to process request")
    else:
        print(f"Comment created: {response.id}")

# handler 6 - get top comments
def get_top_comments(stub):
    top_comment_request = Reddit_pb2.TopCommentsRequest(
        postID = "P001",
        n = 1
    )
    
    response = stub.GetTopComments(top_comment_request)
    
    print(response.comments)
    
    print()
    
    print(f"Are there more comments? {response.hasResponses}")


def expand_comment_branch(stub):
    exoand_comment_request = Reddit_pb2.ExpandCommentBranchRequest(
        commentID = "C001",
        n = 3
    )
    
    response = stub.ExpandCommentBranch(exoand_comment_request)
    
    print(response.comments)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = Reddit_pb2_grpc.MockRedditStub(channel=channel)
        
        print("----------create_post()---------")
        create_post(stub)
        
        print("----------vote_post()---------")
        vote_post(stub)
        
        print("----------vote_comment()---------")
        vote_comment(stub)
        
        print("----------retrieve_post()---------")
        retrieve_post(stub)
        
        print("----------create_comment()---------")
        create_comment(stub)
        
        print("----------get_top_comments()---------")
        get_top_comments(stub)
        
        print("----------expand_comment_branch()---------")
        expand_comment_branch(stub)
        
        

if __name__ == '__main__':
    run()
