import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class SystemStatusLogic extends StatusLogic {
  var running = false;

  SystemStatusLogic({queueName}) : super(queueName ?? "system");

  void toggle() {
    print("System toggle");

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

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [S] Received string: ${message.payloadAsString}");
  }
}