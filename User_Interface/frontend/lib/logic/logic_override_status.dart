import 'package:frontend/api/api.dart';

class OverrideStatusLogic {
  static final OverrideStatusLogic _singleton = OverrideStatusLogic._internal();

  factory OverrideStatusLogic() {
    return _singleton;
  }
  
  OverrideStatusLogic._internal();

  void override(endpointAddition, json) {
    print("OverrideStatusLogic sendMessage [$endpointAddition]: $json");

    apiManager.sendData(endpointAddition, json);
  }
}
