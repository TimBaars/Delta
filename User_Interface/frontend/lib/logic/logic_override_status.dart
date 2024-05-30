import 'package:frontend/api/api.dart';

class OverrideStatusLogic {
  static void override(endpointAddition, json) {
    print("OverrideStatusLogic sendMessage [$endpointAddition]: $json");

    apiManager.sendData(endpointAddition, json);
  }
}
