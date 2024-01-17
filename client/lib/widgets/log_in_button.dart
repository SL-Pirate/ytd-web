import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';

class LogInButton extends StatelessWidget {
  const LogInButton({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20.0),
      child: SizedBox(
        height: 60,
        width: 150,
        child: ElevatedButton(
          style: Styles.buildButtonStyle(borderRadius: 10),
          onPressed: () {},
          child: const Text(
            "Log In",
            style: TextStyle(fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }
}
