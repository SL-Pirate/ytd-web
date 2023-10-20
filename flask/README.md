# YTD Web

## A simple website that allows people to download youtube videos made with flask 

### Try it live 
[ytd-web](https://ytd-web.onrender.com/)

## Screenshots
![homepage](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss1.png)
![video search page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss5.png)
![video description page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss2.png)
![login page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss6.png)
![dashboard](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss7.png)

### dependancies 
- flask
- pytube
- requests
- ffmpeg

### Setup instructions on a development server
#### Clone the project to local server
```bash
git clone https://github.com/SL-Pirate/ytd-web.git
cd ytd-web
```
#### Configurarion
- Open `server.cfg` and edit
  - max_vids
  - keep_time
  #### Set
  - main_server_root
  - api_server_root
  To the address of your host.

  For example if you have hosted your app on "www.example.com",  you should set these values to "https://www.example.com"
  - Both the server root and api root should set to the same host unless this is an API only host
- rename `secrets.key.example` to `secrets.key` and add your Google Api key which has YouTube data api enabled

#### Setting up environment variables
- The server uses a pepper to encrypt passwords stored in the DB for security reasons
- So you have to set the environment variable of your host "pepper" to any value (preferably a strong and complicated one).
- Failing to do so will crash the server when trying to manipulate users.

#### install dependancies using pip
`pip install -r requirements.txt`

#### installing ffmpeg
 - Installation process of ffmpeg may vary depending on your operating system
 - for more information visit [downloads page of ffmpeg's official site](https://ffmpeg.org/download.html)

#### Start the server with
```bash
python ./main.py
```

- site will be loaded on localhost:5000
