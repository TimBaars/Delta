import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_data_points.dart';

class DataScreen extends StatefulWidget {
  DataScreen({super.key});

  @override
  _DataScreen createState() => _DataScreen();
}

class _DataScreen extends State<DataScreen> {
  late final SystemStatusLogic logic = SystemStatusLogic();
  _DataScreen();
  
  @override
  void initState() {
    super.initState();
    logic.function = () {
      setState(() {});
      return {};
    };
  }

  @override
  void dispose() {
    super.dispose();
    logic.function = () => {};
  }

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
