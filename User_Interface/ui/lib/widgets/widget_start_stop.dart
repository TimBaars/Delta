import 'package:flutter/material.dart';
import 'package:dart_amqp/dart_amqp.dart';

import '../rabbitmq/client.dart';

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
    setupConsumer();
 }

 void setupConsumer() async {
    Consumer robotStatusConsumer = await RabbitMQClient().setupConsumer("robot_status");

    robotStatusConsumer.listen((AmqpMessage message) {
      if (message.payloadAsString == "running") {
        setState(() {
          _isRobotRunning = true;
          _buttonTextController.text = "Stop";
        });
      } else if (message.payloadAsString == "stopped") {
        setState(() {
          _isRobotRunning = false;
          _buttonTextController.text = "Start";
        });
      }
      message.ack();
    });
 }

 void _onButtonClick() {
    if (!_callbackReceived) {
      print("Previous callback not received yet.");
      return;
    }

    _callbackReceived = false;

    if (_isRobotRunning) {
      // Stop the robot
      print("Stopping the robot...");
      RabbitMQClient().publish("robot_control", "", "stop");
    } else {
      // Start the robot
      print("Starting the robot...");
      RabbitMQClient().publish("robot_control", "", "start");
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
