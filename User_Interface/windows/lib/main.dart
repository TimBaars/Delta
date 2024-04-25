import 'package:flutter/material.dart';
import 'package:windows/screen/screen_main.dart';

// Temp Individual Tests
import 'package:windows/screen/screen_crosslink.dart';
import 'package:windows/screen/screen_pathfinding.dart';
import 'package:windows/screen/screen_controllers.dart';
import 'package:windows/screen/screen_combi.dart';
void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
 @override
 Widget build(BuildContext context) {
    return MaterialApp(
      title: "Delta UI",
      home: MainScreen(),
      
      // home: GenericScreen(),
      // home: AllScreen(),
      // home: PathFindingScreen(),
      // home: ControllerScreen(),
    );
 }
}