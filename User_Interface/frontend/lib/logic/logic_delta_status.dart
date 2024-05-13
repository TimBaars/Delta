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
  var function = () => {};
  Map<String, dynamic> json = {
    "position": {"x": 0, "y": 0, "z": 0},
    "moving": false,
  };

  DeltaStatusLogic();

  void setJson(Map<String, dynamic> json) {
    this.json = json;
  }

  void request() async {
    await Future.delayed(Duration(milliseconds: 500));

    if (SystemStatusLogic().isRunning()) {
      http.Response result = await apiManager.requestData(endpointAddition);

      if (result.statusCode == 200) {
        String body = result.body;

        if (body != "") {
          var jsonResult = jsonDecode(body.replaceAll("\'", "\""));

          if (jsonResult.toString() != json.toString()) {
            if (historicalData.length > 10) historicalData.removeAt(0);
            historicalData.add(json);

            setJson(jsonResult);

            function();
          }
        }
      }
    }

    request();
  }
}
