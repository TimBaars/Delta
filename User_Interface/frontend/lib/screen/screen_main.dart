import 'package:flutter/material.dart';
import 'package:frontend/screen/screen_combi.dart';
import 'package:frontend/screen/screen_controllers.dart';
import 'package:frontend/screen/screen_crosslink.dart';
import 'package:frontend/screen/screen_data.dart';
import 'package:frontend/screen/screen_pathfinding.dart';
import 'package:frontend/widgets/widget_ground_thruth_stream.dart';
import 'package:frontend/widgets/widget_navigatorbutton.dart';

class MainScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Main Screen'),
      ),
      body: Row(
        children: [
          Expanded(
            flex: 8,
            child: GroundThruthStreamWidget(),
          ),
          const Expanded(
            flex: 1,
            child: Column()
          ),
          Expanded(
            flex: 2,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Pathfinding", Icons.approval_rounded, PathFindingScreen())),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Cameraview", Icons.video_camera_back_outlined, AllScreen())),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Controllers", Icons.addchart_sharp, ControllerScreen())),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Datachannel", Icons.numbers_rounded, DataScreen())),
                const Expanded(flex:1, child: Text("")),
              ],
            ),
          ),
          const Expanded(
            flex: 1,
            child: Column()
          ),
        ],
      )
    );
  }
}