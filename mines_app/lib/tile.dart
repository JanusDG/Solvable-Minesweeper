import 'package:flutter/material.dart';
import 'dart:math';
import 'package:flutter_bloc/flutter_bloc.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_block.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_event.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_state.dart';

// TileButton widget definition
class TileButton extends StatelessWidget {
  // const TileButton({Key? key}) : super(key: key);
  final double x, y, width, height;
  final Color defaultColor;
  final String text;
  // final VoidCallback onLeftMouseClick;
  bool clicked = false;
  bool mine = false;
  int minesAround = 0;
  int iRow;
  int iColumn;

  TileButton({
    super.key,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
    required this.defaultColor,
    required this.text,
    // required this.onLeftMouseClick,
    required this.iColumn,
    required this.iRow,
  });

  // void onLeftMouseClick() {
  //   if (clicked) {
  //     return;
  //   }
  //   clicked = true;
  // }

  void injectMine() {
    mine = true;
  }

  void incrementMinesAround() {
    minesAround++;
  }

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<TileBloc, TileState>(
      builder: (context, state) {
        return Positioned(
          left: x,
          top: y,
          child: GestureDetector(
            onTap: () {
              context.read<TileBloc>().add(Click());
            },
            onLongPress: () {
              context.read<TileBloc>().add(DoubleClick());
            },
            child: Container(
              width: width,
              height: height,
              color: state.clicked
                  ? (mine ? Colors.red : Colors.grey)
                  : defaultColor,
              child: Center(
                  child: state.flagged
                      ? ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: Image.asset(
                            'extra/flag.png',
                            fit: BoxFit.cover, // Adjust the image fit
                          ))
                      : state.clicked
                          ? mine
                              ? ClipRRect(
                                  borderRadius: BorderRadius.circular(10),
                                  child: Image.asset(
                                    'extra/mine.png',
                                    fit: BoxFit.cover, // Adjust the image fit
                                  ))
                              : Text((minesAround > 0
                                  ? minesAround.toString()
                                  : ''))
                          : Text(
                              text,
                              style: const TextStyle(
                                  fontSize: 20.0, color: Colors.black),
                            )),
            ),
          ),
        );
      },
    );
  }
}
