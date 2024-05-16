import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_ground_truth_image.dart';
import 'package:frontend/widgets/widget_masked_image.dart';
import '../widgets/widget_rrt_image.dart';

class PathFindingScreen extends StatelessWidget {
  final SystemStatusLogic logic = SystemStatusLogic();

  PathFindingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Path Finding'),
      ),
      body: Row(
        children: <Widget>[
          Expanded(child: GroundTruthImageWidget(logic: logic.groundTruthImageLogic)),
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(child: MaskedImageWidget(logic: logic.maskedImageLogic)),
                Expanded(child: RrtImageWidget(logic: logic.rrtImageLogic)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
