# PyGame Networking
A simple game which displays the position of connected clients. Each client is able to move around the screen and 
have their postion sent to the server. Each client recieves the position of all the other connected clients and is able
to display those clients accordingly. This game uses the Transmission Control Protocol (TCP). This is a game purely created for me to practice Python and is not meant to be played
as a real game.

### Prerequisites



```
- PyGame (https://www.pygame.org/)
```

### Installing

1. Ensure PyGame is Installed
2. Run game.py

### Network Overview
1. server.py is opened, it binds to host "127.0.0.1" and port 5000
2. The server then listens for connections
3. If a connection is found, the server opens a new thread for the function clientThread. This thread handles data back
and forth between that client. The server continues to listen for more connections
4. The server then sends the client their ClientID with the message message: ["setID", "server", random.randint(100,999)]
5. The client then recieves this message and sets their ClientID to the number recieved
6. The client sends its player object to the server once per game loop
7. The server recieves this player object, and sends it to all connected clients
8. All clients then recieve this object and update the position for each player based on the data recieved
9. The client won't update their own player position, only the postion of other clients as this can cause the player to
appear as if they are "teleporting" if they have a high ping as their position won't be smooth

### Features



- Server and client connection
- Server recieves and sends data between the clients
- Each client has a "ClientID" which is used to differenciate between the player and other players


### Todo


- Remove instances where the server trusts the client. Currently the client could change their variables manually and the
server would update other clients with these new variables. For example the player could set their size to 1000x1000 pixels
and fill the screen. It would be better to have the server manage these variables and functions while the client
just sends over the player controls.
- When the ClientID is set by the server, the server should do a check to ensure that the ID doesn't already exists as this
can cause issues with multiple clients having the same ID.
- Implement a better system to handle high ping. Perhaps by using the players velocity to predict where they will have moved
to if they have a ping spike. Currently the player will be "teleporting" across other players screens as their position
won't be updated as often.
- Implement server side collision detection
- Allow the user  to enter the IP of the server they wish to connect to. Currently it's set to 127.0.0.1
- Remove a client if they disconnect. Currently they continue to be displayed
- Currently the client waits 1 second while connecting to the server. This is not a good idea as it's possible that
the client takes more than 1 second to connect. After that 1 second the program will try to run normally and will crash
as it is not yet connected to the server.
- Fix _pickle.UnpicklingError: invalid load key (Occurs randomly while clients are connected to the server, perhaps because
the data hasn't been sent properly when it tries to dump  it



## Authors

* **Camron W** - *Initial work* - [CamronW](https://github.com/CamronW)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


