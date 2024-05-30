import 'package:flutter/material.dart';
import 'package:frontend/screen/screen_controllers.dart';
import 'package:frontend/screen/screen_data.dart';
import 'package:frontend/screen/screen_override.dart';
import 'package:frontend/screen/screen_pathfinding.dart';
import 'package:frontend/screen/home_screen.dart';

class MainScreen extends StatefulWidget {
  @override
  _MainScreenState createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    HomeScreen(),
    ControllerScreen(),
    DataScreen(),
    PathFindingScreen(),
    OverrideScreen(),
  ];

  final List<String> _titles = [
    'Home',
    'Controllers',
    'Data',
    'Pathfinding',
    'Override',
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Center(child: Text(_titles[_selectedIndex], style:TextStyle(fontWeight: FontWeight.bold))),
        backgroundColor: Colors.green[700],
      ),
      body: Row(
        children: [
          NavigationRail(
            selectedIndex: _selectedIndex,
            onDestinationSelected: _onItemTapped,
            labelType: NavigationRailLabelType.all,
            backgroundColor: Colors.brown[100],
            selectedIconTheme: IconThemeData(color: Colors.green[700]),
            unselectedIconTheme: IconThemeData(color: Colors.brown[700]),
            selectedLabelTextStyle: TextStyle(color: Colors.green[700]),
            unselectedLabelTextStyle: TextStyle(color: Colors.brown[700]),
            destinations: [
              NavigationRailDestination(
                icon: Icon(Icons.home),
                selectedIcon: Icon(Icons.home_outlined),
                label: Text('Home'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.control_camera),
                selectedIcon: Icon(Icons.control_camera_outlined),
                label: Text('Controllers'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.data_usage),
                selectedIcon: Icon(Icons.data_usage_outlined),
                label: Text('Data'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.pattern),
                selectedIcon: Icon(Icons.pattern_outlined),
                label: Text('Pathfinding'),
              ),
              NavigationRailDestination(
                icon: Icon(Icons.admin_panel_settings),
                selectedIcon: Icon(Icons.admin_panel_settings_outlined),
                label: Text('Override'),
              ),
            ],
          ),
          Expanded(
            flex: 8,
            child: _screens[_selectedIndex],
          ),
        ],
      ),
    );
  }
}
