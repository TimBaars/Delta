import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_rrt_image.dart';

class RrtImageWidget extends StatefulWidget {
  final RrtImageLogic logic;

  RrtImageWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _RrtImageWidgetState createState() => _RrtImageWidgetState();
}

class _RrtImageWidgetState extends State<RrtImageWidget> {
  @override
  void initState() {
    super.initState();

    widget.logic.function = () {
      setState(() {});
      return {};
    };
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        const Center(child: CircularProgressIndicator()),
        if (widget.logic.imageCache.lastImage != null)
          Center(child: Image.memory(widget.logic.imageCache.lastImage!)),
        if (widget.logic.imageCache.secondLastImage != null)
          Center(child: Image.memory(widget.logic.imageCache.secondLastImage!)),
        Positioned(child: Text('RRT Image', style: TextStyle(fontSize: 16.0), textAlign: TextAlign.center), top: 0, left: 0, right: 0),
      ],
    );
  }
}
