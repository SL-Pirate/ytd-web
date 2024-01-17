import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:ytd_web/screens/about_screen.dart';
import 'package:ytd_web/util/styles.dart';

class BaseFrame extends StatelessWidget {
  final Widget child;
  final String product;

  const BaseFrame({super.key, required this.child, required this.product});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: const Size(double.infinity, 100),
          child: Material(
            color: Styles.primary,
            child: Material(
              elevation: 10,
              color: Styles.primary,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  (!Styles.of(context).isMobile)
                      ? Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: InkWell(
                            onTap: () {
                              launchUrl(
                                Uri.parse(
                                    "https://www.github.com/SL-Pirate/ytd-web"),
                              );
                            },
                            child: const Icon(
                              FontAwesomeIcons.github,
                              color: Styles.textColor,
                              size: 50,
                            ),
                          ),
                        )
                      : const SizedBox(
                          width: 50,
                        ),
                  Center(
                    child: Image.asset(
                      "assets/img/logo.png",
                      width: 100,
                    ),
                  ),
                  (!Styles.of(context).isMobile)
                      ? Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: SizedBox(
                            height: 60,
                            width: 150,
                            child: ElevatedButton(
                              style: Styles.buttonStyle,
                              onPressed: () {},
                              child: const Text(
                                "Log In",
                                style: TextStyle(fontWeight: FontWeight.bold),
                              ),
                            ),
                          ),
                        )
                      : IconButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => const AboutScreen(),
                              ),
                            );
                          },
                          icon: const Icon(
                            Icons.menu,
                            color: Styles.textColor,
                            size: 25,
                          ),
                        )
                ],
              ),
            ),
          ),
        ),
        body: Material(
          color: Styles.primary,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const SizedBox(),
              child,
              Container(
                width: double.infinity,
                height: 30,
                color: Styles.color4,
                child: Center(
                  child: Text(
                    "Copyright © ${DateTime.now().year} $product. "
                    "All Rights Reserved.",
                    style: TextStyle(
                        color: Styles.buttonTextColor,
                        fontSize: Styles.of(context).fontSizeSmall,
                        fontFamily: Styles.fontFamily),
                  ),
                ),
              )
            ],
          ),
        ),
      ),
    );
  }
}
