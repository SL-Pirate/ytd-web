import 'package:flutter/material.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/util/constants.dart';
import 'package:ytd_web/util/styles.dart';

class DownloadSection extends StatefulWidget {
  final String url;
  final ValueNotifier<String?> videoResolution;
  final ValueNotifier<String?> audioBitRate;
  final ValueNotifier<DownloadType> type;
  final void Function(DownloadType type, String quality) onDownload;
  const DownloadSection({
    super.key,
    required this.url,
    required this.videoResolution,
    required this.audioBitRate,
    required this.type,
    required this.onDownload,
  });

  @override
  State<DownloadSection> createState() => _DownloadSectionState();
}

class _DownloadSectionState extends State<DownloadSection> {
  dynamic _futureData;

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: futureData,
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const CircularProgressIndicator();
        }
        widget.videoResolution.value ??= snapshot.data["video_qualities"][0];
        widget.audioBitRate.value ??= snapshot.data["audio_qualities"][0];

        return Column(
          children: [
            SizedBox(
              width: double.infinity,
              child: Text(
                "Select ${(widget.type.value == DownloadType.video) ? "Resolution" : "Bitrate"}",
                style: TextStyle(
                  fontSize: Styles.of(context).subtitleFontSize,
                  fontFamily: Styles.fontFamily,
                  fontWeight: FontWeight.bold,
                  color: Styles.textColor,
                ),
              ),
            ),
            const SizedBox(
              height: 21,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Container(
                    height: 40,
                    margin: const EdgeInsets.only(right: 22),
                    padding: const EdgeInsets.only(left: 15),
                    decoration: BoxDecoration(
                        color: Styles.backgroundColor,
                        borderRadius: BorderRadius.circular(4)),
                    child: DropdownButton<String>(
                      value: widget.type.value == DownloadType.video
                          ? widget.videoResolution.value
                          : widget.audioBitRate.value,
                      isExpanded: true,
                      style: TextStyle(
                          color: Styles.textColor,
                          fontSize: Styles.of(context).bodyFontSize,
                          fontFamily: Styles.fontFamily),
                      icon: const Padding(
                        padding: EdgeInsets.only(right: 8.0),
                        child: Icon(Icons.arrow_drop_down),
                      ),
                      underline: const SizedBox(),
                      items: [
                        for (var quality in snapshot.data[
                            widget.type.value == DownloadType.video
                                ? "video_qualities"
                                : "audio_qualities"])
                          DropdownMenuItem(
                            value: quality,
                            child: Text(quality),
                          )
                      ],
                      onChanged: (selection) {
                        setState(() {
                          if (widget.type.value == DownloadType.video) {
                            widget.videoResolution.value = selection;
                          } else {
                            widget.audioBitRate.value = selection;
                          }
                        });
                      },
                    ),
                  ),
                ),
                Row(children: [
                  Container(
                    decoration: BoxDecoration(
                      border: (widget.type.value != DownloadType.video)
                          ? Border.all(color: Styles.borderColor)
                          : null,
                      borderRadius: BorderRadius.circular(5),
                    ),
                    child: IconButton(
                      style: Styles.buildButtonStyle(
                        backgroundColor: widget.type.value == DownloadType.video
                            ? Styles.secondary
                            : Styles.backgroundColor,
                        foregroundColor: widget.type.value == DownloadType.video
                            ? Styles.backgroundColor
                            : Styles.textColor,
                      ),
                      icon: const Icon(
                        Icons.videocam,
                      ),
                      onPressed: () {
                        setState(() {
                          widget.type.value = DownloadType.video;
                        });
                      },
                    ),
                  ),
                  const SizedBox(
                    width: 6,
                  ),
                  Container(
                    decoration: BoxDecoration(
                        border: (widget.type.value != DownloadType.audio)
                            ? Border.all(color: Styles.borderColor)
                            : null,
                        borderRadius: BorderRadius.circular(5)),
                    child: IconButton(
                      style: Styles.buildButtonStyle(
                        backgroundColor: widget.type.value == DownloadType.audio
                            ? Styles.secondary
                            : Styles.backgroundColor,
                        foregroundColor: widget.type.value == DownloadType.audio
                            ? Styles.backgroundColor
                            : Styles.textColor,
                      ),
                      icon: const Icon(Icons.music_note),
                      onPressed: () {
                        setState(() {
                          widget.type.value = DownloadType.audio;
                        });
                      },
                    ),
                  )
                ])
              ],
            )
          ],
        );
      },
    );
  }

  Future<dynamic> get futureData async {
    return _futureData ??= await Api.instance.getQualities(widget.url);
  }
}
