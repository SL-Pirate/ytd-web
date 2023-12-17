import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/generic_button.dart';

class BaseFrame extends StatelessWidget {
  final Widget child;
  final String product;

  const BaseFrame({
    super.key,
    required this.child,
    required this.product
  });

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: const Size(double.infinity, 250),
          child: Material(
            color: Styles.blue,
            child: Material(
              elevation: 10,
              color: Styles.blue,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Padding(
                    padding: const EdgeInsets.all(20.0),
                    child: InkWell(
                      onTap: () {
                        launchUrl(
                            Uri.parse(
                                "https://www.github.com/SL-Pirate/ytd-web"
                            )
                        );
                      },
                      child: const Icon(
                        FontAwesomeIcons.github,
                        color: Styles.white,
                        size: 35,
                      ),
                    ),
                  ),
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
                    child: const GenericButton("Log In"),
                  )
                ],
              ),
            ),
          ),
        ),
        body: Material(
          color: Styles.blue,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const SizedBox(),
              child,
              Container(
                width: double.infinity,
                height: 30,
                color: Styles.black.withOpacity(0.25),
                child: Center(
                  child: Text(
                    "Copyright © ${DateTime.now().year} $product. "
                        "All Rights Reserved.",
                    style: TextStyle(
                        color: Styles.grey.withOpacity(0.5),
                        fontSize: Styles.of(context).fontSizeSmall,
                        fontFamily: Styles.fontFamily
                    ),
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