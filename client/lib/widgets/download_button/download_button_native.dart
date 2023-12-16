import 'package:background_downloader/background_downloader.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:simple_circular_progress_bar/simple_circular_progress_bar.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/util/styles.dart';

class DownloadingButtonPlatform extends StatefulWidget {
  final Map<String, String> downloadable;
  final SearchResultModel searchResult;
  final ValueNotifier quality;
  const DownloadingButtonPlatform({
    super.key,
    required this.downloadable,
    required this.searchResult,
    required this.quality
  });

  @override
  State<DownloadingButtonPlatform> createState() => _DownloadingButtonState();
}

class _DownloadingButtonState extends State<DownloadingButtonPlatform> {
  bool isDownloading = false;
  static const downloadLabel = Text(
      "Download",
      style: TextStyle(
          fontSize: 12,
          fontFamily: Styles.fontFamily,
          fontWeight: FontWeight.bold,
          color: Colors.white
      )
  );
  late Widget downloadButtonIcon;

  @override
  void initState() {
    downloadButtonIcon = downloadLabel;

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () async {
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
                widget.quality.value!
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
                  if (!context.mounted) return;
                  ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                          content: Row(
                            children: [
                              Container(
                                decoration: BoxDecoration(
                                    border: Border.all(
                                        color: Styles.green,
                                        width: 2
                                    ),
                                    borderRadius: BorderRadius.circular(100)
                                ),
                                child: const Icon(
                                  Icons.check,
                                  color: Styles.green,
                                ),
                              ),
                              const SizedBox(width: 10,),
                              const Text(
                                  "Downloaded Successfully",
                                  style: TextStyle(
                                      color: Styles.white,
                                      fontSize: 12,
                                      fontFamily: Styles.fontFamily
                                  )
                              )
                            ],
                          )
                      )
                  );
                  setState(() {
                    downloadButtonIcon = downloadLabel;
                  });
                }) ();

              case TaskStatus.canceled:
                if (!context.mounted) return;
                showFailureSnackBar(context);
                setState(() {
                  downloadButtonIcon = downloadLabel;
                });

              default:
                if (!context.mounted) return;
                showFailureSnackBar(context);
                setState(() {
                  downloadButtonIcon = downloadLabel;
                });
            }
          }
          else {
            if (!context.mounted) return;
            showFailureSnackBar(context);
            setState(() {
              downloadButtonIcon = const Icon(Icons.close, color: Colors.red,);
            });
            if (!mounted) return;
            ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text("Video unavailable!"))
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
      },
      child: Container(
        padding: const EdgeInsets.symmetric(
          horizontal: 29,
          vertical: 12,
        ),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(5),
          color: Styles.red,
        ),
        child: downloadButtonIcon,
      ),
    );
  }

  void showFailureSnackBar (context) {
    ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
            content: Row(
              children: [
                Container(
                  decoration: BoxDecoration(
                      color: Styles.red,
                      borderRadius: BorderRadius.circular(100)
                  ),
                  child: const Icon(
                    Icons.close,
                    color: Styles.red,
                  ),
                ),
                const SizedBox(width: 10,),
                const Text(
                    "Download Failed",
                    style: TextStyle(
                        color: Styles.white,
                        fontSize: 12,
                        fontFamily: Styles.fontFamily
                    )
                )
              ],
            )
        )
    );
  }
}
