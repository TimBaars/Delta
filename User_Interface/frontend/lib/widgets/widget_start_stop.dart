import 'package:flutter/material.dart';
import 'package:dart_amqp/dart_amqp.dart';

class RobotStatusButtonWidget extends StatefulWidget {
 @override
 _RobotStatusButtonWidgetState createState() => _RobotStatusButtonWidgetState();
}

class _RobotStatusButtonWidgetState extends State<RobotStatusButtonWidget> {
 final TextEditingController _buttonTextController = TextEditingController();
 bool _isRobotRunning = false;
 bool _callbackReceived = true;

 @override
 void initState() {
    super.initState();
 }

 void _onButtonClick() {
    if (!_callbackReceived) {
      print("Previous callback not received yet.");
      return;
    }

    _callbackReceived = false;

    if (_isRobotRunning) {
      
    } else {
      
    }
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
