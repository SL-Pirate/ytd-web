import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';

class GenericButton extends StatelessWidget {
  final String text;
  const GenericButton(this.text, {super.key});

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: () {},
      child: Text(
        text,
        style: TextStyle(
            color: Styles.white,
            fontSize: Styles.of(context).bodyFontSize,
            fontFamily: Styles.fontFamily,
            fontWeight: FontWeight.bold
        ),
      ),
    );
  }
}

