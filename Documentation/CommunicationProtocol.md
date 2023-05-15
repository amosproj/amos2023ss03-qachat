# Communication Protocols 
##  REST API

```seq
participant Client
participant Server

Client->Server: GET /api/items
Server-->Client: HTTP 200 OK
Server-->Client: [ { id: 1, name: "Item 1" }, { id: 2, name: "Item 2" } ]

Client->Server: POST /api/items
Server-->Client: HTTP 201 Created
Server-->Client: { id: 3, name: "Item 3" }

Client->Server: PUT /api/items/3
Server-->Client: HTTP 204 No Content

Client->Server: DELETE /api/items/2
Server-->Client: HTTP 204 No Content

```  
####Advantage 

- simple to implement
- platform independence

####Disadvantage

- lack of real-time communication
- requires additional data such as headers 

##  WebSocket

```seq
participant Client
participant Server

Client->Server: WebSocket handshake request
Server-->Client: WebSocket handshake response

Client->Server: WebSocket message
Server-->Client: WebSocket message

Client->Server: WebSocket message
Server-->Client: WebSocket message

Client->Server: WebSocket close request
Server-->Client: WebSocket close response

```

####Advantage 

- real-time communication
- bi-directional communication

####Disadvantage

- complexer than REST
- lack of scalability 

##  Message Queueing
```seq
participant Sender
participant Queue
participant Receiver

Sender->Queue: Message 1
Queue->Receiver: Message 1
Receiver-->Queue: Acknowledgement 1
Queue-->Sender: Acknowledgement 1

Sender->Queue: Message 2
Queue->Receiver: Message 2
Receiver-->Queue: Acknowledgement 2
Queue-->Sender: Acknowledgement 2
```
####Advantage 

- asynchronous processing
- scalability 

####Disadvantage

- complex to implement 
- costly in cloud-based archticture

##  gRPC
```seq

participant Client
participant Server

Client->Server: CreateChannel()
Client->Server: CreateMessage(message)
Server->Client: SendAck()
Server->Client: ProcessMessage(message)
Server->Client: SendResponse()
Client->Server: CloseChannel()
```
####Advantage 

- asynchronous processing
- high performance 

####Disadvantage

- challenging to implement

## Conclusion:
As real-time cimmunication is not a critical requirement for our project, WebSocket may not be the most suitable option. Similarly, due to its complexity, gRPC may not be the best fit either.

Instead, I suggest that we keep it simple by using REST API initially. As we progress with testing and deployment, we can explore other options such as message queuing if we encounter any bottlenecks that require more advanced communication capabilities.

