import 'package:flutter/material.dart';
import 'package:ytd_web/api/api.dart';
import 'package:ytd_web/main.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/screens/base_frame.dart';
import 'package:ytd_web/screens/video_screen.dart';
import 'package:ytd_web/util/styles.dart';

class HomePage extends StatefulWidget {
  static const double mainTextSize = 24;
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController controller = TextEditingController();
  Widget submitButtonText = const Text(
    "Submit",
    style: TextStyle(
        color: Styles.white,
        fontSize: 16,
        fontWeight: FontWeight.bold,
        fontFamily: Styles.fontFamily
    ),
  );

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              "YouTube Video",
              style: TextStyle(
                  fontSize: HomePage.mainTextSize,
                  color: Styles.white,
                  fontWeight: FontWeight.bold,
                  fontFamily: Styles.fontFamily
              ),
            ),
            SizedBox(width: 10,),
            Text(
              "Downloader",
              style: TextStyle(
                  fontSize: HomePage.mainTextSize,
                  color: Styles.red,
                  fontWeight: FontWeight.bold,
                  fontFamily: Styles.fontFamily
              ),
            )
          ],
        ),
        const Padding(
          padding: EdgeInsets.all(8.0),
          child: Text(
            "Use this convenient YouTube video Downloader site to easily save"
                " your favorite videos for offline viewing.",
            textAlign: TextAlign.center,
            style: TextStyle(
                color: Styles.white,
                fontSize: 12,
                fontFamily: Styles.fontFamily
            ),
          ),
        ),
        Container(
          width: double.infinity,
          padding: const EdgeInsets.symmetric(
              horizontal: 20,
              vertical: 50
          ),
          margin: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            border: Border.all(
                color: Styles.red
            ),
            borderRadius: const BorderRadius.all(Radius.circular(25)),
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                "YouTube Video URL"
                    " or Search Term",
                maxLines: 2,
                style: TextStyle(
                    color: Styles.white,
                    fontFamily: Styles.fontFamily
                ),
              ),
              Container(
                margin: const EdgeInsets.symmetric(vertical: 20),
                height: 40,
                child: TextField(
                  controller: controller,
                  decoration: const InputDecoration(
                      fillColor: Styles.white,
                      filled: true,
                      hintText: "Search",
                      hintStyle: TextStyle(
                          color: Styles.grey,
                          fontFamily: Styles.fontFamily
                      ),
                      border: OutlineInputBorder(
                          borderRadius: BorderRadius.all(Radius.circular(8))
                      )
                  ),
                  style: const TextStyle(
                      fontFamily: Styles.fontFamily,
                      fontSize: 12,
                      height: 1
                  ),
                  onSubmitted: onSubmit,
                ),
              ),
              Container(
                height: 50,
                width: 140,
                margin: const EdgeInsets.only(top: 20),
                decoration: const BoxDecoration(
                  borderRadius: BorderRadius.all(Radius.circular(5)),
                  color: Styles.red,
                ),
                child: TextButton(
                  onPressed: onSubmit,
                  child: submitButtonText
                ),
              )
            ],
          ),
        )
      ],
    );
  }

  void onSubmit([String? value]) {
    if (controller.text.isEmpty) return;
    if (value != null) controller.text = value;
    setState(() {
      submitButtonText = const SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(
          color: Styles.white,
          strokeWidth: 2,
        ),
      );
    });
    Api.instance.search(controller.text).then((value) {
      if (!context.mounted) return;
      if ((value as List).isEmpty) {
        setState(() {
          submitButtonText = const Text(
            "Submit",
            style: TextStyle(
                color: Styles.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
                fontFamily: Styles.fontFamily
            ),
          );
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("No results found!"),
            backgroundColor: Styles.red,
          )
        );
        return;
      }

      if ((value).length == 1) {
        Navigator.of(context).push(
            MaterialPageRoute(
                builder: (context) => BaseFrame(
                    product: product,
                    child: VideoScreen(
                      searchResult: SearchResultModel(
                          videoId: value.first["video_id"],
                          title: value.first["title"],
                          thumbnailUrl: value.first["thumbnail_url"],
                          channelName: value.first["channel_name"]
                      ),
                    )
                )
            )
        );
      }

      else {
        setState(() {
          submitButtonText = const Text(
            "Submit",
            style: TextStyle(
                color: Styles.white,
                fontSize: 16,
                fontWeight: FontWeight.bold,
                fontFamily: Styles.fontFamily
            ),
          );
        });
        ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Multiple search not implemented yet")
            )
        );
        return;
      }
    });
  }
}

