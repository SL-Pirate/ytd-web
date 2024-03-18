import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/models/downloadable.dart';
import 'package:simple_circular_progress_bar/simple_circular_progress_bar.dart';

// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

class DownloadingButtonPlatform extends StatefulWidget {
  final Future<Downloadable?> Function() getDownloadable;
  final double? loadingBarSize;
  const DownloadingButtonPlatform({
    super.key,
    required this.getDownloadable,
    this.loadingBarSize,
  });

  @override
  State<DownloadingButtonPlatform> createState() => _DownloadingButtonState();
}

class _DownloadingButtonState extends State<DownloadingButtonPlatform> {
  bool isDownloading = false;
  late final Widget downloadLabel;
  late Widget downloadButtonIcon;

  @override
  void initState() {
    downloadLabel = Center(
      child: IconButton(
        onPressed: download,
        icon: const Icon(Icons.download),
        style: Styles.buttonStyle,
      ),
    );
    downloadButtonIcon = downloadLabel;

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return downloadButtonIcon;
  }

  void showFailureSnackBar(context) {
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Row(
      children: [
        Container(
          decoration: BoxDecoration(
              color: Styles.secondary,
              borderRadius: BorderRadius.circular(100)),
          child: const Icon(
            Icons.close,
            color: Styles.secondary,
          ),
        ),
        const SizedBox(
          width: 10,
        ),
        const Text("Download Failed",
            style: TextStyle(
                color: Styles.textColor,
                fontSize: 12,
                fontFamily: Styles.fontFamily))
      ],
    )));
  }

  Future<void> download() async {
    if (!isDownloading) {
      isDownloading = true;
      ValueNotifier<double> progressBar = ValueNotifier(0);
      setState(() {
        downloadButtonIcon = SizedBox(
          child: SimpleCircularProgressBar(
            size: widget.loadingBarSize ?? 100,
            valueNotifier: progressBar,
          ),
        );
      });

      Downloadable? downloadable = await widget.getDownloadable();
      if (downloadable != null) {
        final Response<dynamic> response = await Dio().get(
          downloadable.url,
          options: Options(responseType: ResponseType.bytes),
          onReceiveProgress: (received, total) {
            progressBar.value = received / total * 100;
          },
        );

        if (response.statusCode == 200) {
          final blob = html.Blob([Uint8List.fromList(response.data)]);

          final anchor = html.AnchorElement(
              href: html.Url.createObjectUrlFromBlob(blob))
            ..setAttribute('download', downloadable.name) // Set the filename
            ..click();

          html.Url.revokeObjectUrl(anchor.href!);
          if (!mounted) return;
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(
              content: Row(
            children: [
              Container(
                decoration: BoxDecoration(
                    border: Border.all(color: Styles.successColor, width: 2),
                    borderRadius: BorderRadius.circular(100)),
                child: const Icon(
                  Icons.check,
                  color: Styles.successColor,
                ),
              ),
              const SizedBox(
                width: 10,
              ),
              const Text("Downloaded Successfully",
                  style: TextStyle(
                      color: Styles.buttonTextColor,
                      fontSize: 12,
                      fontFamily: Styles.fontFamily))
            ],
          )));
          setState(() {
            downloadButtonIcon = downloadLabel;
          });
        }
      } else {
        if (!mounted) return;
        showFailureSnackBar(context);
        setState(() {
          downloadButtonIcon = downloadLabel;
        });
      }

      isDownloading = false;
    } else {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Expanded(
        child: Text(
          "Please be patient while the requested file is downloaded",
          maxLines: 2,
        ),
      )));
    }
  }
}
