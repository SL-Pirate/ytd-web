import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:ytd_web/components/download_section.dart';
import 'package:ytd_web/modals/downloadable.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:dio/dio.dart';
import 'package:ytd_web/util/constants.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/components/channel_label.dart';
import 'package:ytd_web/widgets/download_button/download_button.dart';

class VideoScreen extends StatefulWidget {
  final SearchResultModel searchResult;
  const VideoScreen({super.key, required this.searchResult});

  @override
  State<VideoScreen> createState() => _VideoScreenState();
}

class _VideoScreenState extends State<VideoScreen> {
  static const double playerMaxWidth = 640;
  final ValueNotifier<String> videoResolution = ValueNotifier("360p");
  final ValueNotifier<String> audioBitRate = ValueNotifier("128kbps");
  final ValueNotifier<DownloadType> type = ValueNotifier(DownloadType.video);
  final List<Downloadable> downloadables = [];
  final Player videoPlayer = Player();
  late final VideoController controller;
  Widget? preview;
  Widget startPlayerIndicator = const Icon(
    Icons.play_circle, color: Colors.white70,
    size: 69,
  );

  @override
  void initState() {
    controller = VideoController(videoPlayer);
    super.initState();
  }

  @override
  void dispose() {
    videoPlayer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: SingleChildScrollView(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          width: double.infinity,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(
                height: 100,
              ),
              Wrap(
                alignment: WrapAlignment.spaceEvenly,
                children: [
                  Container(
                    constraints: const BoxConstraints(
                        maxWidth: playerMaxWidth
                    ),
                    child: Column(
                      children: [
                        preview ?? GestureDetector(
                            child: Container(
                                color: Colors.black,
                                child: FutureBuilder(
                                  future: widget.searchResult.thumbnail,
                                  builder: (context, snapshot) {
                                    if (snapshot.hasData) {
                                      return SizedBox(
                                          width: double.infinity,
                                          child: Stack(
                                            alignment: Alignment.center,
                                            children: [
                                              snapshot.data!,
                                              Center(
                                                child: startPlayerIndicator,
                                              )
                                            ],
                                          )
                                      );
                                    }
                                    else {
                                      return const Center(
                                        child: CircularProgressIndicator(),
                                      );
                                    }
                                  },
                                )
                            ),
                            onTap: () async {
                              setState(() {
                                startPlayerIndicator = const CircularProgressIndicator();
                              });
                              Downloadable? match = Downloadable.getDownloadableFromList(
                                  downloadables: downloadables,
                                  type: type.value,
                                  blacklistQualities: ["144p", "240p"]
                              );

                              if (match == null) {
                                final Response<dynamic> fileResponse = await Api.instance.getVideo(
                                    widget.searchResult.videoId,
                                    () {
                                      // Ignoring 144p and 240p because they tend to cause errors with the player
                                      // and its also not practical to show preview of such low quality
                                      if (videoResolution.value == "144p" || videoResolution.value == "240p") {
                                        return "360p";
                                      }

                                      return videoResolution.value;
                                    } ()
                                );
                                if (fileResponse.statusCode != 404) {
                                  final String url = fileResponse.data["downloadable_link"];
                                  downloadables.add(Downloadable(
                                      url: url,
                                      type: DownloadType.video,
                                      quality: () {
                                        // Applying the correct quality to the downloadable
                                        // Because it 144p and 240p were replaced with 360p above
                                        if (videoResolution.value == "144p" || videoResolution.value == "240p") {
                                          return "360p";
                                        }

                                        return videoResolution.value;
                                      } (),
                                      name: fileResponse.data["file_name"]
                                  ));
                                  setupPlayer(url);
                                }
                              }
                            }
                        ),
                        const SizedBox(height: 30,),
                        SizedBox(
                          width: double.infinity,
                          child: Text(
                            widget.searchResult.title,
                            style: TextStyle(
                                fontSize: Styles.of(context).subtitleFontSize,
                                fontWeight: FontWeight.bold,
                                fontFamily: Styles.fontFamily,
                                color: Styles.white
                            ),
                          ),
                        ),
                        SizedBox(height: Styles.of(context).isMobile ? 15 : 20),
                        ChannelLabel(searchResultModel: widget.searchResult),
                        const SizedBox(height: 50,),
                      ],
                    ),
                  ),
                  Container(
                    width: playerMaxWidth,
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 50
                    ),
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(15),
                        border: Border.all(
                            color: Colors.red,
                            width: 1
                        )
                    ),
                    child: Column(
                      children: [
                        DownloadSection(
                          videoId: widget.searchResult.videoId,
                          videoResolution: videoResolution,
                          audioBitRate: audioBitRate,
                          type: type,
                          onDownload: (type, quality) {},
                        ),
                        const SizedBox(height: 30,),
                        DownloadButton(
                          getDownloadable: () async {
                            Downloadable? downloadable = Downloadable.getDownloadableFromList(
                                downloadables: downloadables,
                                type: type.value,
                                quality: type.value == DownloadType.video
                                    ? videoResolution.value
                                    : audioBitRate.value
                            );
                            if (downloadable != null) {
                              return downloadable;
                            }
                            if (type.value == DownloadType.video) {
                              dynamic video = (await Api.instance.getVideo(
                                  widget.searchResult.videoId,
                                  videoResolution.value
                              )).data;

                              video["type"] = type.value.name;
                              video["quality"] = videoResolution.value;
                              Downloadable downloadable = Downloadable.fromJson(video);
                              downloadables.add(downloadable);

                              return downloadable;
                            }
                            else {
                              dynamic audio = (await Api.instance.getAudio(
                                  widget.searchResult.videoId,
                                  audioBitRate.value
                              )).data;

                              audio["type"] = type.value.name;
                              audio["quality"] = audioBitRate.value;
                              Downloadable downloadable = Downloadable.fromJson(audio);
                              downloadables.add(downloadable);

                              return downloadable;
                            }
                          },
                        )
                      ],
                    ),
                  )
                ],
              ),
              const SizedBox(height: 50,),
            ],
          ),
        ),
      ),
    );
  }

  Stream<int> uInt8ListToStreamInt(Stream<Uint8List> uInt8ListStream) async* {
    await for (final Uint8List chunk in uInt8ListStream) {
      for (final int byte in chunk) {
        yield byte;
      }
    }
  }

  void setupPlayer(String src) {
    videoPlayer.open(Media(src));
    setState(() {
      preview = AspectRatio(
        aspectRatio: 16/9,
        child: Container(
            constraints: const BoxConstraints(
              maxWidth: playerMaxWidth,
            ),
            child: Video(controller: controller,)
        ),
      );
    });
  }
}
