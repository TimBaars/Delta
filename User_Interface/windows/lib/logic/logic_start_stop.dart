import '../api/api_connection.dart';

class LogicStartStop {
  static Future<bool> toggle(bool active) {
    if (active) {
      return stop();
    } else {
      return start();
    }
  }

  static Future<bool> start() {
    return startDelta();
  }

  static Future<bool> stop() {
    return stopDelta();
  }

  static String getButtonText(bool active) {
    return active ? "Stop" : "Start";
  }
}