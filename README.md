# YTD Web

## A simple website that allows people to download youtube videos made with flask 

## Screenshots
![homepage](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss1.png)
![video search page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss5.png)
![video description page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss2.png)

### dependancies 
- flask
- pytube
- requests
- ffmpeg

#### install dependancies using pip
`pip install flask pytube requests`

#### installing ffmpeg
 - Installation process of ffmpeg may vary depending on your operating system
 - for more information visit [downloads page of ffmpeg's official site](https://ffmpeg.org/download.html)

### Setup instructions on a development server
```bash
git clone https://github.com/SL-Pirate/ytd-web.git
cd ytd-web
`pip install flask pytube requests`
python ./main.py
```

- open up a browser and go to 192.168.8.150:5000

### Configurarion
- Open ```main.py``` and edit
  - max_vids
  - keep_time