import 'package:flutter/material.dart';
import 'package:ui/rabbitmq/client.dart';
import 'package:ui/screen/screen_main.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  void init() {
    RabbitMQClient().initialize();
  }

  @override
  Widget build(BuildContext context) {
    init();

    return MaterialApp(
      title: "Delta UI",
      home: MainScreen(),

      // home: GenericScreen(),
      // home: AllScreen(),
      // home: PathFindingScreen(),
      // home: ControllerScreen(),
    );
  }

  void dispose() {
    RabbitMQClient client = RabbitMQClient();
    client.close();
  }
}
