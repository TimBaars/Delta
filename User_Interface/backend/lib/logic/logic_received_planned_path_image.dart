import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class PlannedPathImageLogic extends StatusLogic {
  var running = false;

  PlannedPathImageLogic({queueName}) : super(queueName ?? "planned_path");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [P] Received string: ${message.payloadAsString}");
  }
}