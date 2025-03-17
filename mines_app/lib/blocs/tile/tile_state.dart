// Define the state of the Counter (in this case, just an integer)
class TileState {
  final bool clicked;
  final bool flagged;

  TileState({required this.clicked, this.flagged = false});

  TileState copyWith({bool? clicked, bool? flagged}) {
    return TileState(
      clicked: clicked ?? this.clicked,
      flagged: flagged ?? this.flagged,
    );
  }
}
