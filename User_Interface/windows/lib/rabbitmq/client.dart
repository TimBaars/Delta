import 'package:dart_amqp/dart_amqp.dart';

import 'package:windows/util/constants.dart';

class RabbitMQClient {
  static final RabbitMQClient _singleton = RabbitMQClient._internal();
  late Client _client;
  late Channel _channel;

  factory RabbitMQClient() {
    return _singleton;
  }

  RabbitMQClient._internal();

  Future<void> initialize({host, username, password}) async {
    ConnectionSettings settings = ConnectionSettings(
      host: host ?? RMQHOST,
      authProvider: PlainAuthenticator(username ?? RMQUSERNAME, password ?? RMQPASSWORD),
    );
    _client = Client(settings: settings);
    _channel = await _client.channel();
  }

  Future<void> close() async {
    await _client.close();
  }

  Future<Consumer> setupConsumer(String queueName) async {
    Exchange exchange = await _channel.exchange(queueName, ExchangeType.TOPIC);
    Queue queue = await _channel.queue(queueName);
    print("Queue $queueName declared");
    await queue.bind(exchange, "");
    return await queue.consume();
  }

  Future<void> publish(String exchangeName, String routingKey, String message) async {
    Exchange exchange = await _channel.exchange(exchangeName, ExchangeType.FANOUT);
    exchange.publish(message, routingKey);
  }
}