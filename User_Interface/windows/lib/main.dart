import 'package:flutter/material.dart';
import 'package:windows/rabbitmq/client.dart';
import 'package:windows/screen/screen_main.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  void init() async {
    print(String.fromEnvironment('APIKEY', defaultValue: ''));

    var host = String.fromEnvironment('RABBITMQ_HOST', defaultValue: '192.168.178.170');
    var username = String.fromEnvironment('RABBITMQ_USERNAME', defaultValue: 'rabbitmq');
    var password = String.fromEnvironment('RABBITMQ_PASSWORD', defaultValue: 'orangepi');

    print('Connecting to RabbitMQ at $host with $username:$password');

    RabbitMQClient().initialize(host, username, password);
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
