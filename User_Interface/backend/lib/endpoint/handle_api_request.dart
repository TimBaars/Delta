import '../application/application.dart';
import 'package:shelf/shelf.dart';

Response HandleApiRequests(Request request) {
  String? jsonData = null;

  if (request.url.path == 'actuator') {
    jsonData = Application().getActuatorStatus();
  }
  if (request.url.path == 'delta') {
    jsonData = Application().getRobotStatus();
  }
  // ToDo expand with more endpoint handlers

  if (jsonData != null) {
    return Response.ok(jsonData, headers: {'Content-Type': 'application/json'});
  }

  return Response.notFound('Not Found');
}