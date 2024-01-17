import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';
import 'package:ytd_web/widgets/contact_info.dart';
import 'package:ytd_web/widgets/log_in_button.dart';
import 'package:ytd_web/widgets/logo.dart';

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
          const Logo(),
          const SizedBox(
            height: 60,
          ),
          const ContactInfo(),
          const SizedBox(
            height: 35,
          ),
          const LogInButton()
        ],
      ),
    );
  }
}
