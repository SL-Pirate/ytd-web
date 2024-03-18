import 'package:flutter/material.dart';

class Resolution {
  final List<String> videoResolutions;
  final List<String> audioResolutions;

  Resolution({
    required this.videoResolutions,
    required this.audioResolutions,
  });

  Resolution.fromJson(Map? map)
      : this(
          videoResolutions: List<String>.from(map?['video_qualities'] ?? []),
          audioResolutions: List<String>.from(map?['audio_qualities'] ?? []),
        );

  List<DropdownMenuItem<String>> get videoDropdownItems {
    if (videoResolutions.isEmpty) {
      return const [
        DropdownMenuItem(child: Text('No optional resolutions')),
      ];
    }

    return videoResolutions
        .map((e) => DropdownMenuItem<String>(
              value: e,
              child: Text(e),
            ))
        .toList();
  }

  List<DropdownMenuItem<String>> get audioDropdownItems {
    if (audioResolutions.isEmpty) {
      return const [
        DropdownMenuItem(child: Text('No optional resolutions')),
      ];
    }

    return audioResolutions
        .map((e) => DropdownMenuItem<String>(
              value: e,
              child: Text(e),
            ))
        .toList();
  }
}
