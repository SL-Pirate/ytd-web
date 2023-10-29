# Project YTD - frontend
This is the frontend for the project YTD which is an Open Source Youtube Video Downloader.

## Build instructions
- Build the project with the following command
```bash
flutter build <your platform> --release --dart-define="token=<session token from the .env file of your ytd-web server>" --dart-define="baseUrl=<server url/ip address>:<port>/api/v1"
```

### Available Platforms
- Web Application: `web`
- Android: `apk`
- Windows: `windows`

### Other platforms
- This project also can be built for other platforms such as mac os and IOS
- But since I don't own a device myself I haven't configured and tested the project for them
- But if you are interested in building for those platforms, this project is open for contributions
