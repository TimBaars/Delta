import 'dart:convert';
import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import '../rabbitmq/client.dart';

class GroundThruthImageWidget extends StatefulWidget {
  @override
  _GroundThruthImageWidgetState createState() =>
      _GroundThruthImageWidgetState();
}

class _GroundThruthImageWidgetState extends State<GroundThruthImageWidget> {
  Uint8List? _imageBytes;
  bool _isProcessingImage = false;

  @override
  void initState() {
    super.initState();
    setupConsumer();
  }

  void setupConsumer() async {
    Consumer groundTruthImageConsumer =await RabbitMQClient().setupConsumer("ground_truth_image");

    groundTruthImageConsumer.listen((AmqpMessage message) async {
      print("[GroundThruthImageWidget] Received message: ${message.payloadAsString}");

      if (!_isProcessingImage) {
        _isProcessingImage = true;
        // Parse the JSON string to get the URL
        Map<String, dynamic> json = jsonDecode(message.payloadAsString);
        String imageUrl = json['url'];

        // Fetch the image from the URL
        http.Response response = await http.get(Uri.parse(imageUrl));
        if (response.statusCode == 200) {
          // Convert the response body to Uint8List
          Uint8List imageBytes = response.bodyBytes;
          setState(() {
            _imageBytes = imageBytes;
          });
        } else {
          print("Failed to load image from URL");
        }
        message.ack();
        _isProcessingImage = false;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return _imageBytes != null
        ? Image.memory(_imageBytes!)
        : const CircularProgressIndicator();
  }
}
