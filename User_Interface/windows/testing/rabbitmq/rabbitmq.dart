import 'package:dart_amqp/dart_amqp.dart';

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

  // Declare exchanges for each queue
  Exchange actuatorExchange = await channel.exchange("actuator", ExchangeType.FANOUT);
  // Exchange robotExchange = await channel.exchange("robot", ExchangeType.FANOUT);
  // Exchange maskedImageExchange = await channel.exchange("masked_image", ExchangeType.FANOUT);
  // Exchange groundTruthImageExchange = await channel.exchange("ground_truth_image", ExchangeType.FANOUT);
  // Exchange rrtImageExchange = await channel.exchange("rrt_image", ExchangeType.FANOUT);
  // Exchange statusOverrideExchange = await channel.exchange("status_override", ExchangeType.FANOUT);

  // Send dummy data to each queue
  actuatorExchange.publish("{\"activated\": true, \"extended\": 50}", "");
  // robotExchange.publish("{\"position\": {\"x\": 10, \"y\": 20, \"z\": 30}, \"in_movement\": false}", "");
  // maskedImageExchange.publish("{\"url\": \"http://192.168.178.170/static/images/masked_result_image.png\"}", "");
  // groundTruthImageExchange.publish("{\"url\": \"http://192.168.178.170/static/images/ground_truth_image.png\"}", "");
  // rrtImageExchange.publish("{\"url\": \"http://192.168.178.170/static/images/rrt_tree_image.png\"}", "");
  // statusOverrideExchange.publish("{\"status\": \"start\"}", "");

  print("done");

  // Close the client
  client.close();
}
