import '../application/application.dart';
import 'package:shelf/shelf.dart';

Future<Response> HandleApiRequests(Request request) async {
  String? jsonData = null;
  int timestamp = 1;

  // print("request: ${request.url.path}, ${request.headers.entries}, ${request.headers}, ${request.url.queryParameters}, ${request.url.queryParametersAll}");
  
  try {
    timestamp = int.parse(request.headers['timestamp']!);
  } catch (e) {
    print('Error parsing timestamp: $e');
  }

  // print("timestamp: $timestamp");

  var urlPath = request.url.path.split('/').last;

  if (urlPath == 'actuator') {
    jsonData = await Application().getActuatorStatus(timestamp);
  }
  if (urlPath == 'delta') {
    jsonData = await Application().getRobotStatus(timestamp);
  }
  if (urlPath == 'masked') {
    jsonData = await Application().getMaskedImage(timestamp);
  }
  if (urlPath == 'rrt') {
    jsonData = await Application().getRrtImage(timestamp);
  }
  if (urlPath == 'system') {
    jsonData = await Application().getSystemStatus(timestamp);
  }
  if (urlPath == 'ground_truth') {
    jsonData = await Application().getGroundTruthImage(timestamp);
  }
  if (urlPath == 'planned_path') {
    jsonData = await Application().getPlannedPathImage(timestamp);
  }
  if (urlPath == 'optimized_path') {
    jsonData = await Application().getOptimizedPathStatus(timestamp);
  }
  if (urlPath == 'post') {
    jsonData = await Application().putData(request);
  }

  if (jsonData != null && jsonData != "") {
    return Response.ok(jsonData, headers: {'Content-Type': 'application/json'});
  } else if (jsonData == "") {
    return Response.notModified(context: {'message': 'No new data available'});
  }

  return Response.notFound('Not Found');
}