import 'package:flutter/material.dart';
import 'package:flutter_vlc_player/flutter_vlc_player.dart';

import 'package:ui/util/constants.dart';

class GroundThruthStreamWidget extends StatefulWidget {
  GroundThruthStreamWidget({Key? key}) : super(key: key);

  @override
  _GroundThruthStreamWidgetState createState() =>
      _GroundThruthStreamWidgetState();
}

class _GroundThruthStreamWidgetState extends State<GroundThruthStreamWidget> {
  late VlcPlayerController _vlcPlayerController;

  @override
  void initState() {
    super.initState();
    _vlcPlayerController = VlcPlayerController.network(
      RMQHOST,
      autoPlay: true,
      options: VlcPlayerOptions(),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Expanded(
            child: VlcPlayer(
              controller: _vlcPlayerController,
              aspectRatio: 16 / 9,
              placeholder: Center(child: CircularProgressIndicator()),
            ),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _vlcPlayerController.dispose();
    super.dispose();
  }
}

void main() {
  runApp(MaterialApp(
    home: GroundThruthStreamWidget(),
  ));
}
