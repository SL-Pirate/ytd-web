import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:ytd_web/util/styles.dart';

class ContactInfo extends StatelessWidget {
  const ContactInfo({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: InkWell(
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
    );
  }
}
