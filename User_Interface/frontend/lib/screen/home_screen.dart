import 'package:flutter/material.dart';
import 'package:frontend/logic/logic_system_status.dart';
import 'package:frontend/widgets/widget_data_points.dart';

class HomeScreen extends StatelessWidget {
  final SystemStatusLogic logic = SystemStatusLogic();

  HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: <Widget>[
            // Basic Information
            Container(
              padding: EdgeInsets.all(8.0),
              color: Colors.green[50],
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Center(
                    child: Text(
                      'Welcome to the Home Screen',
                      style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.green[700]),
                    ),
                  ),
                  SizedBox(height: 8),
                  Center(
                    child: Text(
                      'This project was realised for the Fontys A-systems minor ',
                      style: TextStyle(fontSize: 16),
                    ),
                  ),
                ],
              ),
            ),          
            SizedBox(height: 16),
            // Start/Stop Buttons
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: <Widget>[
                ElevatedButton(
                  onPressed: () {
                    // Start button functionality
                    //logic.startSystem();
                  },
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.green[700], // Background color
                  ),
                  child: Text('Start'),
                ),
                ElevatedButton(
                  onPressed: () {
                    // Stop button functionality
                    //logic.stopSystem();
                  },
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.brown[700], // Background color
                  ),
                  child: Text('Stop'),
                ),
              ],
            ),
            SizedBox(height: 20),
            Container(
              height: 200,
              color: Colors.grey[300],
              child: Center(
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    Image(image: AssetImage('assets/images/compas_agro.png'), fit: BoxFit.contain),
                    Image(image: AssetImage('assets/images/green_tech_lab.png'), fit: BoxFit.contain),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
