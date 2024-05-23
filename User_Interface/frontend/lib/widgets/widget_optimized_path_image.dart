import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_optimized_path_image.dart';

class OptimizedPathImageWidget extends StatefulWidget {
  final OptimizedPathImageLogic logic;

  OptimizedPathImageWidget({Key? key, required this.logic}) : super(key: key);

  @override
  _OptimizedPathImageWidgetState createState() => _OptimizedPathImageWidgetState();
}

class _OptimizedPathImageWidgetState extends State<OptimizedPathImageWidget> {
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
      ],
    );
  }
}
