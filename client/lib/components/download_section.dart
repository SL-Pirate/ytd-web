import 'package:flutter/material.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/util/constants.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/square_icon_button.dart';

class DownloadSection extends StatefulWidget {
  final String videoId;
  final ValueNotifier<String> videoResolution;
  final ValueNotifier<String> audioBitRate;
  final ValueNotifier<DownloadType> type;
  final void Function(DownloadType type, String quality) onDownload;
  const DownloadSection({
    super.key,
    required this.videoId,
    required this.videoResolution,
    required this.audioBitRate,
    required this.type,
    required this.onDownload
  });

  @override
  State<DownloadSection> createState() => _DownloadSectionState();
}

class _DownloadSectionState extends State<DownloadSection> {
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
                  "Select ${
                      (widget.type.value == DownloadType.video)
                          ? "Resolution"
                          : "Bitrate"
                  }",
                  style: TextStyle(
                      fontSize: Styles.of(context).subtitleFontSize,
                      fontFamily: Styles.fontFamily,
                      fontWeight: FontWeight.bold,
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
                      height: 40,
                      margin: const EdgeInsets.only(right: 22),
                      padding: const EdgeInsets.only(left: 15),
                      decoration: BoxDecoration(
                          color: Styles.white,
                          borderRadius: BorderRadius.circular(4)
                      ),
                      child: DropdownButton(
                        value: widget.type.value == DownloadType.video
                            ? widget.videoResolution.value : widget.audioBitRate.value,
                        isExpanded: true,
                        style: TextStyle(
                            color: Styles.black,
                            fontSize: Styles.of(context).bodyFontSize,
                            fontFamily: Styles.fontFamily
                        ),
                        icon: const Padding(
                          padding: EdgeInsets.only(right: 8.0),
                          child: Icon(Icons.arrow_drop_down),
                        ),
                        underline: const SizedBox(),
                        items: () {
                          List<DropdownMenuItem> entries = [
                            for (var quality in snapshot.data[
                            widget.type.value == DownloadType.video
                                ? "video_qualities" : "audio_qualities"
                            ]) DropdownMenuItem(
                              value: quality,
                              child: Text(quality),
                            )
                          ];
                          entries.sort((a, b) {
                            int? aQuality = int.tryParse(
                                a.value.replaceAll(RegExp(r'(p|kbps)$'), '')
                            );
                            int? bQuality = int.tryParse(
                                b.value.replaceAll(RegExp(r'(p|kbps)$'), '')
                            );

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
                          setState(() {
                            if (widget.type.value == DownloadType.video) {
                              widget.videoResolution.value = selection;
                            }
                            else {
                              widget.audioBitRate.value = selection;
                            }
                          });
                        },
                      ),
                    ),
                  ),
                  Row(
                      children: [
                        SquareIconButton(
                          color: widget.type.value == DownloadType.video
                              ? Styles.red : Styles.white,
                          icon: Icon(
                            Icons.videocam,
                            color: widget.type.value == DownloadType.video
                                ? Styles.white : Styles.black,
                          ),
                          onPressed: () {
                            setState(() {
                              widget.type.value = DownloadType.video;
                            });
                          },
                        ),
                        const SizedBox(width: 6,),
                        SquareIconButton(
                          color: widget.type.value == DownloadType.audio
                              ? Styles.red : Styles.white,
                          icon: Icon(
                            Icons.music_note,
                            color: widget.type.value == DownloadType.audio
                                ? Styles.white : Styles.black,
                          ),
                          onPressed: () {
                            setState(() {
                              widget.type.value = DownloadType.audio;
                            });
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
