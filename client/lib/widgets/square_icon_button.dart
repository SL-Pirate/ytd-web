import 'package:flutter/material.dart';

class SquareIconButton extends StatelessWidget {
  final Icon icon;
  final void Function() onPressed;
  final Color? color;
  const SquareIconButton({
    super.key,
    required this.icon,
    required this.onPressed,
    this.color
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onPressed,
      child: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
            color: color,
            borderRadius: BorderRadius.circular(4)
        ),
        child: Center(child: icon),
      ),
    );
  }
}
