import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';

import '../rabbitmq/client.dart';

class DataPointsOverlayImageWidget extends StatefulWidget {
 @override
 _DataPointsOverlayImageWidgetState createState() => _DataPointsOverlayImageWidgetState();
}

class _DataPointsOverlayImageWidgetState extends State<DataPointsOverlayImageWidget> {
 Uint8List? _groundTruthImageBytes;
 Uint8List? _maskedResultImageBytes;
 bool _isProcessingImage = false;

 @override
 void initState() {
    super.initState();
    setupConsumers();
 }

 void setupConsumers() async {
    Consumer groundTruthConsumer = await RabbitMQClient().setupConsumer("ground_truth_image");
    Consumer maskedResultConsumer = await RabbitMQClient().setupConsumer("masked_result_image");

    groundTruthConsumer.listen((AmqpMessage message) {
      print("[GroundTruthImageWidget] Received message: ${message.payloadAsString}");

      if (!_isProcessingImage) {
        _isProcessingImage = true;
        Uint8List imageBytes = Uint8List.fromList(message.payloadAsString.codeUnits);
        setState(() {
          _groundTruthImageBytes = imageBytes;
        });
        message.ack();
        _isProcessingImage = false;
      }
    });

    maskedResultConsumer.listen((AmqpMessage message) {
      print("[MaskedResultImageWidget] Received message: ${message.payloadAsString}");
      
      if (!_isProcessingImage) {
        _isProcessingImage = true;
        Uint8List imageBytes = Uint8List.fromList(message.payloadAsString.codeUnits);
        setState(() {
          _maskedResultImageBytes = imageBytes;
        });
        message.ack();
        _isProcessingImage = false;
      }
    });
 }

 @override
 Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Stack(
          alignment: Alignment.center,
          children: <Widget>[
            // Bottom image
            _groundTruthImageBytes != null ? Image.memory(_groundTruthImageBytes!) : CircularProgressIndicator(),
            // Top image with 50% opacity
            Opacity(
              opacity: 0.5,
              child: _maskedResultImageBytes != null ? Image.memory(_maskedResultImageBytes!) : CircularProgressIndicator(),
            ),
          ],
        ),
      ),
    );
 }
}
