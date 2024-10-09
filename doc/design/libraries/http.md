# libraries: http

The http library is an implementation of an HTTP server on top of Boost Beast, 
a Boost library that provides an HTTP protocol implementation. 

The top class is `http::Server`, which internally opens a listening TCP 
session (`TCPListener`) for incoming connections. 
Once a client is connected, the server spawn a new `ServerSession` 
to handle the connection.

For flexibility purposes, the endpoints accessible to the client can be 
dynamically managed. At any time during the execution, endpoints can be added
and removed.

## Endpoints

A endpoint is represented by two values:

- A HTTP method, can be `GET`, `POST`, `PUT`, etc.
- A target, that represent the 'path' of the endpoint.

For example, the following endpoint:
```
GET localhost:9373/pipelines/1/status
```
has the 3 level target `pipelines`, `1`, `status`. Target levels can be 
strings, in which case they need to match exactly, or regular expressions. In
the example above, the second level can be any integer number.

## Request handler

When registering a new endpoint in the server, the caller code need to provide
a function that will handle the client request and generates 
the server response.

The abstract class `RequestHandler` exists for that purpose. It has two
methods to override, one for endpoints declaration and one for requests 
handling. The latter is responsible for parsing the request, doing the 
work asked by the client, and generating the HTTP response.

Request handlers can be added to the server using `Server::add_handler()`.

When a client is making a HTTP request to the server, the server will try to 
match this request with the declared endpoints by the different handlers. 
If a match is found, the corresponding handler will be called to generate 
a response. 
The class `RequestDispatcher` handle the matching job internally inside 
the server.