import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:ytd_web/util/styles.dart';

class AboutScreen extends StatelessWidget {
  const AboutScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Styles.primary,
      body: Column(
        children: [
          Align(
            alignment: Alignment.centerRight,
            child: IconButton(
              onPressed: () {
                Navigator.pop(context);
              },
              icon: const Icon(Icons.close),
            ),
          ),
          const SizedBox(
            height: 140,
          ),
          Image.asset(
            "assets/img/logo.png",
            width: 100,
          ),
          const SizedBox(
            height: 60,
          ),
          InkWell(
            onTap: () {
              launchUrl(
                Uri.parse("https://www.github.com/SL-Pirate/ytd-web"),
              );
            },
            child: const Icon(
              FontAwesomeIcons.github,
              color: Styles.textColor,
              size: 50,
            ),
          ),
          const SizedBox(
            height: 35,
          ),
          SizedBox(
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
          )
        ],
      ),
    );
  }
}
