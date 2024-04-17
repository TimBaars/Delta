import 'package:http/http.dart' as http; 
import 'dart:convert'; 
import '../logic/logic_environment_loader.dart';

typedef Response = http.Response;

const String endpoint = 'http://localhost:5000';
String apikey = "";
 
Future<Response> callEndpoint(endpointAddition) async { 
  if (apikey.isEmpty) {
    apikey = await retrieveKey('APIKEY');
  }

  final response = await http.get( 
    Uri.parse('$endpoint/api/$endpointAddition'), 
    headers: {'X-API-KEY': apikey},
  ); 
  
  if (response.statusCode == 200) { 
    return response; 
  } else { 
    var errorMessage = "";
    
    try {
      Map<String, dynamic> data = jsonDecode(response.body); 

      errorMessage = data['error'];
    } catch (e) { 
      throw Exception('Failed to request data'); 
    } 

    throw Exception(errorMessage);
  } 
} 
 
Future<bool> startDelta() async { 
  try { 
    final response = await callEndpoint('start'); 
    Map<String, dynamic> data = jsonDecode(response.body); 
    print(data['message']);

    return data['message'] != null ? true : false;
  } catch (e) { 
    print('Failed to start Delta: $e');
  } 
  
  return false;
} 

Future<bool> stopDelta() async { 
  try { 
    final response = await callEndpoint('stop'); 
    Map<String, dynamic> data = jsonDecode(response.body); 
    print(data['message']); 

    return data['message'] != null ? true : false;
  } catch (e) { 
    print('Failed to start Delta: $e'); 
  } 

  return false; 
} 

Future<void> getLocationDelta() async { 
  try { 
    final response = await callEndpoint('location'); 
    Map<String, dynamic> data = jsonDecode(response.body); 
    print(data['message']); 
    print(data['location']); 
  } catch (e) { 
    print('Failed to start Delta: $e'); 
  } 

  // ToDo: Callback to the ui instead of print 
} 