import 'dart:io';
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class DataPointsOverlayImageWidget extends StatefulWidget {
 @override
 _DataPointsOverlayImageWidgetState createState() => _DataPointsOverlayImageWidgetState();
}

class _DataPointsOverlayImageWidgetState extends State<DataPointsOverlayImageWidget> {
 late StreamSubscription<FileSystemEvent> _subscription;
 late File _groundTruthImageFile;
 late File _maskedResultImageFile;
 Uint8List? _groundTruthImageBytes;
 Uint8List? _maskedResultImageBytes;

 @override
 void initState() {
    super.initState();
    _groundTruthImageFile = File("assets/images/ground_thruth_image.png");
    _maskedResultImageFile = File("assets/images/masked_result_image.png");
    
    _loadImages();
    
    _subscription = _groundTruthImageFile.parent.watch().listen((event) {
      if (event is FileSystemModifyEvent) {
        _loadImages(); // Reload the images when the file changes
      }
    });
 }

 void _loadImages() async {
    await Future.delayed(Duration(milliseconds: 50));

    try {
      final groundTruthBytes = await _groundTruthImageFile.readAsBytes();
      final maskedResultBytes = await _maskedResultImageFile.readAsBytes();
      setState(() {
        _groundTruthImageBytes = groundTruthBytes;
        _maskedResultImageBytes = maskedResultBytes;
      });
    } catch (e) {
      print("[DataPointsOverlayImageWidget] Error loading images: $e");
      _loadImages();
    }
 }

 @override
 void dispose() {
    _subscription.cancel();
    super.dispose();
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
