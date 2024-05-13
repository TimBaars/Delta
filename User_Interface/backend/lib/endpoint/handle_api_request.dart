import '../application/application.dart';
import 'package:shelf/shelf.dart';

Response HandleApiRequests(Request request) {
  String? jsonData = null;

  var urlPath = request.url.path.split('/').last;

  if (urlPath == 'actuator') {
    jsonData = Application().getActuatorStatus();
  }
  if (urlPath == 'delta') {
    jsonData = Application().getRobotStatus();
  }
  if (urlPath == 'masked') {
    jsonData = Application().getMaskedImage();
  }
  if (urlPath == 'rrt') {
    jsonData = Application().getRrtImage();
  }
  if (urlPath == 'system') {
    jsonData = Application().getSystemStatus();
  }
  if (urlPath == 'ground_truth') {
    jsonData = Application().getGroundTruthImage();
  }

  if (jsonData != null) {
    return Response.ok(jsonData, headers: {'Content-Type': 'application/json'});
  }

  return Response.notFound('Not Found');
}