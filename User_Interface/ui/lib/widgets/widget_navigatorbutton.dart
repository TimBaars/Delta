import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class NavigatorButtonWidget extends StatelessWidget {
  final String _title;
  final IconData _icon;
  final StatelessWidget _nextScreen;
  final Function _function;
  
  static void defaultFunction() {}

  NavigatorButtonWidget(this._title, this._icon, this._nextScreen, {super.key, function = defaultFunction}) : _function = function;

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      style: ButtonStyle(
        backgroundColor: MaterialStateProperty.all<Color>(Colors.blue),
        padding: MaterialStateProperty.all<EdgeInsetsGeometry>(const EdgeInsets.all(20)),
      ),
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => _nextScreen),
        );
        _function();
      },
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(_icon),
            Text(_title, style: const TextStyle(fontSize: 20, overflow: TextOverflow.ellipsis)),
          ],
        ),
      ),
    );
  }
}