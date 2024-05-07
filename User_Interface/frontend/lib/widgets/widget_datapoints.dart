import 'dart:typed_data';
import 'package:dart_amqp/dart_amqp.dart';
import 'package:flutter/material.dart';

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
