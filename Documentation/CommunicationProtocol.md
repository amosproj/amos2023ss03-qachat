# Communication Protocols 
##  REST API
REST API (Representational State Transfer Application Programming Interface) is a software architectural style that defines a set of constraints for creating web services. It is commonly used to build web services that are lightweight, maintainable, and scalable. REST APIs rely on HTTP methods such as GET, POST, PUT, and DELETE to interact with resources and allow clients to retrieve, create, update, and delete data. The simplicity of the REST architecture makes it easy to develop and integrate with other applications and services, making it a popular choice for building web-based systems and APIs.

<img width="444" alt="image" src="https://github.com/amosproj/amos2023ss03-qachat/assets/33463794/447c707c-3774-4a28-b90f-94e20025665d">

### Advantage 

- simple to implement
- platform independence

### Disadvantage

- lack of real-time communication
- requires additional data such as headers 

##  WebSocket

WebSocket is a communication protocol that enables real-time, bidirectional communication between a client and server over a single, long-lived connection. It allows for instant updates to be pushed from the server to the client without the client having to constantly poll the server for new data. WebSocket is commonly used in web applications that require real-time updates, such as online gaming and financial trading platforms.

<img width="344" alt="image" src="https://github.com/amosproj/amos2023ss03-qachat/assets/33463794/90cc8e71-89ca-4fc0-8ab9-041abf6d75b3">

### Advantage 

- real-time communication
- bi-directional communication

### Disadvantage

- complexer than REST
- lack of scalability 

##  Message Queueing
Message Queuing is a communication pattern where messages are sent asynchronously between systems through a message broker. The sender of the message does not wait for a response from the receiver and can continue with other tasks, allowing for asynchronous processing. The message broker acts as an intermediary, ensuring reliable delivery and message ordering. This communication pattern is commonly used in distributed systems and microservices architectures to decouple components and improve scalability.

<img width="444" alt="image" src="https://github.com/amosproj/amos2023ss03-qachat/assets/33463794/4fe04ed1-75cc-4f73-af23-ab141d15ece1">

### Advantage 

- asynchronous processing
- scalability 

### Disadvantage

- complex to implement 
- costly in cloud-based archticture

##  gRPC
gRPC is a high-performance, open-source, and platform-neutral Remote Procedure Call (RPC) framework that enables efficient communication between microservices. It uses Protocol Buffers as the default interface definition language, which allows for efficient data serialization and deserialization. gRPC supports multiple programming languages and provides features like bidirectional streaming, flow control, and error handling, making it suitable for high-throughput and low-latency applications.

<img width="301" alt="image" src="https://github.com/amosproj/amos2023ss03-qachat/assets/33463794/c46686bd-0bcc-4c99-bfa2-71632bd5398a">


### Advantage 

- asynchronous processing
- high performance 

### Disadvantage

- challenging to implement

## Conclusion:
As real-time cimmunication is not a critical requirement for our project, WebSocket may not be the most suitable option. Similarly, due to its complexity, gRPC may not be the best fit either.

Instead, I suggest that we keep it simple by using REST API initially. As we progress with testing and deployment, we can explore other options such as message queuing if we encounter any bottlenecks that require more advanced communication capabilities.

