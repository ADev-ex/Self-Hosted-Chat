## Usage

### 1. Install dependencies

Make sure you have Python 3 installed.

Install the required libraries:

pip install -r requirements.txt
### 2. Start the server

The host has to run the server first:

python server.py

The server will start listening for incoming connections.

If you want people outside your local network to connect, you need to:

Open the required port on your router/internet box
Enable port forwarding
Share your public IP address with the clients
### 3. Configure the client

Open client.py and change:

SERVER_IP = "YOUR_SERVER_IP"
PORT = 5000

Replace YOUR_SERVER_IP with the public IP address of the computer hosting the server.

Example:

SERVER_IP = "88.177.2.4"
PORT = 5000
### 4. Connect to the chat

Run the client:

python client.py

Enter your username when prompted.

You can now send messages in real time.

### 5. Commands

Available command:

/quit

Disconnects from the chat server.

Network notes
The server must stay running while clients are connected.
The server's port must be open and forwarded on the host's router.
Clients only need the server's public IP address and port.