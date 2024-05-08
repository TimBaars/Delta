import 'package:flutter/material.dart';
import 'package:web_socket_channel/io.dart';

import 'package:frontend/util/constants.dart';

class WebSocketDemo extends StatefulWidget {
  @override
  _WebSocketDemoState createState() => _WebSocketDemoState();
}

class _WebSocketDemoState extends State<WebSocketDemo> {
  late IOWebSocketChannel channel;

  @override
  void initState() {
    super.initState();
    channel = IOWebSocketChannel.connect(WSHOST);
    channel.stream.listen((message) {
      // Update UI with new message
    });
  }

  @override
  void dispose() {
    channel.sink.close();
    super.dispose();
  }

  void sendMessage(String message) {
    channel.sink.add(message);
  }

  @override
  Widget build(BuildContext context) {
    return Center(
      child: ElevatedButton(
        onPressed: () {
          sendMessage('Hello from frontend!');
        },
        child: Text('Send Message'),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: Scaffold(
      appBar: AppBar(
        title: Text('WebSocket Demo'),
      ),
      body: WebSocketDemo(),
    ),
  ));
}