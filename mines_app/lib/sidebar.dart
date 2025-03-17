import 'package:flutter/material.dart';
import 'package:mines_app/clickableObject.dart';

class MenuButton extends ClickableObject {
  final VoidCallback? onRightMouseClick;

  MenuButton({
    required super.x,
    required super.y,
    required super.width,
    required super.height,
    required super.defaultColor,
    required super.text,
    VoidCallback? onLeftMouseClick,
    this.onRightMouseClick,
  }) : super(
          onLeftMouseClick: onLeftMouseClick ??
              () => print(1), // Default action for left click
        );

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onLeftMouseClick, // Left mouse click (tap)
      onSecondaryTap: onRightMouseClick, // Right mouse click equivalent
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
    );
  }
}

class Sidebar extends StatelessWidget {
  final VoidCallback resetMinefield;
  final VoidCallback exitGame;

  const Sidebar({
    super.key,
    required this.resetMinefield,
    required this.exitGame,
  });

  @override
  Widget build(BuildContext context) {
    double buttonWidth = 150;
    double buttonHeight = 50;
    double buttonMargin = 20;

    return Container(
      width: buttonWidth + 40, // Add some margin for the container
      padding: const EdgeInsets.all(10), // Padding around the buttons
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          MenuButton(
            x: 0, // Position will be managed by the Column
            y: 0, // Position will be managed by the Column
            width: buttonWidth,
            height: buttonHeight,
            defaultColor: Colors.white,
            text: "Reset",
            onLeftMouseClick: resetMinefield,
          ),
          SizedBox(height: buttonMargin), // Space between buttons
          MenuButton(
            x: 0, // Position will be managed by the Column
            y: 0, // Position will be managed by the Column
            width: buttonWidth,
            height: buttonHeight,
            defaultColor: Colors.white,
            text: "Exit",
            onLeftMouseClick: exitGame,
          ),
        ],
      ),
    );
  }
}
