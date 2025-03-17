import 'package:flutter_bloc/flutter_bloc.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_block.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_event.dart';
// ignore: unused_import
import 'package:mines_app/blocs/tile/tile_state.dart';

class TileBloc extends Bloc<TileEvent, TileState> {
  TileBloc() : super(TileState(clicked: false)) {
    on<Click>((event, emit) => emit(state.copyWith(clicked: !state.clicked)));
    on<DoubleClick>(
        (event, emit) => emit(state.copyWith(flagged: !state.flagged)));
  }
}
