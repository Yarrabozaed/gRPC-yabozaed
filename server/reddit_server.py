import grpc
from concurrent import futures
import logging
import os
import sys
import json
import time
import random

# Generated with an LLM -> needed to access files in proto dir
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from proto import Reddit_pb2, Reddit_pb2_grpc

USER_IDs = ["U001","U002","U003","U004","U005"]


post_fp = os.path.join(parent_dir, 'data', 'post.json')
comment_fp = os.path.join(parent_dir, 'data', 'comment.json')
user_fp = os.path.join(parent_dir, 'data', 'user.json')

#load all the post data from JSON file
with open(post_fp, 'r') as p:
    posts = json.load(p)

#load all the comment data from JSON file
with open(comment_fp, 'r') as c:
    comments = json.load(c)

#load all the user data from JSON file
with open(user_fp, 'r') as u:
    users = json.load(u)
    
    
class MockRedditService(Reddit_pb2_grpc.MockRedditServicer):
    
    # CreatePost rpc
    def CreatePost(self, request, context):
        
        #Generate ID for the new post
        post_id = f"P{random.randint(1000, 9999)}"

        # Set the time based on real-time data
        publication_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        # set response object as Post() 
        response = Reddit_pb2.Post()

        # this is the json-to-push into the post store
        new_post = {}
        
        # ensure the user ID passed is a real person
        if request.author.id not in USER_IDs:
            return response
        
        # try pulling all the needed data from the client's request
        try:
            response.id = post_id
            response.author.CopyFrom(
                Reddit_pb2.User(
                    id=request.author.id
                )
            )
            response.title = request.title
            response.text = request.text
            response.media_url = request.media_url

            response.score = 0
            response.state = Reddit_pb2.PostState.Value('POST_NORMAL')
            response.publication_date = publication_date
        except:
            # if it fails, return -1 to indicate failure...
            response.id = "0000"
            return response

        # this JSON object will be appended to the post.json list
        new_post = {
            "author": {"id": request.author.id},
            "score": 0,
            "state": "NORMAL",
            "publication_date": publication_date,                
            "title": request.title,
            "text": request.text,
            "media_url": request.media_url,
            "id": post_id
        }
        
        posts.append(new_post)
        with open(post_fp, 'w') as file:
            json.dump(posts, file, indent=4)
        
        # response data
        return response

    # VotePost rpc
    def VotePost(self, request, context):
        
        for post in posts:
            if request.id == post['id']:
                if request.upvote == True:
                    post['score'] += 1
                else:
                    post['score'] -= 1
                
                response = Reddit_pb2.VoteResponse(
                    id = request.id,
                    score = post['score']
                )
                
                try:
                    with open(post_fp, 'w') as file:
                        json.dump(posts, file, indent=4)
                except:
                    print("Failed to update file")
                    return Reddit_pb2.VoteResponse(
                        id = "0000",
                        score = -9999
                    )
                return response

        print("Post not found")
        return Reddit_pb2.VoteResponse(
            id = "0000",
            score = -9999
        )
    
    # VoteComment rpc
    def VoteComment(self, request, context):
        
        for comment in comments:
            if request.id == comment['id']:
                if request.upvote == True:
                    comment['score'] += 1
                else:
                    comment['score'] -= 1
                
                response = Reddit_pb2.VoteResponse(
                    id = request.id,
                    score = comment['score']
                )
                
                try:
                    with open(comment_fp, 'w') as file:
                        json.dump(comments, file, indent=4)
                except:
                    print("Failed to update file")
                    return Reddit_pb2.VoteResponse(
                        id = "0000",
                        score = -9999
                    )
                return response

        print("Comment not found")
        return Reddit_pb2.VoteResponse(
            id = "0000",
            score = -9999
        )
    
    # RetrievePost rpc
    def RetrievePost(self, request, context):
        for post in posts:
            if request.id == post['id']:
                response = Reddit_pb2.Post(
                    id = post['id'],
                    score = post['score'],
                    state = "POST_" + post['state'],
                    publication_date = post['publication_date'],
                    title = post['title'],
                    text = post['text'],
                    media_url = post['media_url']
                )
                
                response.author.CopyFrom(
                    Reddit_pb2.User(
                        id=post['author']['id']
                    )
                )
                
                return response
        
        return Reddit_pb2.Post(
            id = "0000"
        )
        
    
    # CHANGE THIS
    def CreateComment(self, request, context):
        
        #Generate ID for the new comment
        comment_id = f"C{random.randint(1000, 9999)}"

        # Set the time based on real-time data
        publication_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())

        # set response object as Comment() 
        response = Reddit_pb2.Comment()

        # this is the json-to-push into the post store
        new_comment = {}
        
        # ensure the user ID passed is a real person
        if request.author.id not in USER_IDs:
            return response
        
        # try pulling all the needed data from the client's request
        try:
            response.id = comment_id
            response.author.CopyFrom(
                Reddit_pb2.User(
                    id=request.author.id
                )
            )
            response.content = request.content
            
            if request.HasField('associated_post'):
                response.associated_post.CopyFrom(request.associated_post)
            
            if request.HasField('associated_comment'):
                response.associated_comment.CopyFrom(request.associated_comment)
            
            response.score = 0
            response.state = Reddit_pb2.CommentState.Value('COMMENT_NORMAL')
            response.publication_date = publication_date
        except:
            # if it fails, return -1 to indicate failure...
            response.id = "0000"
            return response

        # this JSON object will be appended to the post.json list
        new_comment = {
            "author": {"id": request.author.id},
            "score": 0,
            "state": "NORMAL",
            "publication_date": publication_date,
            "content": request.content,
            "id": comment_id,
            "associated_post": request.associated_post.id if request.HasField('associated_post') else None,
            "associated_comment": request.associated_comment.id if request.HasField('associated_comment') else None
        }
        
        comments.append(new_comment)
        with open(comment_fp, 'w') as file:
            json.dump(comments, file, indent=4)
        
        # response data
        return response
    
    def GetTopComments(self, request, context):
        associated_comments = []
        
        # get all the comments under some post
        for comment in comments:
            if comment['associated_post'] is not None:
                if comment['associated_post']['id'] == request.postID:
                    associated_comments.append(comment)

        sorted_comments = sorted(associated_comments, key=lambda x: x['score'], reverse=True)
        
        top_comments = []
        
        for i in range(0, request.n):
            top_comments.append(sorted_comments[i])
            
            if (i+1) >= len(sorted_comments):
                break

        comments_response = []
        
        # format the response
        for comment in top_comments:
            
            c = Reddit_pb2.Comment(
                author = Reddit_pb2.User(id=comment['author']['id']),
                score = comment['score'],
                state = "COMMENT_" + comment['state'],
                publication_date = comment['publication_date'],
                content = comment['content'],
                id = comment['id']
            )

            if comment['associated_comment'] is not None:
                c.associated_comment.CopyFrom(
                    Reddit_pb2.Comment(
                        id= comment['associated_comment']['id']
                    )
                )
                
            
            if comment['associated_post'] is not None:
                c.associated_post.CopyFrom(
                    Reddit_pb2.Post(
                        id= comment['associated_post']['id']
                    )
                )
            
            comments_response.append(c)

        has_more_responses = False
        
        # check if there are more comments we didn't return under the post
        if len(sorted_comments) > request.n:
            has_more_responses = True

        response = Reddit_pb2.TopCommentsResponse(
            comments = comments_response,
            hasResponses = has_more_responses
        )

        return response
              
    

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
    logging.basicConfig(level=logging.INFO)
    print("Starting the server...")
    serve()
