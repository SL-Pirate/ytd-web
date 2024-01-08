import 'package:background_downloader/background_downloader.dart';
import 'package:flutter/material.dart';
import 'package:simple_circular_progress_bar/simple_circular_progress_bar.dart';
import 'package:ytd_web/models/downloadable.dart';
import 'package:ytd_web/util/styles.dart';

class DownloadingButtonPlatform extends StatefulWidget {
  final Future<Downloadable>? Function() getDownloadable;
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
        downloadButtonIcon = SimpleCircularProgressBar(
          size: widget.loadingBarSize ?? 100,
          valueNotifier: progressBar,
        );
      });
      Downloadable? downloadable = await widget.getDownloadable();
      if (downloadable != null) {
        final task = DownloadTask(
          url: downloadable.url,
          filename: downloadable.name,
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
              final newFilePath = await FileDownloader()
                  .moveToSharedStorage(task, SharedStorage.downloads);
              if (newFilePath == null) {
                // handle error
              } else {
                if (!mounted) return;
                ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                    content: Row(
                  children: [
                    Container(
                      decoration: BoxDecoration(
                          border:
                              Border.all(color: Styles.successColor, width: 2),
                          borderRadius: BorderRadius.circular(100)),
                      child: const Icon(
                        Icons.check,
                        color: Styles.color4,
                      ),
                    ),
                    const SizedBox(
                      width: 10,
                    ),
                    Expanded(
                      child: Text(
                        "File saved successfully to $newFilePath",
                        style: const TextStyle(
                            color: Styles.buttonTextColor,
                            fontSize: 12,
                            fontFamily: Styles.fontFamily),
                        maxLines: 2,
                      ),
                    )
                  ],
                )));
              }
              setState(() {
                downloadButtonIcon = downloadLabel;
              });
            })();

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
      } else {
        if (!context.mounted) return;
        showFailureSnackBar(context);
        setState(() {
          downloadButtonIcon = const Icon(
            Icons.close,
            color: Colors.red,
          );
        });
        if (!mounted) return;
        ScaffoldMessenger.of(context)
            .showSnackBar(const SnackBar(content: Text("Video unavailable!")));
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
