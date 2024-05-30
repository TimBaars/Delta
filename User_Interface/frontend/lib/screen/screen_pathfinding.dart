import 'dart:math';

import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_optimized_path_image.dart';
import 'package:frontend/widgets/widget_planned_path_image.dart';

class PathFindingScreen extends StatefulWidget {
  PathFindingScreen({super.key});

  @override
  _PathFindingScreenState createState() => _PathFindingScreenState();
}

class _PathFindingScreenState extends State<PathFindingScreen> {
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
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          children: <Widget>[
            // Left side: Table of white containers
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
            SizedBox(width: 16), // Space between the table and images
            // Right side: Column of images
            Expanded(
              flex: 2,
              child: Column(
                children: <Widget>[
                  Expanded(
                    child: Column(
                      children: <Widget>[
                        Expanded(child: OptimizedPathImageWidget(logic: logic.optimizedPathImageLogic)),
                        SizedBox(width: 8),
                        Expanded(child: PlannedPathImageWidget(logic: logic.plannedPathImageLogic)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget getContainerContent(int index) {
    switch (index) {
      case 0:
        return LocationContainer(title: 'X location', value: logic.deltaStatusLogic.json["position"]["x"].toString());
      case 1:
        return LocationContainer(title: 'Status', value: logic.deltaStatusLogic.json["status"].toString());
      case 2:
        return LocationContainer(title: 'Y location', value: logic.deltaStatusLogic.json["position"]["y"].toString());
      case 3:
        return LocationContainer(title: 'Speed', value: logic.deltaStatusLogic.json["velocity"].toString());
      case 4:
        return LocationContainer(title: 'Z location', value: logic.deltaStatusLogic.json["position"]["z"].toString());
      case 5:
        return LocationContainer(title: 'Direction', value: logic.deltaStatusLogic.json["direction"].toString());
      default:
        return Text('Container ${index + 1}');
    }
  }
}

class LocationContainer extends StatelessWidget {
  final String title;
  final String value;

  LocationContainer({required this.title, required this.value});

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
          Text(value, style: TextStyle(fontSize: 16)),
          // You can replace the above Text widget with any other widgets to display fetched data
        ],
      ),
    );
  }
}
