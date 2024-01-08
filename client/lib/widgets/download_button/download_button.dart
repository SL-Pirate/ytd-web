import 'download_button_native.dart'
    if (dart.library.html) 'download_button_web.dart';

class DownloadButton extends DownloadingButtonPlatform {
  const DownloadButton({
    super.key,
    super.loadingBarSize,
    required super.getDownloadable,
  });
}
