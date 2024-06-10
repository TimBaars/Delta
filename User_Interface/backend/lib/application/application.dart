import 'package:backend/logic/logic_received_optimized_path_image.dart';
import 'package:backend/logic/logic_received_planned_path_image.dart';
import 'package:backend/rabbitmq/client.dart';

import '../logic/logic_delta_status.dart';
import '../logic/logic_received_ground_truth_image.dart';
import '../logic/logic_received_masked_image.dart';
import '../logic/logic_received_rrt_image.dart';
import '../logic/logic_system_status.dart';

import '../logic/logic_actuator_status.dart';
import '../logic/logic_status.dart';
import '../endpoint/handle_api_request.dart';

import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as shelf_io;
import 'package:shelf_cors_headers/shelf_cors_headers.dart';

class Application {
  static final Application _singleton = Application._internal();

  static const overrideHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': '*',
  };
  
  final StatusLogic actuatorStatusLogic = ActuatorStatusLogic();
  final StatusLogic deltaStatusLogic = DeltaStatusLogic();
  final StatusLogic maskedImageLogic = MaskedImageLogic();
  final StatusLogic rrtImageLogic = RrtImageLogic();
  final StatusLogic plannedPathImageLogic = PlannedPathImageLogic();
  final StatusLogic optimizedPathImageLogic = OptimizedPathImageLogic();
  final StatusLogic systemStatusLogic = SystemStatusLogic();
  final StatusLogic groundTruthImageLogic = GroundTruthImageLogic();

  factory Application() {
    return _singleton;
  }

  Application._internal();

  Future<String> getActuatorStatus(int timestamp) async {
    return actuatorStatusLogic.retrieveLastData(timestamp);
  }

  Future<String> getRobotStatus(int timestamp) async {
    return deltaStatusLogic.retrieveLastData(timestamp);
  }
  
  Future<String> getMaskedImage(int timestamp) async {
    return maskedImageLogic.retrieveLastData(timestamp);
  }

  Future<String> getRrtImage(int timestamp) async {
    return rrtImageLogic.retrieveLastData(timestamp);
  }

  Future<String> getSystemStatus(int timestamp) async {
    return systemStatusLogic.retrieveLastData(timestamp);
  }

  Future<String> getGroundTruthImage(int timestamp) async {
    return groundTruthImageLogic.retrieveLastData(timestamp);
  }

  Future<String> getOptimizedPathStatus(int timestamp) async {
    return optimizedPathImageLogic.retrieveLastData(timestamp);
  }

  Future<String> getPlannedPathImage(int timestamp) async {
    return plannedPathImageLogic.retrieveLastData(timestamp);
  }

  Future<String> putData(Request request) async {
    var headers = request.headers;

    if (headers.containsKey("Endpoint")) {
      var updated = false;

      var endpoint = headers["Endpoint"];
      var timestamp = DateTime.now().toUtc().millisecondsSinceEpoch;

      if (headers.containsKey("Timestamp")) {
        try {
          timestamp = int.parse(headers["Timestamp"]!.toString());
        } catch (e) {
          print('Error parsing timestamp: $e');
        }
      }

      var body = await request.readAsString();
      var data = body;

      if (endpoint == "actuator") {
        updated = actuatorStatusLogic.setData(data, timestamp);
      }
      if (endpoint == "delta") {
        updated = deltaStatusLogic.setData(data, timestamp);
      }
      if (endpoint == "masked") {
        updated = maskedImageLogic.setData(data, timestamp);
      }
      if (endpoint == "rrt") {
        updated = rrtImageLogic.setData(data, timestamp);
      }
      if (endpoint == "system") {
        updated = systemStatusLogic.setData(data, timestamp);
      }
      if (endpoint == "ground_truth") {
        updated = groundTruthImageLogic.setData(data, timestamp);
      }
      if (endpoint == "optimized_path") {
        updated = optimizedPathImageLogic.setData(data, timestamp);
      }
      if (endpoint == "planned_path") {
        updated = plannedPathImageLogic.setData(data, timestamp);
      }

      // if (updated) RabbitMQClient().publish(endpoint!, "", data);

      return "Data received";
    } else {
      return "No endpoint specified";
    }
  }

  Future<void> endpoint() async {
    var handler = Pipeline()
      .addMiddleware(corsHeaders(headers: overrideHeaders))
      .addHandler(HandleApiRequests);

    var server = await shelf_io.serve(handler, 'localhost', 8080);
    print('Server running on localhost:${server.port}');
  }
}