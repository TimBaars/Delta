import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:http/http.dart' as http;

void main() {
  DeltaStatusLogic deltaStatusLogic = DeltaStatusLogic();

  deltaStatusLogic.toggle();
  deltaStatusLogic.request();
}

class DeltaStatusLogic {
  final String endpointAddition = "delta";
  final List<Map<String, dynamic>> historicalData = [];
  var running = false;
  var function = () => {};
  Map<String, dynamic> json = {
    "position": {"x": 0, "y": 0, "z": 0},
    "moving": false,
  };

  DeltaStatusLogic();

  void setJson(Map<String, dynamic> json) {
    this.json = json;
    
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

          print("DeltaStatusLogic request: position: changed");

          function();
        } else {
          print("DeltaStatusLogic request: no change");
        }
      }

      request();
    }
  }

  void toggle() {
    print("DeltaStatusLogic toggle");

    if (running) {
      stop();
    } else {
      start();
    }
  }

  void stop() {
    running = false;
    print("DeltaStatusLogic sendStop");
  }

  void start() {
    running = true;

    request();

    print("DeltaStatusLogic sendStart");
  }
}
