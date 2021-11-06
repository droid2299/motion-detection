# Motion Detection API

A motion detection API which uses Flask for a client-server based architecture. The server takes an image as input and stores a buffer, if there is a change in the consecutive frame (motion is present), it will return a JSON containing the frame number and whether or not motion is present. The client reads an input video and sends each frame to the server and reads the output given by the server.


## Installation & Usage:
### Dependencies:
```sh
pip install -r requirements.txt
```
### Usage:
##### For Server:
For each client that will be served by this server, a deque has to initialized of length = 2.
**Example:** If server is already serving 2 clients and another client has to be added then, 
```sh
list_images3 = deque(maxlen = 2)
```
And an elif loop has to added for the corresponding deque, like:
```sh
elif(r.args.get('value') == '3'):
        list_images3.append(img)
        motion_indicator = image_motion.detector(list_images3 , r.args.get('value'))
```
Once the server file is edited according to the number of clients, run:
```sh
python server.py
```
##### For Client:

For each client, change the path to the input video and also change the ***value in the test_url*** variable according to the number of clients.
**Example:** If server is already serving 2 clients and another client has to be added then, 
```sh
test_url = addr + '/api/test?value=3'
```
Once the variable is changed according to the number of clients, run:
```sh
python client.py
```
***Note:*** Each new client should be in a new .py file. 

