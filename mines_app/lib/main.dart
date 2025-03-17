import 'package:flutter/material.dart';
import 'package:mines_app/sidebar.dart';
import 'package:mines_app/minefield.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Minesweeper',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Minesweeper'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  void resetMinefield() {
    // Logic to reset the minefield
    print('Minefield reset');
  }

  void exitGame() {
    // Logic to exit the game
    print('Exiting game...');
    Navigator.of(context).pop(); // Closes the app or goes back
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Column(
        children: [
          Sidebar(
            resetMinefield: resetMinefield,
            exitGame: exitGame,
          ),
          Expanded(
            child: Center(
              child: Minefield(
                rows: 10,
                columns: 10,
                mineSize: 40,
                margin: 5,
                minesPercent: 20,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
