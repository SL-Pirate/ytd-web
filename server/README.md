# ytd-web Server

This is the server for the ytd-web platform, a free and open-source YouTube video downloader. The server is responsible for handling video conversion and caching using ffmpeg and Redis, respectively.

## Environment setup
- Create a new python virtual environment with `python -m venv .venv` (Recommended)
- If you are running a UNIX OS activate the virtual environment in the current shell by running `source .venv/bin/activate`
- install the python dependancies with `pip install -r requirements.txt` 

### Setting up secrets in .env
The `sample.env` file contains sample environment variables that are required to run the application. You need to create a copy of this file as `.env` and set your own secrets in it.

#### Google API Key
The `googleApiKey` variable is used to store the Google API key. To set your own Google API key, replace `myGoogleApiKey` with your own key.
#### Session Key
The `mySecretKey` variable is used to store your session key. replace `mySecretKey` with a string of random characters of your preference. Longer the key is better. Recommended length is 32 characters.

## Configuration
The server configuration file can be found as `server.cfg` The configuration file contains the following variables:

- max_vids: The maximum number of videos that can exist on the server. This value should be adjusted according to the requirements and capabilities of the host machine.
- keep_time: The time duration (in minutes) that a particular downloadable video file is kept on the host system. This value should be set depending on the usage and disk space capabilities.
- cache_folder: The folder where cached files are stored.
- redis_connection: The link to the Redis server. This is required for Celery to clean caches.

Make sure to adjust these variables according to your requirements and capabilities.

## Dependencies

The following dependencies are required to run the server:

- ffmpeg: A platform-level dependency required for video conversion.
- redis: A platform-level dependency required for caching. A Redis server should be connected to handle the cache cleaning process with Celery. This can be configured in server.cfg.

## Deployment

To deploy the application, run the following commands in the terminal:

### Platform-level dependencies

Make sure the following dependencies are installed on your system:

- ffmpeg
- redis

A Redis server should be connected to handle the cache cleaning process with Celery. You can configure this in server.cfg.

### Deploy command

To start the server, run the following command in the terminal:

```bash
    export csrf="<it is highly recommended that you put your own secret here>";
    gunicorn ytd_web.wsgi --timeout 600 -b 0.0.0.0:8000 --workers 2
```

Open up a new terminal/cli instance and run the following command as it is required for cleaning caches
```bash
    celery -A ytd_web_core worker -l INFO
```

## API Documentation
- To refer the API Documentation, run the server and go to [https://localhost:8000/docs](https://localhost:8000/docs)

### TODO
#### goal - Implement ability to download from different sources other than youtube
- [x] Improvements to search API
- [ ] Improvements to thumbnail proxy
- [ ] Improvements to get video API
- [ ] Improvements to get audio API