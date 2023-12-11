import unittest
import os, sys
from unittest.mock import Mock, create_autospec

# Generated with an LLM -> needed to access files in proto dir
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from proto import Reddit_pb2, Reddit_pb2_grpc

from client.reddit_client import MockRedditResolvers

class TestMockReddit(unittest.TestCase):
    def setUp(self):
        # Mocking the stub (which is the server)
        self.mock_stub = create_autospec(Reddit_pb2_grpc.MockRedditStub)

        # making an instance of the resolver with injection of mock
        self.resolver = MockRedditResolvers(self.mock_stub)
    
    # Retrieve a post
    def test_retrieve_post(self):
        mock_response = Reddit_pb2.Post(
            id="P005",
            author=Reddit_pb2.User(id="U005"),
            score=75,
            state=Reddit_pb2.PostState.Value('POST_NORMAL'),
            publication_date="2021-09-05T22:15:00Z",
            title="Space Exploration",
            text="Humanity's quest to explore the final frontier.",
            media_url="http://example.com/video2.mp4"
        )
        
        self.mock_stub.RetrievePost = Mock()

        self.mock_stub.RetrievePost.return_value = mock_response
        
        self.resolver.retrieve_post(post_id="P005")
        
        self.mock_stub.RetrievePost.assert_called_once()
        
    
    # Retrieve most upvoted comments under the post
    def test_retrieve_top_comments(self):
        mock_response = Reddit_pb2.TopCommentsResponse(
            comments = [Reddit_pb2.Comment(
                author = Reddit_pb2.User(id = "U001"),
                score = 100,
                state = "COMMENT_NORMAL",
                publication_date="2021-09-05T22:15:00Z",
                content = "hello = )",
                id = "C001"
            )],
            hasResponses = True
        )
        
        self.mock_stub.GetTopComments = Mock()

        self.mock_stub.GetTopComments.return_value = mock_response
        
        self.resolver.get_top_comments(id="P001")
        
        self.mock_stub.GetTopComments.assert_called_once()
    
    # Expand the most upvoted comment
    def test_expand_top_comment(self):
        mock_response = Reddit_pb2.ExpandCommentBranchResponse(
            comments = [Reddit_pb2.Comment(
                author = Reddit_pb2.User(id = "U001"),
                score = 100,
                state = "COMMENT_NORMAL",
                publication_date="2021-09-05T22:15:00Z",
                content = "hello = )",
                id = "C002"
            )]
        )
        
        self.mock_stub.ExpandCommentBranch = Mock()

        self.mock_stub.ExpandCommentBranch.return_value = mock_response
        
        self.resolver.expand_comment_branch(id="C001")
        
        self.mock_stub.ExpandCommentBranch.assert_called_once()
    
    # Return the most upvoted reply under the most upvoted comment, 
    #       or None if there are no comments or no replies under the most upvoted one
    def test_retrieve_top_reply(self):
        mock_response = Reddit_pb2.TopCommentsResponse(
            comments = [Reddit_pb2.Comment(
                author = Reddit_pb2.User(id = "U001"),
                score = 100,
                state = "COMMENT_NORMAL",
                publication_date="2021-09-05T22:15:00Z",
                content = "hello = )",
                id = "C001"
            )],
            hasResponses = True
        )
        
        self.mock_stub.GetTopComments = Mock()

        self.mock_stub.GetTopComments.return_value = mock_response
        
        self.resolver.get_top_comments(id="P001",inp_n=1)
        
        self.mock_stub.GetTopComments.assert_called_once()
        
        mock_response = Reddit_pb2.ExpandCommentBranchResponse(
            comments = [Reddit_pb2.Comment(
                author = Reddit_pb2.User(id = "U001"),
                score = 100,
                state = "COMMENT_NORMAL",
                publication_date="2021-09-05T22:15:00Z",
                content = "hello = )",
                id = "C002"
            )]
        )
        
        self.mock_stub.ExpandCommentBranch = Mock()

        self.mock_stub.ExpandCommentBranch.return_value = mock_response
        
        self.resolver.expand_comment_branch(id="C001")
        
        self.mock_stub.ExpandCommentBranch.assert_called_once()
        

if __name__ == '__main__':
    unittest.main()