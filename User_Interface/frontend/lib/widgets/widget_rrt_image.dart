import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';

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
 }

 @override
 Widget build(BuildContext context) {
    return _imageBytes != null ? Image.memory(_imageBytes!) : CircularProgressIndicator();
 }
}
