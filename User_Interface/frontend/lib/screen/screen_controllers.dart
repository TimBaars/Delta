import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_actuator_status.dart';
import '../widgets/widget_start_stop.dart';

class ControllerScreen extends StatelessWidget {
  late final ActuatorStatusLogic logic;

  ControllerScreen({super.key}) : logic = ActuatorStatusLogic();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Controllers Screen'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(
            child: Column(
              children: <Widget>[
                // Expanded(child: RrtImageWidget()),
                Expanded(child: RobotStatusButtonWidget()),
              ],
            ),
          ),
          Expanded(
            child: Column(
              children: <Widget>[
                // Expanded(child:), // Delta robot status
                // Expanded(child: ActuatorStatusWidget(logic: logic)), // Actuator status
              ],
            ),
          ),
        ],
      ),
    );
  }
}
