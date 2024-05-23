import 'package:dart_amqp/dart_amqp.dart';
import 'logic_status.dart';

class OptimizedPathImageLogic extends StatusLogic {
  var running = false;

  OptimizedPathImageLogic({queueName}) : super(queueName ?? "optimized_path");

  @override
  void listener(AmqpMessage message) {
    super.listener(message);

    // print(" [O] Received string: ${message.payloadAsString}");
  }
}