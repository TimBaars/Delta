import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class DeltaStatusLogic extends StatusLogic {
  var running = false;

  DeltaStatusLogic({queueName}) : super(queueName ?? "delta");

  void toggle() {
    print("DeltaStatusLogic toggle");

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

    print(" [D] Received string: ${message.payloadAsString}");
  }
}