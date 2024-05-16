import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import 'package:frontend/util/constants.dart';

class apiManager {
  static Future<http.Response> requestData(endpointAddition, {DateTime? dateTime}) async {
    var host = kDebugMode ? WSHOSTDEBUG : WSHOST;
    var endpoint = "$host/$endpointAddition";

    int timestamp = dateTime != null ? dateTime.millisecondsSinceEpoch : 0;

    http.Response response = await http.get(Uri.parse(endpoint), headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Timestamp': timestamp.toString(),
    });

    return response;
  }

  static Future<void> sendData(String endpointAddition, String data) async {
    var host = kDebugMode ? WSHOSTDEBUG : WSHOST;
    var endpoint = "$host/$endpointAddition";

    var body = data;

    http.Response response = await http.post(
      Uri.parse(endpoint),
      body: body,
    );

    print('Response status code: ${response.statusCode}');
  }
}