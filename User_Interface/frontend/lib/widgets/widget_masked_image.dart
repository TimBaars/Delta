import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_masked_image.dart';

class MaskedImageWidget extends StatefulWidget {
  final MaskedImageLogic logic;

  MaskedImageWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _MaskedImageWidgetState createState() =>
      _MaskedImageWidgetState();
}

class _MaskedImageWidgetState extends State<MaskedImageWidget> {
  @override
  void initState() {
    super.initState();

    widget.logic.function.add(() {
      setState(() {});
      return {};
    });
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
        Positioned(child: Text('Masked Image', style: TextStyle(fontSize: 16.0), textAlign: TextAlign.center), top: 0, left: 0, right: 0),
      ],
    );
  }
}
