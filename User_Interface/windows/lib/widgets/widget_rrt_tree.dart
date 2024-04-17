import 'dart:io';
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class RrtTreeImageWidget extends StatefulWidget {
   final String imagePath = "assets/images/rrt_tree_image.png";

 @override
 _RrtTreeImageWidgetState createState() => _RrtTreeImageWidgetState();
}

class _RrtTreeImageWidgetState extends State<RrtTreeImageWidget> {
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
        print("[RrtTreeImageWidget] Error loading image: $e");
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