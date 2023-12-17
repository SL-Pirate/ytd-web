import 'package:flutter/material.dart';

class SquareIconButton extends StatelessWidget {
  final Icon icon;
  final void Function() onPressed;
  final Color? color;
  final double? width;
  final double? height;
  const SquareIconButton({
    super.key,
    required this.icon,
    required this.onPressed,
    this.color,
    this.width,
    this.height
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onPressed,
      child: Container(
        width: width ?? 40,
        height: height ?? 40,
        decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(4)
        ),
        child: Center(child: icon),
      ),
    );
  }
}
