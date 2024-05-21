import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_ground_truth_image.dart';
import 'package:frontend/widgets/widget_rrt_image.dart';
import '../widgets/widget_start_stop.dart';

class ControllerScreen extends StatelessWidget {
  late final SystemStatusLogic logic = SystemStatusLogic();
  ControllerScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Controllers Screen')),
      body: Row(
        children: <Widget>[
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: GroundTruthImageWidget(logic: logic.groundTruthImageLogic)),
                Expanded(child: DeltaRobotStatusButtonWidget(logic: logic)),
              ],
            ),
          ),
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: RrtImageWidget(logic: logic.rrtImageLogic)),
                // Expanded(child: ActuatorStatusWidget(logic: logic)), // Actuator status
              ],
            ),
          ),
        ],
      ),
    );
  }
}
