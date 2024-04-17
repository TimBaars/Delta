import 'package:flutter/services.dart';

Future<String> retrieveKey(String key) async {
  final Map<String, String> env = await parseStringToMap();
  print("Retrieved key $key: ${env[key]}");
  return env[key] ?? '';
}

Future<Map<String, String>> parseStringToMap({String assetsFileName = '.env'}) async {
  final lines = await rootBundle.loadString(assetsFileName);
  Map<String, String> environment = {};
  for (String line in lines.split('\n')) {
    line = line.trim();
    if (line.contains('=') && !line.startsWith(RegExp(r'=|#'))) {
      List<String> contents = line.split('=');
      environment[contents[0]] = contents.sublist(1).join('=');
    }
  }
  return environment;
}
