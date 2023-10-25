import 'package:background_downloader/background_downloader.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:simple_circular_progress_bar/simple_circular_progress_bar.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';

class DownloadingButtonPlatform extends StatefulWidget {
  final Map<String, String> downloadable;
  final SearchResultModel searchResult;
  final Map<String, String> quality;
  const DownloadingButtonPlatform({
    super.key,
    required this.downloadable,
    required this.searchResult,
    required this.quality
  });

  @override
  State<DownloadingButtonPlatform> createState() => _DownloadingButtionState();
}

class _DownloadingButtionState extends State<DownloadingButtonPlatform> {
  bool isDownloading = false;
  Widget downloadButtonIcon = const Icon(Icons.download, color: Colors.green,);

  @override
  Widget build(BuildContext context) {
    return IconButton(
        iconSize: 69,
        color: Colors.red,
        icon: downloadButtonIcon,
        onPressed: () async {
          if (!isDownloading) {
            isDownloading = true;
            ValueNotifier<double> progressBar = ValueNotifier(0);
            setState(() {
              downloadButtonIcon = SimpleCircularProgressBar(
                valueNotifier: progressBar,
              );
            });
            if (widget.downloadable["link"] == null) {
              Response<dynamic> fileResponse = await Api.instance.getVideo(
                widget.searchResult.videoId,
                widget.quality["currentQuality"]!
              );
              if (fileResponse.statusCode != 404) {
                widget.downloadable["link"] =
                fileResponse.data["downloadable_link"];
                widget.downloadable["name"] = fileResponse.data["file_name"];
              }
            }
            if (widget.downloadable["link"] != null) {
              final task = DownloadTask(
                url: widget.downloadable["link"]!,
                filename: widget.downloadable["name"]!,
                updates: Updates.statusAndProgress,
                allowPause: true,
              );

              final result = await FileDownloader().download(
                task,
                onProgress: (progress) {
                  progressBar.value = progress * 100;
                },
              );

              switch (result.status) {
                case TaskStatus.complete:
                  (() async {
                    final newFilePath = await FileDownloader().moveToSharedStorage(task, SharedStorage.downloads);
                    if (newFilePath == null) {
                      // handle error
                    } else {
                      if (!mounted) return;
                      ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text("Successfully downloaded file to $newFilePath"))
                      );
                    }
                    setState(() {
                      downloadButtonIcon = const Icon(Icons.done, color: Colors.green,);
                    });
                  }) ();

                case TaskStatus.canceled:
                  setState(() {
                    downloadButtonIcon = const Icon(Icons.close, color: Colors.red,);
                  });

              // case TaskStatus.paused:
              //   print('Download was paused');

                default:
                  setState(() {
                    downloadButtonIcon = const Icon(Icons.close, color: Colors.red,);
                  });
              }
            }
            else {
              setState(() {
                downloadButtonIcon = const Icon(Icons.close, color: Colors.red,);
              });
              if (!mounted) return;
              showDialog(
                  context: context,
                  builder: (context) => const AlertDialog(
                    content: Text("Video unavailable!"),
                  )
              );
            }
            isDownloading = false;
          }
          else {
            ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                    content: Text(
                        "Please be patient while the requested file is downloaded"
                    )
                )
            );
          }
        }
    );
  }
}
