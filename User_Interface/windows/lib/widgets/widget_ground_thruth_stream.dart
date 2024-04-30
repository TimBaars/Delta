import 'dart:html' as html;
import 'package:flutter/material.dart';

import 'package:windows/util/constants.dart';

class GroundThruthStreamWidget extends StatefulWidget {
  GroundThruthStreamWidget({Key? key}) : super(key: key);

  @override
  _GroundThruthStreamWidgetState createState() =>
      _GroundThruthStreamWidgetState();
}

class _GroundThruthStreamWidgetState extends State<GroundThruthStreamWidget> {
  late html.VideoElement _videoElement;

  @override
  void initState() {
    super.initState();
    _videoElement = html.VideoElement()
      ..src = STREAMENDPOINT
      ..autoplay = true
      ..controls = true;
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: HtmlElementView(
        viewType: 'video-player',
        onPlatformViewCreated: (int id) {
          final container =
              html.window.document.getElementById('video-player')!;
          container.append(_videoElement);
        },
      ),
    );
  }

  @override
  void dispose() {
    _videoElement.remove();
    super.dispose();
  }
}

void main() {
  runApp(MaterialApp(
    home: Expanded(child: GroundThruthStreamWidget()),
  ));
}
