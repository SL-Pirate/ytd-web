import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:ytd_web/util/api.dart';
import 'package:ytd_web/main.dart';
import 'package:ytd_web/models/search_result_model.dart';
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
      searchText = Icon(
        Icons.search,
        size: Styles.of(context).bodyFontSize,
      );

      searchSuffix = searchText!;
    }

    return Expanded(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            SizedBox(
              width: MediaQuery.of(context).size.width,
            ),
            const SizedBox(height: 100),
            SvgPicture.asset(
              "img/home_page_icon.svg",
              width: 200,
              height: 175,
            ),
            const SizedBox(height: 50),
            Text(
              "Online Video Downloader",
              style: TextStyle(
                  fontSize: Styles.of(context).titleFontSize,
                  color: Styles.textColor,
                  fontWeight: FontWeight.bold,
                  fontFamily: Styles.fontFamily),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text(
                "Use this convenient YouTube video Downloader site to easily save"
                " your favorite videos for offline viewing.",
                textAlign: TextAlign.center,
                style: TextStyle(
                    color: Styles.textColor,
                    fontSize: Styles.of(context).bodyFontSize,
                    fontFamily: Styles.fontFamily),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 50),
              child: Material(
                color: Styles.backgroundColor,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(20),
                ),
                shadowColor: Styles.shadowColor,
                elevation: 5,
                child: Container(
                  constraints: const BoxConstraints(
                    maxWidth: 1000,
                  ),
                  width: double.infinity,
                  margin: const EdgeInsets.all(20),
                  padding: EdgeInsets.symmetric(
                    horizontal: Styles.of(context).isMobile ? 10 : 20,
                    vertical: Styles.of(context).isMobile ? 10 : 20,
                  ),
                  color: Styles.backgroundColor,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        "YouTube Video URL"
                        " or Search Term",
                        style: TextStyle(
                          color: Styles.textColor,
                          fontFamily: Styles.fontFamily,
                          fontSize: Styles.of(context).bodyFontSize,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                      const SizedBox(height: 10),
                      SizedBox(
                        height: Styles.of(context).isMobile ? 40 : 50,
                        child: Row(
                          children: [
                            Expanded(
                              child: TextField(
                                controller: controller,
                                decoration: InputDecoration(
                                    fillColor: Styles.backgroundColor,
                                    filled: true,
                                    hintText: "YouTube Video URL"
                                        " or Search Term",
                                    hintStyle: TextStyle(
                                        color: Styles.color4,
                                        fontFamily: Styles.fontFamily,
                                        fontSize:
                                            Styles.of(context).fontSizeSmall),
                                    contentPadding: const EdgeInsets.symmetric(
                                        horizontal: 10),
                                    border: const OutlineInputBorder(
                                        borderRadius: BorderRadius.all(
                                            Radius.circular(8)))),
                                style: TextStyle(
                                    fontFamily: Styles.fontFamily,
                                    fontSize: Styles.of(context).bodyFontSize),
                                onSubmitted: onSubmit,
                              ),
                            ),
                            const SizedBox(width: 20),
                            IconButton(
                              style: Styles.buttonStyle,
                              onPressed: onSubmit,
                              icon: Padding(
                                padding: const EdgeInsets.all(8.0),
                                child: searchSuffix,
                              ),
                            )
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
            if (result != null)
              Container(
                constraints: const BoxConstraints(
                  maxWidth: 1000,
                ),
                child: Column(children: () {
                  List<Widget> children = [];

                  children.add(const SizedBox(height: 50));

                  for (dynamic item in result) {
                    SearchResultModel data = SearchResultModel(
                      url: item["url"],
                      title: item["title"],
                      description: item["description"],
                      thumbnailUrl: item["thumbnail_url"],
                      channelName: item["channel_name"],
                      channelThumbnailUrl: item["channel_thumbnail_url"],
                    );

                    children.add(Padding(
                      padding:
                          const EdgeInsets.only(bottom: 10, top: 10, left: 16),
                      child: GestureDetector(
                        onTap: () {
                          Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => BaseFrame(
                                  product: product,
                                  child: VideoScreen(searchResult: data))));
                        },
                        child: SearchResultComponent(data),
                      ),
                    ));
                  }

                  return children;
                }()),
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
      searchSuffix = SizedBox(
        width: Styles.of(context).bodyFontSize,
        height: Styles.of(context).bodyFontSize,
        child: const CircularProgressIndicator(
          color: Styles.buttonTextColor,
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
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text("No results found!"),
          backgroundColor: Styles.secondary,
        ));
        return;
      }

      setState(() {
        result = value;
        searchSuffix = searchText!;
      });

      if ((value).length == 1) {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => BaseFrame(
              product: product,
              child: VideoScreen(
                searchResult: SearchResultModel(
                    url: value.first["url"],
                    title: value.first["title"],
                    description: value.first["description"],
                    thumbnailUrl: value.first["thumbnail_url"],
                    channelName: value.first["channel_name"],
                    channelThumbnailUrl: value.first["channel_thumbnail_url"]),
              ),
            ),
          ),
        );
      } else {
        return;
      }
    });
  }
}
