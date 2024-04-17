import 'dart:io';
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class GroundThruthImageWidget extends StatefulWidget {
   final String imagePath = "assets/images/ground_thruth_image.png";

 @override
 _GroundThruthImageWidgetState createState() => _GroundThruthImageWidgetState();
}

class _GroundThruthImageWidgetState extends State<GroundThruthImageWidget> {
 late StreamSubscription<FileSystemEvent> _subscription;
 late File _imageFile;
 Uint8List? _imageBytes;

 @override
 void initState() {
    super.initState();
    _imageFile = File(widget.imagePath);
    _loadImage();
    _subscription = _imageFile.parent.watch().listen((event) {
      if (event is FileSystemModifyEvent) {
        _loadImage(); // Reload the image when the file changes
      }
    });
 }

 void _loadImage() async {
    await Future.delayed(Duration(milliseconds: 50));

    try {
        final bytes = await _imageFile.readAsBytes();
        setState(() {
          _imageBytes = bytes;
        });
    } catch (e) {
        print("[GroundThruthImageWidget] Error loading image: $e");
        _loadImage();
    }
 }

 @override
 void dispose() {
    _subscription.cancel();
    super.dispose();
 }

 @override
 Widget build(BuildContext context) {
    return _imageBytes != null ? Image.memory(_imageBytes!) : CircularProgressIndicator();
 }
}