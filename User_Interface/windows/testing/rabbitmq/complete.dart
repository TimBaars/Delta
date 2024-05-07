import 'package:dart_amqp/dart_amqp.dart';
import 'package:uuid/uuid.dart';

void main() async {
  // Connection settings
  ConnectionSettings settings = ConnectionSettings(
    host: "192.168.178.170",
    authProvider: PlainAuthenticator("rabbitmq", "orangepi"),
  );

  // Create a client with the specified settings
  Client client = Client(settings: settings);

  // Open a channel
  Channel channel = await client.channel();

  // Declare a fanout exchange
  Exchange exchange = await channel.exchange("complete", ExchangeType.FANOUT);

  // Declare a queue
  Queue queue = await channel.queue("actuator");

  // Bind the queue to the exchange
  await queue.bind(exchange, "");

  // Start consuming messages from the queue
  Consumer consumer = await queue.consume();
  consumer.listen((AmqpMessage message) {
    print(" [x] Received string: ${message.payloadAsString}");
    message.ack();
  });

  // Publish a message to the exchange
  exchange.publish("A Hello, World!", "");
  exchange.publish("A World!", "");
  exchange.publish("A Hello!", "");
  exchange.publish("A Hello, World!", "");
  exchange.publish("A !", "");

  // Close the client after a delay to allow the message to be processed
  await Future.delayed(Duration(seconds: 100));
  client.close();
}
