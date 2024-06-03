import 'package:dart_amqp/dart_amqp.dart';
import 'package:uuid/uuid.dart';

import '../util/constants.dart';

class RabbitMQClient {
  static final RabbitMQClient _singleton = RabbitMQClient._internal();
  static bool isInitialized = false;
  static bool isInitializing = false;
  late Client _client;
  late Channel _channel;
  final String identifier = "dart-${const Uuid().v4()}";

  factory RabbitMQClient() {
    return _singleton;
  }

  RabbitMQClient._internal();

  Future<void> initialize({host, username, password}) async {
    if (!isInitializing && !isInitialized) {
      print("Initializing RabbitMQClient");

      isInitializing = true;
      ConnectionSettings settings = ConnectionSettings(
        host: host ?? RMQHOST,
        authProvider: PlainAuthenticator(username ?? RMQUSERNAME, password ?? RMQPASSWORD),
        connectionName: identifier,
      );
      _client = Client(settings: settings);
      _channel = await _client.channel();

      isInitialized = true;
    } else if (!isInitialized && isInitializing) {
      await Future.delayed(Duration(milliseconds: 200));

      await initialize(host: host, username: username, password: password);
    }
  }

  Future<void> close() async {
    await _client.close();
  }

  Future<void> clientIsInitialized() async {
    if (!isInitialized) {
      await initialize();
    }
  }

  Future<Consumer> setupConsumer(String exchangeName) async {
    await clientIsInitialized();

    Exchange exchange = await _channel.exchange(exchangeName, ExchangeType.FANOUT);
    Queue queue = await _channel.queue('', autoDelete: true); 
    await queue.bind(exchange, "");
    return await queue.consume();
  }

  Future<void> publish(String exchangeName, String routingKey, String message) async {
    await clientIsInitialized();

    Exchange exchange = await _channel.exchange(exchangeName, ExchangeType.FANOUT);
    exchange.publish(message, routingKey);
  }
}
