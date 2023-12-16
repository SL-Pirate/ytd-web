import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:ytd_web/components/download_section.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:dio/dio.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/channel_label.dart';
import 'package:ytd_web/widgets/download_button/download_button.dart';

class VideoScreen extends StatefulWidget {
  final SearchResultModel searchResult;
  const VideoScreen({super.key, required this.searchResult});

  @override
  State<VideoScreen> createState() => _VideoScreenState();
}

class _VideoScreenState extends State<VideoScreen> {
  static const double playerMaxWidth = 540;
  static const double playerMaxHeight = 304;
  final ValueNotifier<String> videoResolution = ValueNotifier("360p");
  final Map<String, String> downloadable = {};
  final Player videoPlayer = Player();
  late final VideoController controller;
  Widget? preview;
  bool isDownloading = false;
  Widget downloadButtonIcon = const Icon(Icons.download, color: Colors.green,);
  Widget startPlayerIndicator = const Icon(
    Icons.play_circle, color: Colors.white70,
    size: 69,
  );
  final List<DropdownMenuEntry> availableQualities = [];
  Future<dynamic>? qualityResponse;

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
                              if (downloadable["link"] == null) {
                                Response<dynamic> response = await Api.instance.getVideo(
                                    widget.searchResult.videoId,
                                    videoResolution.value
                                );
                                if (response.statusCode != 404) {
                                  downloadable["link"] = response.data["downloadable_link"];
                                  downloadable["name"] = response.data["file_name"];
                                  setupPlayer(downloadable["link"]!);
                                }
                                else {
                                  setState(() {
                                    startPlayerIndicator = const Icon(
                                      Icons.close,
                                      size: 69,
                                      color: Colors.red,
                                    );
                                  });
                                  if (!mounted) return;
                                  showDialog(
                                      context: context,
                                      builder: (context) => const AlertDialog(
                                        content: Text("Video unavailable!"),
                                      )
                                  );
                                }
                              }
                              else {
                                setupPlayer(downloadable["link"]!);
                              }
                            }
                        ),
                        const SizedBox(height: 30,),
                        SizedBox(
                          width: double.infinity,
                          child: Text(
                            widget.searchResult.title,
                            style: const TextStyle(
                                fontSize: 12,
                                fontWeight: FontWeight.bold,
                                fontFamily: Styles.fontFamily,
                                color: Styles.white
                            ),
                          ),
                        ),
                        const SizedBox(height: 15,),
                        ChannelLabel(searchResultModel: widget.searchResult),
                        const SizedBox(height: 50,),
                      ],
                    ),
                  ),
                  Container(
                    constraints: const BoxConstraints(
                      maxWidth: playerMaxWidth,
                    ),
                    padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 50
                    ),
                    decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(15),
                        border: Border.all(
                            color: Colors.red,
                            width: 2
                        )
                    ),
                    child: Column(
                      children: [
                        DownloadSection(
                          videoId: widget.searchResult.videoId,
                          videoResolution: videoResolution,
                          onDownload: (type, quality) {},
                        ),
                        const SizedBox(height: 30,),
                        DownloadButton(
                            downloadable: downloadable,
                            searchResult: widget.searchResult,
                            quality: videoResolution
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
      preview = Container(
          constraints: const BoxConstraints(
              maxWidth: playerMaxWidth,
              maxHeight: playerMaxHeight
          ),
          child: Video(controller: controller,)
      );
    });
  }

  Future<dynamic> fetchQualities() {
    qualityResponse ??= Api.instance.getQualities(
        widget.searchResult.videoId
    );

    return qualityResponse!;
  }
}
