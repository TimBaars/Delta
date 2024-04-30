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
    Consumer groundTruthImageConsumer =
        await RabbitMQClient().setupConsumer("ground_truth_image");

    groundTruthImageConsumer.listen((AmqpMessage message) async {
      print("[GroundThruthImageWidget] Received message: ${message.payloadAsString}");

      if (!_isProcessingImage) {
        _isProcessingImage = true;
        // Parse the JSON string to get the URL
        Map<String, dynamic> json = jsonDecode(message.payloadAsString);
        print("JSON: $json");
        String imageUrl = json['url'];

        try {
          // Fetch the image from the URL
          print("Fetching image from URL: $imageUrl");
          http.Response response = await http.get(Uri.parse(imageUrl));
          print("Response status code: ${response.statusCode}");
          if (response.statusCode == 200) {
            // Check if the entire image has been downloaded
            String? contentLength = response.headers['content-length'];
            if (contentLength != null &&
                int.parse(contentLength) == response.bodyBytes.length) {
              // Convert the response body to Uint8List
              Uint8List imageBytes = response.bodyBytes;
              setState(() {
                _imageBytes = imageBytes;
              });
            } else {
              print("Image not fully downloaded");
            }
          } else {
            print("Failed to load image from URL");
          }
        } catch (e) {
          print("Error fetching image: $e");
        } finally {
          message.ack();
          _isProcessingImage = false;
        }
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
