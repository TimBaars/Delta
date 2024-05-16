import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class MaskedImageLogic extends StatusLogic {
  var running = false;

  MaskedImageLogic({queueName}) : super(queueName ?? "masked");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [M] Received string: ${message.payloadAsString}");
  }
}