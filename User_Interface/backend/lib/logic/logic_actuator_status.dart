import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class ActuatorStatusLogic extends StatusLogic {
  var running = false;

  ActuatorStatusLogic({queueName}) : super(queueName ?? "actuator");

  void toggle() {
    print("ActuatorStatusLogic toggle");

    if (running) {
      sendStop();
    } else {
      sendStart();
    }
  }

  void sendStart() {
    super.sendCommand("START");
  }

  void sendStop() {
    super.sendCommand("STOP");
  }

  void sendShutdown() {
    super.sendCommand("SHUTDOWN");
  }

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    print(" [A] Received string: ${message.payloadAsString}");
  }
}