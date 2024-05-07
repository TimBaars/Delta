import 'package:backend/application/application.dart';
import 'package:dart_amqp/dart_amqp.dart';

void main() async {
  Application app = Application();

  app.endpoint();
}