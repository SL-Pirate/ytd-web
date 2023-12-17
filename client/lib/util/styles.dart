import 'package:flutter/cupertino.dart';

class Styles {
  BuildContext? context;
  Styles._();

  static Styles of(BuildContext context) {
    Styles styles = Styles._();
    styles.context = context;

    return styles;
  }

  // primary colors
  static const  Color blue = Color(0xFF11263E);
  static const Color red = Color(0xFFE9242B);

  // secondary colors
  static const Color white = Color(0xFFFFFFFF);
  static const Color black = Color(0xFF000000);
  static const Color grey = Color(0xFF8D8D8D);
  static const Color green = Color(0xFF03FF44);

  // font family
  static const String fontFamily = "Poppins";

  double get titleFontSize => (isMobile) ? 25.0 : 50.0;
  double get subtitleFontSize => (isMobile) ? 12.0 : 20.0;
  double get bodyFontSize => (isMobile) ? 12.0 : 16.0;
  double get fontSizeSmall => (isMobile) ? 10 : 12;

  bool get isMobile => (MediaQuery.of(context!).size.width < 600);
}
