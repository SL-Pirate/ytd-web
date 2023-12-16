import 'package:flutter/material.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/util/constants.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/square_icon_button.dart';

class DownloadSection extends StatefulWidget {
  final String videoId;
  final ValueNotifier<String> videoResolution;
  final void Function(DownloadType type, String quality) onDownload;
  const DownloadSection({
    super.key,
    required this.videoId,
    required this.videoResolution,
    required this.onDownload
  });

  @override
  State<DownloadSection> createState() => _DownloadSectionState();
}

class _DownloadSectionState extends State<DownloadSection> {
  DownloadType type = DownloadType.video;
  String audioQuality = "128kbps";

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: Api.instance.getQualities(
            widget.videoId
        ),
        builder: (context, snapshot) {
          if (!snapshot.hasData) {
            return const CircularProgressIndicator();
          }

          return Column(
            children: [
              SizedBox(
                width: double.infinity,
                child: Text(
                  (type == DownloadType.video)
                      ? "Resolution"
                      : "Bitrate",
                  style: const TextStyle(
                      fontSize: 15,
                      fontFamily: Styles.fontFamily,
                      color: Styles.white
                  ),
                ),
              ),
              const SizedBox(height: 21,),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Container(
                      margin: const EdgeInsets.only(right: 22),
                      padding: const EdgeInsets.only(left: 15),
                      decoration: BoxDecoration(
                          color: Styles.white,
                          borderRadius: BorderRadius.circular(4)
                      ),
                      child: DropdownButton(
                        value: type == DownloadType.video
                            ? widget.videoResolution.value : audioQuality,
                        isExpanded: true,
                        style: const TextStyle(
                            color: Styles.black,
                            fontSize: 12,
                            fontFamily: Styles.fontFamily
                        ),
                        underline: const SizedBox(),
                        items: () {
                          List<DropdownMenuItem> entries = [
                            for (var quality in snapshot.data[
                            type == DownloadType.video
                                ? "video_qualities" : "audio_qualities"
                            ]) DropdownMenuItem(
                              value: quality,
                              child: Text(quality),
                            )
                          ];
                          entries.sort((a, b) {
                            int? aQuality = int.tryParse(a.value.replaceAll(RegExp(r'(p|kbps)$'), ''));
                            int? bQuality = int.tryParse(b.value.replaceAll(RegExp(r'(p|kbps)$'), ''));

                            if (aQuality == null || bQuality == null) {
                              return 0;
                            }
                            else {
                              return aQuality.compareTo(bQuality);
                            }
                          });

                          return entries;
                        } (),
                        onChanged: (selection) {
                          if (type == DownloadType.video) {
                            widget.videoResolution.value = selection;
                          }
                          else {
                            audioQuality = selection;
                          }

                          // // preventing sending requests when usr has not requested a video
                          // widget.onDownload(type, selection);
                        },
                      ),
                    ),
                  ),
                  Row(
                      children: [
                        SquareIconButton(
                          color: type == DownloadType.video
                              ? Styles.red : Styles.white,
                          icon: Icon(
                            Icons.videocam,
                            color: type == DownloadType.video
                                ? Styles.white : Styles.black,
                          ),
                          onPressed: () {
                            setState(() {
                              type = DownloadType.video;
                            });
                          },
                        ),
                        const SizedBox(width: 6,),
                        SquareIconButton(
                          color: type == DownloadType.audio
                              ? Styles.red : Styles.white,
                          icon: Icon(
                            Icons.music_note,
                            color: type == DownloadType.audio
                                ? Styles.white : Styles.black,
                          ),
                          onPressed: () {
                            ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                    content: Text(
                                        "Audio download is not available yet!"
                                    )
                                )
                            );
                            // setState(() {
                            //   type = DownloadType.audio;
                            // });
                          },
                        )
                      ]
                  )
                ],
              )
            ],
          );
        }
    );
  }
}
