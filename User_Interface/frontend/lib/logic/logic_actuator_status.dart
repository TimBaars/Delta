import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:http/http.dart' as http;

void main() {
  ActuatorStatusLogic actuatorStatusLogic = ActuatorStatusLogic();

  actuatorStatusLogic.toggle();
  actuatorStatusLogic.request();
}

class ActuatorStatusLogic {
  final String endpointAddition = "actuator";
  final List<Map<String, dynamic>> historicalData = [];
  var running = false;
  var function = () => {};
  Map<String, dynamic> json = {
    "position": {"x": 0, "y": 0, "z": 0},
    "drilling": false,
    "extend": false,
    "angle": 0,
  };

  ActuatorStatusLogic();


  void setJson(Map<String, dynamic> json) {
    this.json = json;
    
    var position = json['position'];
    var drilling = json['drilling'];
    var extend = json['extend'];
    var angle = json['angle'];

    print("Json: $json");
  }

  void request() async {
    await Future.delayed(Duration(milliseconds: 500));

    if (running) {
      http.Response result = await apiManager.requestData(endpointAddition);

      if (result.statusCode == 200) {
        String body = result.body;
        
        print(body.toString());
        var jsonResult = jsonDecode(body.replaceAll("\'", "\""));
        print(jsonResult.toString());

        if (jsonResult.toString() != json.toString()) {
          if (historicalData.length > 10) historicalData.removeAt(0);
          historicalData.add(json);

          setJson(jsonResult);

          print("ActuatorStatusLogic request: position: changed");

          function();
        } else {
          print("ActuatorStatusLogic request: no change");
        }
      }

      request();
    }
  }

  void toggle() {
    print("ActuatorStatusLogic toggle");

    if (running) {
      stop();
    } else {
      start();
    }
  }

  void stop() {
    running = false;
    print("ActuatorStatusLogic sendStop");
  }

  void start() {
    running = true;

    request();

    print("ActuatorStatusLogic sendStart");
  }
}
