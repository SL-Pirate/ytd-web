import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:media_kit/media_kit.dart';
import 'package:media_kit_video/media_kit_video.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:dio/dio.dart';
import 'package:ytd_web/widgets/download_button/download_button.dart';

class VideoScreen extends StatefulWidget {
  final SearchResultModel searchResult;
  const VideoScreen({super.key, required this.searchResult});

  @override
  State<VideoScreen> createState() => _VideoScreenState();
}

class _VideoScreenState extends State<VideoScreen> {
  Map<String, String> downloadable = {};
  Widget? preview;
  late Widget thumbnail;
  bool isDownloading = false;
  Widget downloadButtonIcon = const Icon(Icons.download, color: Colors.green,);
  final Player videoPlayer = Player();
  late final VideoController controller;
  Widget startPlayerIndicator = const Icon(
    Icons.play_circle, color: Colors.white70,
    size: 69,
  );
  List<DropdownMenuEntry> availableQualities = [];
  Map<String, String> quality = {"currentQuality": "360p"};
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
    thumbnail = Stack(
      children: [
        Center(
          child: ClipRect(
            child: FutureBuilder(
              future: Api.instance.getImage(widget.searchResult.thumbnailUrl),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Image.memory(snapshot.data);
                }
                else {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }
              },
            )
          ),
        ),
        Center(
          child: startPlayerIndicator,
        )
      ],
    );

    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          title: Center(
            child: Text(
              widget.searchResult.title,
              maxLines: 2,
            ),
          ),
          backgroundColor: Colors.blue,
        ),
        body: FutureBuilder(
          future: fetchQualities(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              if (availableQualities.isEmpty) {
                for (String q in snapshot.data["video_qualities"]) {
                  availableQualities.add(
                      DropdownMenuEntry(
                          value: q,
                          label: q
                      )
                  );
                }
              }
              return Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Center(
                    child: Container(
                      width: double.infinity,
                      padding: const EdgeInsets.symmetric(horizontal: 20),
                      child: DropdownMenu(
                        width: MediaQuery.of(context).size.width - 40,
                        hintText: "Select video resolution",
                        dropdownMenuEntries: availableQualities,
                        onSelected: (selection) {
                          quality["currentQuality"] = selection;
                          // preventing sending requests when usr has not requested a video
                          if (downloadable["link"] != null) {
                            Api.instance.getVideo(
                                widget.searchResult.videoId,
                                selection
                            ).then((value) {
                              downloadable["link"] = value.data["downloadable_link"];
                              videoPlayer.open(Media(downloadable["link"]!)).then((value) {
                                videoPlayer.play();
                              });
                            });
                          }
                        },
                      ),
                    ),
                  ),
                  SizedBox(
                    child: preview
                        ?? GestureDetector(
                            child: Container(
                                width: 500,
                                height: 250,
                                color: Colors.black,
                                child: thumbnail
                            ),
                            onTap: () async {
                              setState(() {
                                startPlayerIndicator = const CircularProgressIndicator();
                              });
                              if (downloadable["link"] == null) {
                                Response<dynamic> response = await Api.instance.getVideo(
                                    widget.searchResult.videoId,
                                    quality["currentQuality"]!
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
                  ),
                  Center(
                    child: Text(widget.searchResult.channelName),
                  ),
                  const SizedBox(
                    height: 100,
                    width: 100,
                  )
                ],
              );
            }
            else if (snapshot.hasError) {
              return const Center(
                child: Card(
                  elevation: 4.0,
                  margin: EdgeInsets.all(16.0),
                  child: Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Text(
                      'This video is unavailable!',
                      style: TextStyle(fontSize: 16.0),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
              );
            }
            else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          },
        ),
        floatingActionButton: DownloadButton(
          downloadable: downloadable,
          searchResult: widget.searchResult,
          quality: quality,
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      ),
    );
  }

  Stream<int> uint8ListToStreamInt(Stream<Uint8List> uint8ListStream) async* {
    await for (final Uint8List chunk in uint8ListStream) {
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
              maxWidth: 500,
              maxHeight: 300
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
