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

        # response to client 
        response = Reddit_pb2.Post()
        
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
