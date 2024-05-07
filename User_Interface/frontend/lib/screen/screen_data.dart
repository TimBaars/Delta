import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_actuator_status.dart';
import 'package:frontend/widgets/widget_actuator_status.dart';

class DataScreen extends StatelessWidget {
  late final ActuatorStatusLogic logic;

  DataScreen({super.key}) : logic = ActuatorStatusLogic();

  @override
  Widget build(BuildContext context) {
    logic.start();
    
    return Scaffold(
      appBar: AppBar(
        title: Text('Data Screen'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: DataPointsWidget(logic: logic)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
