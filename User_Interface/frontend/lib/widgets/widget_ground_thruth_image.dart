import 'dart:convert';
import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

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
  }

  @override
  Widget build(BuildContext context) {
    return _imageBytes != null
        ? Image.memory(_imageBytes!)
        : const CircularProgressIndicator();
  }
}
