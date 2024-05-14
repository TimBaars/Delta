import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class ActuatorStatusLogic extends StatusLogic {
  var running = false;

  ActuatorStatusLogic({queueName}) : super(queueName ?? "actuator");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [A] Received string: ${message.payloadAsString}");
  }
}