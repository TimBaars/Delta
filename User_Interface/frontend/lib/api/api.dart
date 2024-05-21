import 'dart:convert';

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

  static Future<void> sendData(String endpointAddition, Map<String, dynamic> data) async {
    var host = kDebugMode ? WSHOSTDEBUG : WSHOST;
    var endpoint = "$host/post";

    var body = jsonEncode(data);

    http.Response response = await http.post(
      Uri.parse(endpoint),
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Endpoint': endpointAddition,
        'Timestamp': DateTime.now().toUtc().millisecondsSinceEpoch.toString(),
      },
      body: body,
    );

    print('Response status code: ${response.statusCode}');
  }
}
