import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:frontend/logic/logic_actuator_status.dart';
import 'package:frontend/logic/logic_delta_status.dart';
import 'package:frontend/logic/logic_ground_truth_logic.dart';
import 'package:frontend/logic/logic_masked_image.dart';
import 'package:frontend/logic/logic_rrt_image.dart';
import 'package:http/http.dart' as http;

void main() {
  SystemStatusLogic systemStatusLogic = SystemStatusLogic();

  systemStatusLogic.toggle();
  systemStatusLogic.request();
}

class SystemStatusLogic {
  static final SystemStatusLogic _singleton = SystemStatusLogic._internal();
  
  final ActuatorStatusLogic actuatorStatusLogic = ActuatorStatusLogic();
  final DeltaStatusLogic deltaStatusLogic = DeltaStatusLogic();
  final MaskedImageLogic maskedImageLogic = MaskedImageLogic();
  final RrtImageLogic rrtImageLogic = RrtImageLogic();
  final GroundTruthImageLogic groundTruthImageLogic = GroundTruthImageLogic();

  final String endpointAddition = "system";
  var running = false;
  var initialized = false;
  var function = () => {};
  Map<String, dynamic> json = {
    "running": "false",
  };

  factory SystemStatusLogic() {
    return _singleton;
  }

  void init() {
    if (!initialized) {
      initialized = true;

      request();

      actuatorStatusLogic.request();
      deltaStatusLogic.request();
      maskedImageLogic.request();
      rrtImageLogic.request();
      groundTruthImageLogic.request();
    }
  }

  bool isRunning() {
    return running;
  }

  SystemStatusLogic._internal();

  void setJson(Map<String, dynamic> json) {
    this.json = json;
  }

  void request() async {
    await Future.delayed(Duration(milliseconds: 500));

    http.Response result = await apiManager.requestData(endpointAddition);

    if (result.statusCode == 200) {
      String body = result.body;

      if (body != "") {
        var jsonResult = jsonDecode(body.replaceAll("\'", "\""));

        if (jsonResult.toString() != json.toString()) {
          running = jsonResult["running"] == "true";

          setJson(jsonResult);

          function();
        }
      }
    }

    request();
  }

  void toggle() {
    print("SystemStatusLogic toggle");

    json["running"] = running ? "false" : "true";

    if (running) {
      stop();
    } else {
      start();
    }

    apiManager.sendData(endpointAddition, jsonEncode(json));
  }

  void stop() {
    running = false;

    print("SystemStatusLogic sendStop");
  }

  void start() {
    running = true;

    print("SystemStatusLogic sendStart");
  }
}
