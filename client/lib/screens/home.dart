import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:ytd_web/components/SearchResultsComponent.dart';
import 'package:ytd_web/util/styles.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController controller = TextEditingController();
  late String product;
  static const double mainTextSize = 24;

  @override
  void initState() {
    if (kIsWeb) {
      product = "YTD-Web";
    }
    else if (Platform.isAndroid || Platform.isIOS) {
      product = "YTD-Mobile";
    }
    else if (Platform.isLinux || Platform.isWindows || Platform.isMacOS) {
      product = "YTD-Desktop";
    }
    else {
      product = "YTDL";
    }

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: PreferredSize(
        preferredSize: const Size(double.infinity, 250),
        child: Material(
          color: Styles.blue,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Material(
                elevation: 10,
                color: Styles.blue,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Image.asset(
                        "assets/img/logo.png",
                        width: 100,
                        height: 50,
                        // scale: 5,
                      ),
                    ),
                    Container(
                      width: 100,
                      margin: const EdgeInsets.all(8),
                      decoration: const BoxDecoration(
                          color: Styles.red,
                          borderRadius: BorderRadius.all(Radius.circular(5))
                      ),
                      child: TextButton(
                          onPressed: () {},
                          child: const Text(
                            "Log In",
                            style: TextStyle(
                              color: Styles.white,
                              fontFamily: Styles.fontFamily
                            ),
                          )
                      ),
                    )
                  ],
                ),
              ),
              Column(
                children: [
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Text(
                        "YouTube Video",
                        style: TextStyle(
                          fontSize: mainTextSize,
                          color: Styles.white,
                          fontWeight: FontWeight.bold,
                          fontFamily: Styles.fontFamily
                        ),
                      ),
                      SizedBox(width: 10,),
                      Text(
                        "Downloader",
                        style: TextStyle(
                          fontSize: mainTextSize,
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
                          "your favorite videos for offline viewing.",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Styles.white,
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
                          " Or Search Term",
                          maxLines: 2,
                          style: TextStyle(
                            color: Styles.white,
                            fontWeight: FontWeight.bold,
                            fontFamily: Styles.fontFamily
                          ),
                        ),
                        Container(
                          margin: const EdgeInsets.all(10),
                          height: 50,
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
                            ),
                          )
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(
                            vertical: 8,
                            horizontal: 25
                          ),
                          margin: const EdgeInsets.symmetric(vertical: 20),
                          decoration: const BoxDecoration(
                            borderRadius: BorderRadius.all(Radius.circular(5)),
                            color: Styles.red,
                          ),
                          child: TextButton(
                            onPressed: () {},
                            child: const Text(
                              "Submit",
                              style: TextStyle(
                                color: Styles.white,
                                fontWeight: FontWeight.bold,
                                fontFamily: Styles.fontFamily
                              ),
                            ),
                          ),
                        )
                      ],
                    ),
                  )
                ],
              ),
              const SizedBox()
            ],
          ),
        ),
      )

      // Scaffold(
      //   appBar: PreferredSize(
      //     preferredSize: const Size(double.infinity,  125),
      //     child: Container(
      //       color: Colors.blue,
      //       child: Column(
      //         children: [
      //           Padding(
      //             padding: const EdgeInsets.all(8.0),
      //             child: Text(
      //               "Welcome to $product",
      //               style: const TextStyle(
      //                 fontWeight: FontWeight.bold,
      //                 fontSize: 24
      //               ),
      //             ),
      //           ),
      //           Padding(
      //             padding: const EdgeInsets.symmetric(horizontal: 8.0),
      //             child: SearchBar(
      //               controller: _ctrlr,
      //               onSubmitted: onSubmitted,
      //               trailing: [
      //                 IconButton(
      //                     onPressed: onSubmitted,
      //                     icon: const Icon(Icons.search)
      //                 )
      //               ],
      //             ),
      //           )
      //         ],
      //       ),
      //     ),
      //   ),
      //   body: SearchResultsComponent(output),
      // ),
    );
  }
}
