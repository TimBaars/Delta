import 'package:http/http.dart' as http;

import 'package:frontend/util/constants.dart';

class apiManager {
  static Future<http.Response> requestData(endpointAddition) async {
    var endpoint = "$WSHOST/$endpointAddition";

    http.Response response = await http.get(Uri.parse(endpoint));

    return response;
  }

  static Future<void> sendData(String endpointAddition, String data) async {
    var endpoint = "$WSHOST/$endpointAddition";

    var body = data;

    http.Response response = await http.post(
      Uri.parse(endpoint),
      body: body,
    );

    print('Response status code: ${response.statusCode}');
  }
}
