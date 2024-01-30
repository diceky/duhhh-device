# duhhh-device
IoT device prototyping tool for duhhh School.

### rest_server_socketio_client.py
This is the best option to go with so far. Acts as a REST API server in the local network to serve input values, while also sending the values to an external Socket IO server hosted on Heroku to broadcast to any other Socket IO client in the same room, like other duhhh devices or Adalo (via custom components).

### rest_server.py
Acts as a REST API server in the local network to serve input values.

### rest_client.py
Sends input values to a local REST API server.

### socketio_server.py
Acts as a Soceket IO server to relay data to other connected Socket IO clients.

### socketio_client.py
Sends input values to an external Socket IO server.

### flasksocketio_server.py
Acts as both REST API server and Soceket IO server to broadcast input data to other connected Socket IO clients.