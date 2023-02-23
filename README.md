# YTD Web

## A simple website that allows people to download youtube videos made with flask 

## Screenshots
![homepage](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss1.png)
![video description page](https://raw.githubusercontent.com/SL-Pirate/ytd-web/main/screenshots/ss2.png)

### dependancies 
- flask
- pytube
- ffmpeg

### Setup instructions on a development server
```bash
git clone https://github.com/SL-Pirate/ytd-web.git
cd ytd-web
python ./ytd.py
```

- open up a browser and go to 192.168.8.150:5000

### Configurarion
- Open ```ytd.py``` and edit
  - max_vids
  - keep_time