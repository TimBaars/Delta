import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:frontend/logic/logic_actuator_status.dart';
import 'package:frontend/logic/logic_delta_status.dart';
import 'package:frontend/logic/logic_ground_truth_logic.dart';
import 'package:frontend/logic/logic_masked_image.dart';
import 'package:frontend/logic/logic_optimized_path_image.dart';
import 'package:frontend/logic/logic_planned_path_image.dart';
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
  final PlannedPathImageLogic plannedPathImageLogic = PlannedPathImageLogic();
  final OptimizedPathImageLogic optimizedPathImageLogic = OptimizedPathImageLogic();

  final String endpointAddition = "system";
  var running = false;
  var initialized = false;
  var function = () => {};
  Map<String, dynamic> json = {
    "running": "false",
  };

  void updateFunctions() {
    actuatorStatusLogic.function = function;
    deltaStatusLogic.function = function;
    maskedImageLogic.function = function;
    rrtImageLogic.function = function;
    groundTruthImageLogic.function = function;
    plannedPathImageLogic.function = function;
    optimizedPathImageLogic.function = function;
  }

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

  void request({DateTime? dateTime}) async {
    await Future.delayed(Duration(milliseconds: 0));
    
    try {
      http.Response result = await apiManager.requestData(endpointAddition, dateTime: dateTime);

      if (result.statusCode == 200) {
        String body = result.body;

        if (body != "") {
          var jsonResult = jsonDecode(body.replaceAll("\'", "\""));

          if (jsonResult.toString() != json.toString()) {
            setJson(jsonResult);

            function();
          }

          if (jsonResult.toString() != json.toString()) {
            running = jsonResult["running"] == "true";

            setJson(jsonResult);

            function();
          }
        }

        dateTime = DateTime.now();
      }
    } catch (e) {
      await Future.delayed(Duration(milliseconds: 500));
      print("SystemStatusLogic request error: $e");
    }

    request(dateTime: dateTime);
  }

  void toggle({bool? runningOverride}) {
    print("SystemStatusLogic toggle");

    running = runningOverride != null ? runningOverride : !running;

    json["running"] = running ? "true" : "false";

    function();

    apiManager.sendData(endpointAddition, json);
  }

  void stop() {
    toggle(runningOverride: false);
  }

  void start() {
    toggle(runningOverride: true);
  }
}
