import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class DeltaStatusLogic extends StatusLogic {
  var running = false;

  DeltaStatusLogic({queueName}) : super(queueName ?? "delta");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [D] Received string: ${message.payloadAsString}");
  }
}