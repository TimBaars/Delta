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
  int lastDataReceived = 0;

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

  Future<String> retrieveLastData(int timestamp, {int counter = 0}) async {
    if (lastDataReceived > timestamp) {
      return lastData;
    } else {
      if (counter > 100) {
        return "";
      }

      await Future.delayed(Duration(milliseconds: 50));

      return retrieveLastData(timestamp, counter: counter + 1);
    }
  }

  bool setData(String data, int timestamp) {
    if (timestamp < lastDataReceived) {
      return false;
    }

    lastData = data;
    lastDataReceived = timestamp;

    return true;
  }

  void listener(AmqpMessage message) {
    if (lastData != message.payloadAsString) {
      lastData = message.payloadAsString;
      lastDataReceived = DateTime.now().toUtc().millisecondsSinceEpoch;

      print("Data was new, re-uploaded the data to ensure all channels receive the data");
      publish(lastData);
    }
  }
}