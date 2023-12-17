import 'package:flutter/foundation.dart';
import 'package:ytd_web/util/constants.dart';

class Downloadable {
  final String url;
  final String quality;
  final DownloadType type;
  final String name;

  Downloadable({
    required this.url,
    required this.quality,
    required this.type,
    required this.name
  });

  /// Converts a [Downloadable] to a JSON object
  /// json keys:
  ///  - downloadable_link
  ///  - quality
  ///  - type
  ///  - file_name
  Downloadable.fromJson(Map<String, dynamic> json)
      : url = json['downloadable_link'],
        quality = json['quality'],
        type = DownloadType.values.firstWhere(
                (element) => element.name == json['type']
        ),
        name = json['file_name'];

  static Downloadable? getDownloadableFromList({
    required List<Downloadable> downloadables,
    required DownloadType type,
    String? quality,
    List<String> blacklistQualities = const []
  }) {
    for (Downloadable downloadable in downloadables) {
      if (downloadable.type == type && (quality == null || downloadable.quality == quality)) {
        if (kDebugMode) {
          print("Quality: ${downloadable.quality}");
        }
        if (blacklistQualities.contains(downloadable.quality)) {
          continue;
        }

        return downloadable;
      }
    }

    if (kDebugMode) {
      print("Downloadable: null");
    }
    return null;
  }
}
