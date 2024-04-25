import 'package:flutter/material.dart';
import 'package:windows/logic/logic_actuator_status.dart';
import 'package:windows/widgets/widget_actuator_status.dart';
import '../widgets/widget_rrt_tree.dart';
import '../widgets/widget_start_stop.dart';

class ControllerScreen extends StatelessWidget {
  late final ActuatorStatusLogic logic;

  ControllerScreen({super.key}) : logic = ActuatorStatusLogic();

  @override
  Widget build(BuildContext context) {
    logic.enable();

    return Scaffold(
      appBar: AppBar(
        title: Text('Controllers Screen'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: RrtTreeImageWidget()),
                Expanded(child: RobotStatusButtonWidget()),
              ],
            ),
          ),
          Expanded(
            child: Column(
              children: <Widget>[
                // Expanded(child:), // Delta robot status
                Expanded(child: ActuatorStatusWidget(logic: logic)), // Actuator status
              ],
            ),
          ),
        ],
      ),
    );
  }
}
