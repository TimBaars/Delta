import 'dart:io';

import 'package:dart_amqp/dart_amqp.dart';
import '../rabbitmq/client.dart';
import '../util/constants.dart';

abstract class StatusLogic {
  var initialized = false;
  var initializing = false;
  final String queueName;
  late final Consumer consumer;
  String lastData = "";

  StatusLogic(this.queueName) {
    init();
  }

  void init() async {
    if (!initializing && !initialized) {
      initializing = true;

      print("Init");
      
      await setupConsumer();

      initialized = true;
      initializing = false;
    }
  }

  Future<void> setupConsumer() async {
    print("$queueName setupConsumer");

    consumer = await RabbitMQClient().setupConsumer(queueName);
    
    consumer.listen(listener);
  }

  void publish(String message) async {
    print("$queueName publish");

    Socket socket = await Socket.connect(RMQHOST, RMQPORT);

    socket.write("PUBLISH $queueName $message");
  }

  void dispose() {
    print("$queueName dispose");

    consumer.cancel();
  }

  void sendCommand(String command) {
    print("$queueName sendCommand");

    publish(command);
  }

  String retrieveLastData() {
    return lastData;
  }

  void listener(AmqpMessage message) {
    lastData = message.payloadAsString;
  }
}