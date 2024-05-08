// import '../api/api_connection.dart';

import 'dart:async';

class LogicStartStop {
  static Future<bool> toggle(bool active) {
    if (active) {
      return stop();
    } else {
      return start();
    }
  }

  static Future<bool> start() {
    return Future(false as FutureOr<bool> Function()); // startDelta();
  }

  static Future<bool> stop() {
    return Future(false as FutureOr<bool> Function()); // stopDelta();
  }

  static String getButtonText(bool active) {
    return active ? "Stop" : "Start";
  }
}