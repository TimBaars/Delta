import 'dart:math';

import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_override_status.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_optimized_path_image.dart';
import 'package:frontend/widgets/widget_planned_path_image.dart';

class OverrideScreen extends StatefulWidget {
  OverrideScreen({super.key});

  @override
  _OverrideScreenState createState() => _OverrideScreenState();
}

class _OverrideScreenState extends State<OverrideScreen> {
  final SystemStatusLogic logic = SystemStatusLogic();
  
  @override
  void initState() {
    super.initState();
    logic.function = () {
      setState(() {});
      return {};
    };
    logic.updateFunctions();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: <Widget>[
          Expanded(
            flex: 1,
            child: Table(
              children: [
                TableRow(
                  children: [
                    getContainerContent(0),
                    getContainerContent(1),
                  ],
                ),
                TableRow(
                  children: [
                    getContainerContent(2),
                    getContainerContent(3),
                  ],
                ),
                TableRow(
                  children: [
                    getContainerContent(4),
                    getContainerContent(5),
                  ],
                ),
              ],
              defaultVerticalAlignment: TableCellVerticalAlignment.middle,
            ),
          ),
        ],
      ),
    );
  }

  Widget getContainerContent(int index) {
    switch (index) {
      case 0:
        return LocationButtonContainer(title: 'System', value: "Stop", endpointAddition: "system", json: "{\"status\": \"false\"}");
      case 1:
        return LocationButtonContainer(title: 'System', value: "Start", endpointAddition: "system", json: "{\"status\": \"true\"}");
      case 2:
        return LocationButtonContainer(title: 'Delta Control', value: "...", endpointAddition: "delta", json: "");
      case 3:
        return LocationButtonContainer(title: 'Delta Control', value: "...", endpointAddition: "delta", json: "");
      case 4:
        return LocationButtonContainer(title: 'Delta Finished Moving', value: "Trigger Actuator", endpointAddition: "actuator", json: "{\"running\": \"true\"}");
      case 5:
        return LocationButtonContainer(title: 'Actuator Finished', value: "Trigger Delta", endpointAddition: "actuator", json: "{\"running\": \"false\"}");
      default:
        return Text('Container ${index + 1}');
    }
  }
}

class LocationButtonContainer extends StatelessWidget {
  final String title;
  final String value;
  final String endpointAddition;
  final String json;

  LocationButtonContainer({required this.title, required this.value, required this.endpointAddition, required this.json});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      height: 200, // Set the height of the container
      padding: EdgeInsets.all(8.0),
      margin: EdgeInsets.all(4.0),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(title, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          SizedBox(height: 8),
          // This is where you'd fetch and display data from the server
          TextButton(
            onPressed: () {
              if (json == "") return
              
              OverrideStatusLogic().override(endpointAddition, json);
            },
            child: Text(value, style: TextStyle(fontSize: 16)),
          ),
          // You can replace the above Text widget with any other widgets to display fetched data
        ],
      ),
    );
  }
}
