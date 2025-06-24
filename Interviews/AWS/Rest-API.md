✅ 1. What is a REST API? How does it work?
Answer:

A REST API (Representational State Transfer) is a web service interface that allows systems to communicate over HTTP using a set of standard operations like GET, POST, PUT, DELETE, etc.

REST APIs are used to access and manipulate resources (e.g., users, orders, logs), where each resource is identified by a URI (Uniform Resource Identifier).

REST works by sending HTTP requests to a server and receiving responses — usually in JSON or XML format.

🔁 How it works (simple example):
GET /users/123 → fetch user with ID 123

POST /users → create a new user

PUT /users/123 → update user 123

DELETE /users/123 → delete user 123

Each HTTP verb maps to an action on a resource, and the client/server exchange is stateless.

✅ Follow-up: What are the core principles of REST architecture?
Statelessness

Each request contains all the information needed (no session stored on the server).

Client-Server Separation

The UI (frontend) and backend logic are separated.

Uniform Interface

Standardized way of interacting with resources using URIs and HTTP methods.

Resource-Based

Everything is treated as a resource, accessed via a URI.

Representations

Resources can be represented in JSON, XML, etc. (usually JSON today).

Cacheability

Responses must define if they can be cached to improve performance.

Layered System

Client doesn’t need to know if it’s talking to the actual server or an intermediate proxy.

✅ Follow-up: Is REST stateful or stateless?
REST is stateless.

Each HTTP request from the client must contain all the information needed to process the request — the server doesn’t store client context between requests.

🔍 Why this matters:
Easier to scale, since each request is independent

Supports load-balanced and distributed systems

However, any needed state (like auth tokens) must be handled explicitly (e.g., using headers like Authorization)
