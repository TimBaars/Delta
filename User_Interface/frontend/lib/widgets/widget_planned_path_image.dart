import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_planned_path_image.dart';

class PlannedPathImageWidget extends StatefulWidget {
  final PlannedPathImageLogic logic;

  PlannedPathImageWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _PlannedPathImageWidgetState createState() => _PlannedPathImageWidgetState();
}

class _PlannedPathImageWidgetState extends State<PlannedPathImageWidget> {
  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        const Center(child: CircularProgressIndicator()),
        if (widget.logic.imageCache.lastImage != null)
          Center(child: Image.memory(widget.logic.imageCache.lastImage!)),
        if (widget.logic.imageCache.secondLastImage != null)
          Center(child: Image.memory(widget.logic.imageCache.secondLastImage!)),
      ],
    );
  }
}
