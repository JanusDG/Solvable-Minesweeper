import 'package:flutter/material.dart';

class ClickableObject extends StatelessWidget {
  final double x, y, width, height;
  final Color defaultColor;
  final String text;
  final VoidCallback onLeftMouseClick;

  const ClickableObject({
    super.key,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    required this.defaultColor,
    required this.text,
    required this.onLeftMouseClick,
  });

  @override
  Widget build(BuildContext context) {
    return Positioned(
      left: x,
      top: y,
      child: GestureDetector(
        onTap: onLeftMouseClick, // Equivalent to left mouse click
        child: Container(
          width: width,
          height: height,
          color: defaultColor,
          child: Center(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 36.0,
                color: Colors.black,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
