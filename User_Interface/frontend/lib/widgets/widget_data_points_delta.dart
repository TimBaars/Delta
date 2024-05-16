import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_delta_status.dart';

class DataPointsDeltaWidget extends StatefulWidget {
  final DeltaStatusLogic logic;
  final bool useHistoricalData;

  DataPointsDeltaWidget(
      {Key? key, required this.logic, required this.useHistoricalData})
      : super(key: key);

  @override
  _DataPointsDeltaWidgetState createState() =>
      _DataPointsDeltaWidgetState();
}

class _DataPointsDeltaWidgetState extends State<DataPointsDeltaWidget> {
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
          Title(
            color: Colors.black,
            child: Text('Delta Data',
                style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center),
          ),
          Table(
            children: [
              TableRow(
                children: [
                  Text('Position',
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 18.0)),
                  Text('Moving',
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
                  Text("${widget.logic.json['position']}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("${widget.logic.json['moving']}",
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
                                "${widget.logic.historicalData[size - index]['position']}"),
                            Text(
                                "${widget.logic.historicalData[size - index]['moving']}"),
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
