import 'dart:convert';
import 'dart:typed_data';

import 'package:frontend/api/api.dart';
import 'package:http/http.dart' as http;

void main() {
  MaskedImageLogic maskedImageLogic = MaskedImageLogic();

  maskedImageLogic.request();
}

class MaskedImageLogic {
  final String endpointAddition = "masked";
  final List<Map<String, dynamic>> historicalData = [];
  var function = () => {};
  Map<String, dynamic> json = {
    "received": false,
    "url": "localhost/masked_image.png",
  };
  ByteData image = ByteData(0);

  MaskedImageLogic();

  void loadImage() {
    print("RrtImageLogic loadImage: loading image");

    http.get(Uri.parse(json["url"])).then((response) {
      if (response.statusCode == 200) {
        print("RrtImageLogic loadImage: image loaded");

        image = ByteData.view(response.bodyBytes.buffer);
        function();
      }
    });
  }

  void setJson(Map<String, dynamic> json) {
    this.json = json;

    print("Json: $json");
  }

  void request() async {
    await Future.delayed(Duration(milliseconds: 500));

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

        print("MaskedImageLogic request: position: changed");

        function();
      } else {
        print("MaskedImageLogic request: no change");
      }
    }

    request();
  }
}
