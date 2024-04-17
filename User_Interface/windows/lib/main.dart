import 'package:flutter/material.dart';
import 'screen/screen_main.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
 @override
 Widget build(BuildContext context) {
    return MaterialApp(
      home: GenericScreen(),
    );
 }
}