import 'package:flutter/material.dart';
import 'dart:math';
import 'package:flutter_bloc/flutter_bloc.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_block.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_event.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_state.dart';

import 'package:mines_app/tile.dart';

// Minefield widget definition
class Minefield extends StatelessWidget {
  final int rows;
  final int columns;
  final double mineSize;
  final double margin;
  final int minesCount;
  late List<List<TileButton>> table;

  Minefield({
    super.key,
    required this.rows,
    required this.columns,
    required this.mineSize,
    required this.margin,
    required double minesPercent,
  }) : minesCount = (rows * columns * minesPercent / 100).round() {
    table = createGrid();
    distributeMines();
    hintPopulate();
  }

  List<List<TileButton>> createGrid() {
    List<List<TileButton>> table = [];
    double rowOffset = 0;
    for (int iRow = 0; iRow < rows; iRow++) {
      List<TileButton> row = [];
      double columnOffset = 0;
      for (int iCol = 0; iCol < columns; iCol++) {
        TileButton tile = TileButton(
          x: columnOffset,
          y: rowOffset,
          iColumn: iCol,
          iRow: iRow,
          width: mineSize,
          height: mineSize,
          defaultColor: Colors.white,
          text: '',
        );
        columnOffset += mineSize + margin;
        row.add(tile);
      }
      rowOffset += mineSize + margin;
      table.add(row);
    }
    return table;
  }

  void clearField(int xStart, int yStart) {
    if (table[yStart][xStart].clicked) {
      return;
    }
    table[yStart][xStart].clicked = true; // Mark as clicked
    if (table[yStart][xStart].minesAround != 0) {
      return;
    }
    for (var tryout in [
      [yStart + 1, xStart],
      [yStart, xStart + 1],
      [yStart + 1, xStart + 1],
      [yStart - 1, xStart],
      [yStart, xStart - 1],
      [yStart - 1, xStart - 1],
      [yStart - 1, xStart + 1],
      [yStart + 1, xStart - 1],
    ]) {
      if (tryout[0] >= 0 &&
          tryout[1] >= 0 &&
          tryout[0] < rows &&
          tryout[1] < columns) {
        clearField(tryout[1], tryout[0]);
      }
    }
  }

  void distributeMines() {
    var random = Random();
    var minesCoordinates = <List<int>>[];
    int count = minesCount;
    while (count > 0) {
      int mineYRows = random.nextInt(rows);
      int mineXCols = random.nextInt(columns);
      if (minesCoordinates.contains([mineYRows, mineXCols])) {
        continue;
      }
      minesCoordinates.add([mineYRows, mineXCols]);
      table[mineYRows][mineXCols].injectMine();
      count--;
    }
  }

  void hintPopulate() {
    for (int iRow = 0; iRow < table.length; iRow++) {
      for (int iColumn = 0; iColumn < table[iRow].length; iColumn++) {
        TileButton current = table[iRow][iColumn];
        for (var tryout in [
          [iRow + 1, iColumn],
          [iRow, iColumn + 1],
          [iRow + 1, iColumn + 1],
          [iRow - 1, iColumn],
          [iRow, iColumn - 1],
          [iRow - 1, iColumn - 1],
          [iRow - 1, iColumn + 1],
          [iRow + 1, iColumn - 1],
        ]) {
          if (tryout[0] >= 0 &&
              tryout[1] >= 0 &&
              tryout[0] < rows &&
              tryout[1] < columns &&
              table[tryout[0]][tryout[1]].mine) {
            current.incrementMinesAround();
          }
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Text("Table of Tiles"),
        Expanded(
          child: Stack(
            children: table.asMap().entries.expand((entry) {
              int rowIndex = entry.key;
              List<Widget> row = entry.value.map((tile) {
                return BlocProvider(
                  create: (_) => TileBloc(), // Create a new Bloc for each tile
                  child: tile, // Assuming 'tile' is already a widget
                );
              }).toList();
              return row;
            }).toList(), // Flatten the table
          ),
        ),
      ],
    );
  }
}
