import 'package:backend/logic/logic_delta_status.dart';
import 'package:backend/logic/logic_received_masked_image.dart';
import 'package:backend/logic/logic_received_rrt_image.dart';
import 'package:backend/logic/logic_system_status.dart';

import '../logic/logic_actuator_status.dart';
import '../logic/logic_status.dart';
import '../endpoint/handle_api_request.dart';

import 'package:shelf/shelf.dart';
import 'package:shelf/shelf_io.dart' as shelf_io;
import 'package:shelf_cors_headers/shelf_cors_headers.dart';

class Application {
  static final Application _singleton = Application._internal();

  static const overrideHeaders = {
    'Access-Control-Allow-Origin': '*', // Adjust this to your needs
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': '*',
  };
  
  final StatusLogic actuatorStatusLogic = ActuatorStatusLogic();
  final StatusLogic deltaStatusLogic = DeltaStatusLogic();
  final StatusLogic maskedImageLogic = MaskedImageLogic();
  final StatusLogic rrtImageLogic = RrtImageLogic();
  final StatusLogic systemStatusLogic = SystemStatusLogic();

  factory Application() {
    return _singleton;
  }

  Application._internal();

  String getActuatorStatus() {
    return actuatorStatusLogic.retrieveLastData();
  }

  String getRobotStatus() {
    return actuatorStatusLogic.retrieveLastData();
  }
  
  String getMaskedImage() {
    return maskedImageLogic.retrieveLastData();
  }

  String getRrtImage() {
    return rrtImageLogic.retrieveLastData();
  }

  String getSystemStatus() {
    return systemStatusLogic.retrieveLastData();
  }

  Future<void> endpoint() async {
    var handler = Pipeline()
      .addMiddleware(corsHeaders(headers: overrideHeaders))
      .addHandler(HandleApiRequests);

    var server = await shelf_io.serve(handler, 'localhost', 8080);
    print('Server running on localhost:${server.port}');
  }
}