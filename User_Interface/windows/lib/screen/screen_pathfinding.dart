import 'package:flutter/material.dart';
import '../widgets/widget_ground_thruth_image.dart';
import '../widgets/widget_rrt_tree.dart';
import '../widgets/widget_datapoints.dart';
import '../widgets/widget_start_stop.dart';

class PathFindingScreen extends StatelessWidget {
 @override
 Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Path Finding'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(child: GroundThruthImageWidget()),
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: DataPointsOverlayImageWidget()),
                Expanded(child: RrtTreeImageWidget()),
              ],
            ),
          ),
        ],
      ),
    );
 }
}
