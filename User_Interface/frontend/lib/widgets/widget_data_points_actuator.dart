import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_actuator_status.dart';

class DataPointsActuatorWidget extends StatefulWidget {
  final ActuatorStatusLogic logic;
  final bool useHistoricalData;

  DataPointsActuatorWidget(
      {Key? key, required this.logic, required this.useHistoricalData})
      : super(key: key);

  @override
  _DataPointsActuatorWidgetState createState() =>
      _DataPointsActuatorWidgetState();
}

class _DataPointsActuatorWidgetState extends State<DataPointsActuatorWidget> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: <Widget>[
          Title(
            color: Colors.black,
            child: Text('Actuator Data',
                style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center),
          ),
          Table(
            children: [
              TableRow(
                children: [
                  Text('Drilling',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 18.0)),
                  Text('Extended',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 18.0)),
                  Text('Angle',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 18.0)),
                  Text('json',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 18.0)),
                ],
              ),
              TableRow(
                decoration: BoxDecoration(
                  color: Colors.grey[200],
                ),
                children: [
                  Text("${widget.logic.json['drilling']}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("${widget.logic.json['extended']}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("${widget.logic.json['angle']}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("${widget.logic.json}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),
            ],
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Icon(Icons.arrow_drop_down),
              Text('Historical Data',
                  style: TextStyle(fontStyle: FontStyle.italic),
                  textAlign: TextAlign.center),
              Icon(Icons.arrow_drop_down),
            ],
          ),
          if (widget.useHistoricalData)
            Expanded(
              child: ListView.builder(
                itemCount: widget.logic.historicalData.length,
                itemBuilder: (context, index) {
                  var size = widget.logic.historicalData.length - 1;
                  bool isEvenRow = index % 2 == 0;

                  return Container(
                    decoration: BoxDecoration(
                      color: isEvenRow ? Colors.grey[200] : Colors.white,
                    ),
                    child: Table(
                      children: [
                        TableRow(
                          decoration: isEvenRow
                              ? BoxDecoration(
                                  color: Colors.grey[100],
                                )
                              : BoxDecoration(),
                          children: [
                            Text(
                                "${widget.logic.historicalData[size - index]['drilling']}"),
                            Text(
                                "${widget.logic.historicalData[size - index]['extended']}"),
                            Text(
                                "${widget.logic.historicalData[size - index]['angle']}"),
                            Text(
                                "${widget.logic.historicalData[size - index]}"),
                          ],
                        ),
                      ],
                    ),
                  );
                },
              ),
            ),
        ],
      ),
    );
  }
}
