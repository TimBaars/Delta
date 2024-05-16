import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class RrtImageLogic extends StatusLogic {
  var running = false;

  RrtImageLogic({queueName}) : super(queueName ?? "rrt");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [R] Received string: ${message.payloadAsString}");
  }
}