import 'package:flutter/material.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/main.dart';
import 'package:ytd_web/modals/search_result_model.dart';
import 'package:ytd_web/screens/base_frame.dart';
import 'package:ytd_web/screens/video_screen.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/components/search_result_component.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget searchSuffix = const SizedBox();
  Widget? searchText;
  final TextEditingController controller = TextEditingController();
  dynamic result;

  @override
  Widget build(BuildContext context) {
    if (searchText == null) {
      searchText = Text(
          "Search",
          style: TextStyle(
              color: Styles.white,
              fontFamily: Styles.fontFamily,
              fontWeight: Styles.of(context).isMobile ? null : FontWeight.bold,
              fontSize: Styles.of(context).bodyFontSize
          )
      );

      searchSuffix = searchText!;
    }

    return Expanded(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const SizedBox(height: 100),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  "YouTube Video",
                  style: TextStyle(
                      fontSize: Styles.of(context).titleFontSize,
                      color: Styles.white,
                      fontWeight: FontWeight.bold,
                      fontFamily: Styles.fontFamily
                  ),
                ),
                const SizedBox(width: 10,),
                Text(
                  "Downloader",
                  style: TextStyle(
                      fontSize: Styles.of(context).titleFontSize,
                      color: Styles.red,
                      fontWeight: FontWeight.bold,
                      fontFamily: Styles.fontFamily
                  ),
                )
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Use this convenient YouTube video Downloader site to easily save"
                    " your favorite videos for offline viewing.",
                textAlign: TextAlign.center,
                style: TextStyle(
                    color: Styles.white,
                    fontSize: Styles.of(context).bodyFontSize,
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
                  Text(
                    "YouTube Video URL"
                        " or Search Term",
                    style: TextStyle(
                        color: Styles.white,
                        fontFamily: Styles.fontFamily,
                        fontSize: Styles.of(context).subtitleFontSize
                    ),
                  ),
                  Container(
                    margin: const EdgeInsets.symmetric(vertical: 20),
                    height: Styles.of(context).isMobile ? 40 : 50,
                    child: TextField(
                      controller: controller,
                      decoration: InputDecoration(
                          fillColor: Styles.white,
                          filled: true,
                          hintText: "YouTube Video URL"
                              " or Search Term",
                          hintStyle: TextStyle(
                              color: Styles.grey,
                              fontFamily: Styles.fontFamily,
                              fontSize: Styles.of(context).bodyFontSize
                          ),
                          suffixIcon: InkWell(
                            onTap: () {
                              FocusScope.of(context).requestFocus(FocusNode());
                              onSubmit();
                            },
                            child: Container(
                              decoration: const BoxDecoration(
                                color: Styles.red,
                                borderRadius: BorderRadius.only(
                                  topRight: Radius.circular(8),
                                  bottomRight: Radius.circular(8),
                                ),
                              ),
                              width: Styles.of(context).isMobile ? 80 : 100,
                              child: Center(
                                  child: searchSuffix
                              ),
                            ),
                          ),
                          contentPadding: const EdgeInsets.symmetric(horizontal: 10),
                          border: const OutlineInputBorder(
                              borderRadius: BorderRadius.all(Radius.circular(8))
                          )
                      ),
                      style: TextStyle(
                          fontFamily: Styles.fontFamily,
                          fontSize: Styles.of(context).bodyFontSize
                      ),
                      onSubmitted: onSubmit,
                    ),
                  ),
                ],
              ),
            ),
            if (result != null) Container(
              constraints: const BoxConstraints(
                maxWidth: 1000,
              ),
              child: Column(
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
                          child: SearchResultComponent(data),
                        ),
                      ));
                    }

                    return children;
                  } ()
              ),
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
      searchSuffix = const SizedBox(
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
          searchSuffix = searchText!;
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
          searchSuffix = searchText!;
        });
        return;
      }
    });
  }
}
