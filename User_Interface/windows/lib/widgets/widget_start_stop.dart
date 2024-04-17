import 'package:flutter/material.dart';
import 'package:windows/logic/logic_start_stop.dart';

class RobotStatusButtonWidget extends StatefulWidget {
  @override
  _RobotStatusButtonWidgetState createState() => _RobotStatusButtonWidgetState();
}

class _RobotStatusButtonWidgetState extends State<RobotStatusButtonWidget> {
  final TextEditingController _buttonTextController = TextEditingController();
  bool _isRobotRunning = false;
  bool _callbackReceived = true;

  void _onButtonClick() {
    if (!_callbackReceived) {
      print("Previous callback not received yet.");
      return;
    }

    _callbackReceived = false;

    if (_isRobotRunning) {
      // Stop the robot
      print("Stopping the robot...");

      LogicStartStop.stop().then((x) => callbackReceived(x));
    } else {
      // Start the robot
      print("Starting the robot...");

      LogicStartStop.start().then((x) => callbackReceived(x));
    }
  }

  void callbackReceived(bool result) {
    if (result) {
      _isRobotRunning = !_isRobotRunning;
    } else {
      print("Error starting/stopping the robot.");
    }

    setState(() {
      _buttonTextController.text = LogicStartStop.getButtonText(_isRobotRunning);
    });

    _callbackReceived = true;
  }

  @override
  Widget build(BuildContext context) {
    _buttonTextController.text = _isRobotRunning ? "Stop" : "Start";

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