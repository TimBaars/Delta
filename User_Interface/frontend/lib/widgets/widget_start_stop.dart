import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';

class DeltaRobotStatusButtonWidget extends StatefulWidget {
  final SystemStatusLogic logic;

  DeltaRobotStatusButtonWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _DeltaRobotStatusButtonWidgetState createState() =>
      _DeltaRobotStatusButtonWidgetState();
}

class _DeltaRobotStatusButtonWidgetState extends State<DeltaRobotStatusButtonWidget> {
  final TextEditingController _buttonTextController = TextEditingController();

  @override
  void initState() {
    super.initState();

    widget.logic.function = () {
      setState(() {});
      return {};
    };
  }

  void _onButtonClick() {
    if (widget.logic.running) {
      widget.logic.stop();
    } else {
      widget.logic.start();
    }
  }

  @override
  Widget build(BuildContext context) {
    _buttonTextController.text = widget.logic.running ? "Stop" : "Start";

    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: <Widget>[
        ElevatedButton(
          onPressed: _onButtonClick,
          child: Text(_buttonTextController.text),
        ),
      ],
    );
  }
}
