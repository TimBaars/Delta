import 'package:flutter/material.dart';
import '../widgets/widget_ground_thruth_stream.dart';
import '../widgets/widget_rrt_image.dart';

class PathFindingScreen extends StatelessWidget {
 @override
 Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Path Finding'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(child: GroundThruthStreamWidget()),
          Expanded(
            child: Column(
              children: <Widget>[
                // Expanded(child: DataPointsOverlayImageWidget()),
                Expanded(child: RrtImageWidget()),
              ],
            ),
          ),
        ],
      ),
    );
 }
}
