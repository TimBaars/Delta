import 'dart:io';

class ActuatorStatusLogic {
  final dir = Directory('assets/static/images');
  final String destinationPath = 'assets/static/images/placeholder_delta_tool_status.png';
  int status = 0;
  bool running = false;
  late int _statusCount;
  late bool _enabled;

  ActuatorStatusLogic({enabled = false}) {
    _enabled = enabled;

    init();
  }

  void init() async {
    // Amount of statuses, based on amount of images under assets/images/static
    _statusCount = await dir.list().length;
    print(_statusCount);
    
    // Api request to see if it's currently running
    start(); // or stop();

    changeStatus(initial: true);

    // Testing purposes
    if (true) test();
  }

  void test() async {
    bool disposed = _enabled;

    await Future.delayed(Duration(milliseconds: 2500));
    stop();
    
    await Future.delayed(Duration(milliseconds: 2500));
    start();
    
    // await Future.delayed(Duration(milliseconds: 2500));
    // disable();

    if (!disposed) test();
  }

  void start() {
    running = true;
  }

  void stop() {
    running = false;
  }

  void changeStatus({bool initial = false, bool toDisable = false}) async {
    print(status);

    int waitTime = 100;
    bool update = running;

    if (!(_enabled || toDisable)) return;

    if (running) {
      status = (status) % (_statusCount - 2);
      status++;
    } else {
      if (status > 0) {
        status = 0;
        update = true;
      }
    }
    
    if (update) {
      try {
        await File('assets/static/images/placeholder_delta_tool_status_$status.png').copy(destinationPath);
      } catch (e) {
        print("[ActuatorStatusLogic] Error copying image: $e");
      }
      
      if (initial) _statusCount = await dir.list().length;
    }

    await Future.delayed(Duration(milliseconds: waitTime));

    if (_enabled) changeStatus();
  }

  void updateStatus(int newStatus) {
    status = newStatus;
  }

  void enable() {
    _enabled = true;
    running = true;

    changeStatus();
  }

  void disable() {
    _enabled = false;
    running = false;

    changeStatus(toDisable: true);
  }
}