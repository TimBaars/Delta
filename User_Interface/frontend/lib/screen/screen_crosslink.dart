import 'package:flutter/material.dart';
import '../widgets/widget_ground_thruth_image.dart';
import '../widgets/widget_rrt_image.dart';
import '../widgets/widget_datapoints.dart';
import '../widgets/widget_start_stop.dart';

class AllScreen extends StatelessWidget {
 @override
 Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Generic Screen'),
      ),
      body: Column(
        children: <Widget>[
          Expanded(
            child: Row(
              children: <Widget>[
                Expanded(child: GroundThruthImageWidget()),
                Expanded(child: DataPointsOverlayImageWidget()),
              ],
            ),
          ),
          Expanded(
            child: Row(
              children: <Widget>[
                Expanded(
                 child: Column(
                    children: <Widget>[
                      Expanded(
                        child: Row(
                          children: <Widget>[
                            Expanded(
                              child: GroundThruthImageWidget() // Delta robot status
                            ),
                            Expanded(
                              child: GroundThruthImageWidget() // Delta robot status
                            ),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Row(
                          children: <Widget>[
                            Expanded(
                              child: RobotStatusButtonWidget() // Start/Stop
                            ),
                            Expanded(
                              child: GroundThruthImageWidget() // Actuator status
                            ),
                          ],
                        ),
                      )
                    ],
                 ),
                ),
                Expanded(child: RrtImageWidget()),
              ],
            ),
          ),
        ],
      ),
    );
 }
}
