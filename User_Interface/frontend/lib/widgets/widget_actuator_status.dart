import 'package:flutter/material.dart';

import 'package:frontend/logic/logic_actuator_status.dart';

class DataPointsWidget extends StatefulWidget {
  final ActuatorStatusLogic logic;

  DataPointsWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _DataPointsWidgetState createState() => _DataPointsWidgetState();
}

class _DataPointsWidgetState extends State<DataPointsWidget> {
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
    widget.logic.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: <Widget>[
            Text("${widget.logic.json}"),
            Table(
              children: [
                TableRow(
                  children: [
                    Text('Status'),
                    Text('Position'),
                    Text('Drilling'),
                    Text('Extend'),
                    Text('Angle'),
                    Text('json'),
                  ],
                ),
                TableRow(
                  children: [
                    Text(widget.logic.running ? 'Running' : 'Stopped'),
                    Text("${widget.logic.json['position']}"),
                    Text("${widget.logic.json['drilling']}"),
                    Text("${widget.logic.json['extend']}"),
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
                          Text('Historical Data ${index + 1}'),
                          Text("${widget.logic.historicalData[index]['position']}"),
                          Text("${widget.logic.historicalData[index]['drilling']}"),
                          Text("${widget.logic.historicalData[index]['extend']}"),
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
      ),
    );
  }
}
