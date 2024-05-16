import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class GroundTruthImageLogic extends StatusLogic {
  var running = false;

  GroundTruthImageLogic({queueName}) : super(queueName ?? "ground_truth");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [G] Received string: ${message.payloadAsString}");
  }
}