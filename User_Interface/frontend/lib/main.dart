import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/screen/screen_main.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  
  @override
  Widget build(BuildContext context) {
    SystemStatusLogic().init();

    return MaterialApp(
      title: "Delta UI",
      home: MainScreen(),
    );
  }
}
