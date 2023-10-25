# platform level dependancies
- ffmpeg
- redis
    - A redis server should be connected to handle the cache cleaning process with celery
    - configure this in server.cfg


# deploy command
```bash
    export csrf="<it is highly recommended that you put your own secret here>"
    celery -A ytd_web_core worker
    gunicorn ytd_web.wsgi --timeout 600 -b 0.0.0.0:8000
```