import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_data_points.dart';

class DataScreen extends StatelessWidget {
  final SystemStatusLogic logic = SystemStatusLogic();

  DataScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          children: <Widget>[
            Expanded(child: DataPointsWidget(logic: logic)),
          ],
        ),
      ),
    );
  }
}
