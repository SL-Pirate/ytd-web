import 'package:flutter/material.dart';

class Styles {
  BuildContext context;
  Styles._(this.context);

  static Styles of(BuildContext context) {
    Styles styles = Styles._(context);

    return styles;
  }

  // primary colors
  static const Color primary = Color(0xFFEBF6FF);
  static const Color secondary = Color(0xFFE9242B);

  // secondary colors
  static const Color textColor = Color(0xFF000000);
  static const Color backgroundColor = Color(0xFFFFFFFF);
  static const Color buttonTextColor = Color(0xFFFFFFFF);
  static const Color buttonColor = Color(0xFF012F58);
  static const Color shadowColor = Color(0x00000029);
  static const Color borderColor = Color(0xFF707070);
  static const Color color4 = Color(0xFF012F58);
  static const Color successColor = Color(0xFF03FF44);
  static const Color hintTextColor = Color(0xFF7E7E7E);

  // font family
  static const String fontFamily = "Poppins";

  double get titleFontSize => (isMobile) ? 25.0 : 50.0;
  double get subtitleFontSize => (isMobile) ? 12.0 : 20.0;
  double get bodyFontSize => (isMobile) ? 12.0 : 16.0;
  double get fontSizeSmall => (isMobile) ? 10 : 12;
  double get fontSizeChannelLabel => (isMobile) ? 12 : 15;

  static ButtonStyle get buttonStyle => ButtonStyle(
        backgroundColor: MaterialStateProperty.all<Color>(buttonColor),
        foregroundColor: MaterialStateProperty.all<Color>(buttonTextColor),
        shape: MaterialStateProperty.all<RoundedRectangleBorder>(
          RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(5),
          ),
        ),
      );

  static ButtonStyle buildButtonStyle({
    Color? backgroundColor,
    Color? foregroundColor,
  }) {
    return ButtonStyle(
      backgroundColor:
          MaterialStateProperty.all<Color>(backgroundColor ?? buttonColor),
      foregroundColor:
          MaterialStateProperty.all<Color>(foregroundColor ?? buttonTextColor),
      shape: MaterialStateProperty.all<RoundedRectangleBorder>(
        RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(5),
        ),
      ),
    );
  }

  bool get isMobile => (MediaQuery.of(context).size.width < 600);
}
