import 'package:flutter/material.dart';
import 'package:frontend/screen/screen_data.dart';
import 'package:frontend/screen/screen_main.dart';

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
      // home: DataScreen(),
    );
  }
}
