# gRPC-yabozaed

Repository for gRPC lab - API Design F23.

# Purpose

This repository simulates a mock & mini version of Reddit. 

# Starting the Server and Client

- To start the server, run `python3 server/reddit_server.py --port 3000` from root. The `--port` argument is optional. The default port is `50051`.
- To start the client, run `python3 reddit_client.py --port 3000` from root in another window. The `--port` argument is optional. The default port is `50051`. Whatever port you run the client on has to match the server.

# Storage Used

This lab uses three json files to mock the data store - `comment.json`, `post.json`, `user.json`. Since this lab focuses on defining and implementing the APIs and not on the database management, I opted to use json objects instead of an actual SQL DB.

# Data Model



# Service Design 



# Testing

- To run the tests, use `python3 tests/reddit_test.py` from the root.

