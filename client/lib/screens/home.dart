import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
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
          child: Stack(
            children: [
              Material(
                elevation: 10,
                color: Styles.blue,
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(20.0),
                      child: Image.asset(
                        "assets/img/logo.png",
                        width: 100,
                        height: 50
                      ),
                    ),
                    Container(
                      width: 90,
                      height: 35,
                      margin: const EdgeInsets.all(20),
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
                              fontSize: 12,
                              fontFamily: Styles.fontFamily,
                              fontWeight: FontWeight.bold
                            ),
                          ),
                      ),
                    )
                  ],
                ),
              ),
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
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
                          child: TextFormField(
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
                            onPressed: () {},
                            child: const Text(
                              "Submit",
                              style: TextStyle(
                                color: Styles.white,
                                fontSize: 16,
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
              Align(
                alignment: Alignment.bottomCenter,
                child: Container(
                  width: double.infinity,
                  height: 30,
                  color: Styles.black.withOpacity(0.25),
                  child: Center(
                    child: Text(
                      "Copyright © ${DateTime.now().year} $product. "
                          "All Rights Reserved",
                      style: TextStyle(
                        color: Styles.grey.withOpacity(0.5),
                        fontSize: 12,
                        fontFamily: Styles.fontFamily
                      ),
                    ),
                  ),
                )
              )
            ],
          ),
        ),
      )
    );
  }
}
