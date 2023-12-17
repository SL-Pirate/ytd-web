import 'package:flutter/material.dart';
import 'package:ytd_web/util/styles.dart';

class GenericButton extends StatelessWidget {
  final dynamic text;
  final void Function()? onTap;
  final double? width;
  final double? height;
  const GenericButton(
      this.text,
      {
        super.key,
        this.onTap,
        this.width,
        this.height
      }
    );

  @override
  Widget build(BuildContext context) {
    assert(text is String || text is Widget, "Text must be either String or Widget");
    return InkWell(
      onTap: onTap,
      child: Container(
        width: width ?? (Styles.of(context).isMobile ? 120 : 190),
        height: height ?? (Styles.of(context).isMobile ? 40 : 60),
        decoration: BoxDecoration(
            color: Styles.red,
            borderRadius: BorderRadius.circular(5),
        ),
        child: Center(
          child: (text is String)
              ? Text(
            text,
            style: TextStyle(
                color: Styles.white,
                fontSize: Styles.of(context).bodyFontSize,
                fontFamily: Styles.fontFamily,
                fontWeight: FontWeight.bold
            ),
          )
              : text,
        ),
      ),
    );
  }
}

