import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_actuator_status.dart';

class DataPointsActuatorWidget extends StatefulWidget {
  final ActuatorStatusLogic logic;

  DataPointsActuatorWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _DataPointsActuatorWidgetState createState() =>
      _DataPointsActuatorWidgetState();
}

class _DataPointsActuatorWidgetState extends State<DataPointsActuatorWidget> {
  @override
  void initState() {
    super.initState();
    widget.logic.function = () {
      setState(() {});
      return {};
    };
  }

  @override
  void dispose() {
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: <Widget>[
          Table(
            children: [
              TableRow(
                children: [
                  Text('Drilling'),
                  Text('Extended'),
                  Text('Angle'),
                  Text('json'),
                ],
              ),
              TableRow(
                children: [
                  Text("${widget.logic.json['drilling']}"),
                  Text("${widget.logic.json['extended']}"),
                  Text("${widget.logic.json['angle']}"),
                  Text("${widget.logic.json}"),
                ],
              ),
            ],
          ),
          Expanded(
            child: ListView.builder(
              itemCount: widget.logic.historicalData.length,
              itemBuilder: (context, index) {
                return Table(
                  children: [
                    TableRow(
                      children: [
                        Text("${widget.logic.historicalData[index]['drilling']}"),
                        Text("${widget.logic.historicalData[index]['extended']}"),
                        Text("${widget.logic.historicalData[index]['angle']}"),
                        Text("${widget.logic.historicalData[index]}"),
                      ],
                    ),
                  ],
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
