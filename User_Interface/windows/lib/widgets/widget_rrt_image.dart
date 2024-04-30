import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';

import '../rabbitmq/client.dart';

class RrtImageWidget extends StatefulWidget {
 @override
 _RrtImageWidgetState createState() => _RrtImageWidgetState();
}

class _RrtImageWidgetState extends State<RrtImageWidget> {
 Uint8List? _imageBytes;
 bool _isProcessingImage = false;

 @override
 void initState() {
    super.initState();
    setupConsumer();
 }

 void setupConsumer() async {
    Consumer rrtTreeImageConsumer = await RabbitMQClient().setupConsumer("rrt_tree_image");

    rrtTreeImageConsumer.listen((AmqpMessage message) {
      print("[RrtImageWidget] Received message: ${message.payloadAsString}");

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
 Widget build(BuildContext context) {
    return _imageBytes != null ? Image.memory(_imageBytes!) : CircularProgressIndicator();
 }
}
