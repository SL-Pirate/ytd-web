import 'package:flutter/material.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/main.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/screens/base_frame.dart';
import 'package:ytd_web/screens/video_screen.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/search_result_widget.dart';

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

  dynamic result;

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(height: 100),
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
              constraints: const BoxConstraints(
                maxWidth: 1000,
              ),
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
                          contentPadding: EdgeInsets.symmetric(horizontal: 10),
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
            ),
            if (result != null) Column(
                children:
                    () {
                  List<Widget> children = [];

                  children.add(const SizedBox(height: 50));

                  for (dynamic item in result) {
                    SearchResultModel data = SearchResultModel(
                        videoId: item["video_id"],
                        title: item["title"],
                        description: item["description"],
                        thumbnailUrl: item["thumbnail_url"],
                        channelName: item["channel_name"],
                        channelThumbnailUrl: item["channel_thumbnail_url"]
                    );

                    children.add(Padding(
                      padding: const EdgeInsets.only(
                          bottom: 10,
                          top: 10,
                          left: 16
                      ),
                      child: GestureDetector(
                        onTap: () {
                          Navigator.of(context).push(
                              MaterialPageRoute(
                                  builder: (context) => BaseFrame(
                                      product: product,
                                      child: VideoScreen(searchResult: data)
                                  )
                              )
                          );
                        },
                        child: SearchResultWidget(data),
                      ),
                    ));
                  }

                  return children;
                } ()
            )
          ],
        ),
      ),
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
                          description: value.first["description"],
                          thumbnailUrl: value.first["thumbnail_url"],
                          channelName: value.first["channel_name"],
                          channelThumbnailUrl: value.first["channel_thumbnail_url"]
                      ),
                    )
                )
            )
        );
      }

      else {
        setState(() {
          result = value;
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
        return;
      }
    });
  }
}
