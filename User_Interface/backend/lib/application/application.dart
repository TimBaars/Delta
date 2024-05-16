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
    return systemStatusLogic.retrieveLastData(timestamp);
  }

  Future<void> endpoint() async {
    var handler = Pipeline()
      .addMiddleware(corsHeaders(headers: overrideHeaders))
      .addHandler(HandleApiRequests);

    var server = await shelf_io.serve(handler, 'localhost', 8080);
    print('Server running on localhost:${server.port}');
  }
}