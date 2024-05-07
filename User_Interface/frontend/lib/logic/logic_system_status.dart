import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:http/http.dart' as http;

void main() {
  SystemStatusLogic systemStatusLogic = SystemStatusLogic();

  systemStatusLogic.toggle();
  systemStatusLogic.request();
}

class SystemStatusLogic {
  final String endpointAddition = "system";
  final List<Map<String, dynamic>> historicalData = [];
  var running = false;
  var function = () => {};
  Map<String, dynamic> json = {
    "running": false,
  };

  SystemStatusLogic();

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

          print("SystemStatusLogic request: position: changed");

          function();
        } else {
          print("SystemStatusLogic request: no change");
        }
      }

      request();
    }
  }

  void toggle() {
    print("SystemStatusLogic toggle");

    if (running) {
      stop();
    } else {
      start();
    }
  }

  void stop() {
    running = false;
    print("SystemStatusLogic sendStop");
  }

  void start() {
    running = true;

    request();

    print("SystemStatusLogic sendStart");
  }
}
