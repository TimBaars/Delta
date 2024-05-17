import 'dart:convert';

import 'package:frontend/util/image_cache.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/api/api.dart';

void main() {
  MaskedImageLogic().request();
}

class MaskedImageLogic {
  final String endpointAddition = "masked";
  final List<Map<String, dynamic>> historicalData = [];
  var function = () => {};
  Map<String, dynamic> json = {
    "url": "http://192.168.178.107/images/masked_image.png",
    "time": 0,
  };
  
  final ImageCache imageCache = ImageCache();

  MaskedImageLogic() {
    loadImage();
  }

  void loadImage() {
    print("Loading image: ${json["url"]}");
    http.get(Uri.parse(json["url"])).then((response) {
      if (response.statusCode == 200) {
        imageCache.addImage(response.bodyBytes.buffer.asUint8List());

        function();
      }
    });
  }

  void setJson(Map<String, dynamic> json) {
    this.json = json;

    print("Json: $json");
  }

  void request({DateTime? dateTime}) async {
    await Future.delayed(Duration(seconds: 1));

    try {
      http.Response result = await apiManager.requestData(endpointAddition, dateTime: dateTime);

      if (result.statusCode == 200) {
        String body = result.body;

        if (body != "") {
          var jsonResult = jsonDecode(body.replaceAll("\'", "\""));

          if (jsonResult.toString() != json.toString()) {
            if (historicalData.length > 10) historicalData.removeAt(0);
            historicalData.add(json);

            setJson(jsonResult);

            loadImage();
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
