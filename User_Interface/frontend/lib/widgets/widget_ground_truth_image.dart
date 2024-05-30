import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_ground_truth_logic.dart';

class GroundTruthImageWidget extends StatefulWidget {
  final GroundTruthImageLogic logic;

  GroundTruthImageWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _GroundTruthImageWidgetState createState() => _GroundTruthImageWidgetState();
}

class _GroundTruthImageWidgetState extends State<GroundTruthImageWidget> {

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
