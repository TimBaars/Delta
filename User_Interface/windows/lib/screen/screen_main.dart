import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:windows/screen/screen_combi.dart';
import 'package:windows/screen/screen_controllers.dart';
import 'package:windows/screen/screen_crosslink.dart';
import 'package:windows/screen/screen_pathfinding.dart';
import 'package:windows/widgets/widget_ground_thruth_image.dart';
import 'package:windows/widgets/widget_navigatorbutton.dart';

class MainScreen extends StatelessWidget {
  late final PathFindingScreen _pathFindingScreen;
  late final AllScreen _allScreen;
  late final ControllerScreen _controllerScreen;
  
  MainScreen() {
    _pathFindingScreen = PathFindingScreen();
    _allScreen = AllScreen();
    _controllerScreen = ControllerScreen();
  }

  @override
  Widget build(BuildContext context) {
    _controllerScreen.logic.disable();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Main Screen'),
      ),
      body: Row(
        children: [
          Expanded(
            flex: 8,
            child: GroundThruthImageWidget(),
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
                Expanded(flex:2, child: NavigatorButtonWidget("Pathfinding", Icons.approval_rounded, _pathFindingScreen)),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Cameraview", Icons.video_camera_back_outlined, _allScreen)),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Controllers", Icons.addchart_sharp, _controllerScreen, function: () => print("Controllers Screen"))),
                const Expanded(flex:1, child: Text("")),
                Expanded(flex:2, child: NavigatorButtonWidget("Controllers", Icons.numbers_rounded, GenericScreen())),
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