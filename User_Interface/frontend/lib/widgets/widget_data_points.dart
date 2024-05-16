import 'package:flutter/material.dart';

import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_data_points_actuator.dart';
import 'package:frontend/widgets/widget_data_points_delta.dart';
import 'package:frontend/widgets/widget_data_points_system.dart';

class DataPointsWidget extends StatefulWidget {
  final SystemStatusLogic logic;

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
    return Column(
      children: <Widget>[
        DataPointsSystemWidget(logic: widget.logic),
        DataPointsActuatorWidget(logic: widget.logic.actuatorStatusLogic, useHistoricalData: true),
        DataPointsDeltaWidget(logic: widget.logic.deltaStatusLogic, useHistoricalData: true),
      ],
    );
  }
}
