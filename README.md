# YTD Web

## A simple website that allows people to download youtube videos made with flask 

### Try it live 
[ytd-web](https://ytd-web.onrender.com/)

## Screenshots
![homepage](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss1.png)
![video search page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss5.png)
![video description page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss2.png)

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
- rename `secrets.key.example` to `secrets.key` and add your Google Api key which has YouTube data api enabled
#### install dependancies using pip
`pip install flask pytube requests`

#### installing ffmpeg
 - Installation process of ffmpeg may vary depending on your operating system
 - for more information visit [downloads page of ffmpeg's official site](https://ffmpeg.org/download.html)

#### Start the server with
```bash
python ./main.py
```

- site will be loaded on localhost:5000
