import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';

import '../logic/logic_actuator_status.dart';
import '../rabbitmq/client.dart';

class ActuatorStatusWidget extends StatefulWidget {
 final ActuatorStatusLogic logic;

 ActuatorStatusWidget({Key? key, required this.logic}) : super(key: key);

 @override
 _ActuatorStatusWidgetState createState() => _ActuatorStatusWidgetState();
}

class _ActuatorStatusWidgetState extends State<ActuatorStatusWidget> {
 Uint8List? _imageBytes;
 bool _isProcessingImage = false;

 @override
 void initState() {
    super.initState();
    setupConsumer();
 }

 void setupConsumer() async {
    Consumer actuatorConsumer = await RabbitMQClient().setupConsumer("actuator");

    actuatorConsumer.listen((AmqpMessage message) {
      print("[ActuatorStatusWidget] Received message: ${message.payloadAsString}");

      if (!_isProcessingImage) {
        _isProcessingImage = true;
        Uint8List imageBytes = Uint8List.fromList(message.payloadAsString.codeUnits);
        setState(() {
          _imageBytes = imageBytes;
        });
        message.ack();
        _isProcessingImage = false;
      }
    });
 }

 @override
 void dispose() {
    // widget.logic.disable();
    super.dispose();
 }

 @override
 Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: <Widget>[
            Text(widget.logic.running ? 'Running' : 'Stopped'),
            _imageBytes != null
                ? Image.memory(_imageBytes!)
                : CircularProgressIndicator(),
          ],
        ),
      ),
    );
 }
}
