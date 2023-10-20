import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:simple_circular_progress_bar/simple_circular_progress_bar.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/modals/search_result_model.dart';
// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

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
  State<DownloadingButtonPlatform> createState() => _DownloadingButtonState();
}

class _DownloadingButtonState extends State<DownloadingButtonPlatform> {
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
              final Response<dynamic> response = await Dio().get(
                widget.downloadable["link"]!,
                options: Options(
                    responseType: ResponseType.bytes
                ),
                onReceiveProgress: (received, total) {
                  progressBar.value = received / total * 100;
                },
              );

              if (response.statusCode == 200) {
                final blob = html.Blob([Uint8List.fromList(response.data)]);

                final anchor = html.AnchorElement(href: html.Url.createObjectUrlFromBlob(blob))
                  ..setAttribute('download', widget.downloadable["name"]!) // Set the filename
                  ..click();

                html.Url.revokeObjectUrl(anchor.href!);
                setState(() {
                  downloadButtonIcon = const Icon(Icons.done, color: Colors.green,);
                });
              }
              else {
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
