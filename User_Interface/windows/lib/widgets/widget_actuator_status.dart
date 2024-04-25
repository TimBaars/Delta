import 'dart:io';
import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/material.dart';

import '../logic/logic_actuator_status.dart';

class ActuatorStatusWidget extends StatefulWidget {
 final ActuatorStatusLogic logic;

 ActuatorStatusWidget({Key? key, required this.logic}) : super(key: key);

 @override
 _ActuatorStatusWidgetState createState() => _ActuatorStatusWidgetState();
}

class _ActuatorStatusWidgetState extends State<ActuatorStatusWidget> {
  late StreamSubscription<FileSystemEvent> _subscription;
 late File _imageFile;
 Uint8List? _imageBytes;

  @override
  void initState() {
    super.initState();
    _imageFile = File("assets/static/images/placeholder_delta_tool_status.png");
    
    _loadImages();
    
    _subscription = _imageFile.parent.watch().listen((event) {
      if (event is FileSystemModifyEvent) {
        _loadImages();
      }
    });
  }

 void _loadImages() async {
    await Future.delayed(Duration(milliseconds: 50));

    try {
      final imageBytes = await _imageFile.readAsBytes();
      setState(() {
        _imageBytes = imageBytes;
      });
    } catch (e) {
      print("[DataPointsOverlayImageWidget] Error loading images: $e");
      _loadImages();
    }
 }

 @override
 void dispose() {
    widget.logic.disable();
    _subscription.cancel();
    super.dispose();
 }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          children: <Widget>[
            Text(widget.logic.running ? 'Running' : 'Stopped'),
            _imageBytes != null ? Image.memory(_imageBytes!) : CircularProgressIndicator(),
          ],
        ),
      ),
    );
  }
}