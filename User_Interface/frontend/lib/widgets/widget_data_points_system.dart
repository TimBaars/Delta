import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';

class DataPointsSystemWidget extends StatefulWidget {
  final SystemStatusLogic logic;

  DataPointsSystemWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _DataPointsSystemWidgetState createState() => _DataPointsSystemWidgetState();
}

class _DataPointsSystemWidgetState extends State<DataPointsSystemWidget> {
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
    widget.logic.function = () => {};
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Title(
          color: Colors.black,
          child: Text('System Data',
              style: TextStyle(fontSize: 24.0, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center),
        ),
          Table(
            children: [
              TableRow(
                children: [
                  Text('Running',
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
                  Text("${widget.logic.running}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                  Text("${widget.logic.json}",
                      style: TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),
            ],
          ),
      ],
    );
  }
}
