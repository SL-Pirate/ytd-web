import 'package:flutter/material.dart';
import 'package:ytd_web/screens/about_screen.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/contact_info.dart';
import 'package:ytd_web/widgets/log_in_button.dart';
import 'package:ytd_web/widgets/logo.dart';

class BaseFrame extends StatelessWidget {
  final Widget child;
  final String product;

  const BaseFrame({super.key, required this.child, required this.product});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: PreferredSize(
          preferredSize: Size(
            double.infinity,
            Styles.of(context).isMobile ? 85 : 100,
          ),
          child: Material(
            color: Styles.primary,
            child: Material(
              elevation: 10,
              color: Styles.primary,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  (!Styles.of(context).isMobile)
                      ? const ContactInfo()
                      : const SizedBox(
                          width: 50,
                        ),
                  const Center(
                    child: Logo(),
                  ),
                  (!Styles.of(context).isMobile)
                      ? const LogInButton()
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
                      fontFamily: Styles.fontFamily,
                      fontWeight: Styles.fontWeightLight,
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
