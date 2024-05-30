import 'dart:convert';

import 'package:frontend/api/api.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:http/http.dart' as http;

void main() {
  DeltaStatusLogic().request();
}

class DeltaStatusLogic {
  final String endpointAddition = "delta";
  final List<Map<String, dynamic>> historicalData = [];
  var function = List<Function>.empty(growable: true);
  Map<String, dynamic> json = {
    "position": {"x": 0, "y": 0, "z": 0},
    "status": "stopped",
    "velocity": 0,
    "direction": {"from x": 0, "from y": 0, "to x": 0, "to y": 0},
  };

  DeltaStatusLogic();

  void setJson(Map<String, dynamic> json) {
    this.json = json;
  }

  void request({DateTime? dateTime}) async {
    await Future.delayed(Duration(milliseconds: 500));

    try {
      if (SystemStatusLogic().isRunning()) {
        http.Response result = await apiManager.requestData(endpointAddition, dateTime: dateTime);

        if (result.statusCode == 200) {
          String body = result.body;

          if (body != "") {
            print(body);
            var tempResult = jsonDecode(body.toLowerCase().replaceAll("\'", "\""));
            var jsonResult = jsonDecode(tempResult);
            
            if (jsonResult.toString() != json.toString()) {
              if (historicalData.length > 10) historicalData.removeAt(0);
              print("dumbPrint1");
              historicalData.add(json);
              print("dumbPrint2");

              setJson(jsonResult);
              print("dumbPrint3");

              function.forEach((fn) => fn());
            }
          }

          dateTime = DateTime.now();
        }
      }
    } catch (e) {
      await Future.delayed(Duration(milliseconds: 500));
      print("SystemStatusLogic request error: $e");
    }

    request(dateTime: dateTime);
  }
}
