  import 'package:flutter/material.dart';
  import 'package:flutter_webrtc/flutter_webrtc.dart';

  class GroundThruthStreamWidget extends StatefulWidget {
  @override
  _GroundThruthStreamWidgetState createState() => _GroundThruthStreamWidgetState();
  }

  class _GroundThruthStreamWidgetState extends State<GroundThruthStreamWidget> {
  RTCPeerConnection? _peerConnection;
  RTCVideoRenderer _remoteRenderer = RTCVideoRenderer();

  @override
  void initState() {
      super.initState();
      _remoteRenderer.initialize(); // Initialize the renderer
      _initWebRTC();
  }

  Future<void> _initWebRTC() async {
      // Initialize WebRTC and connect to the server
      // This is a simplified example; you'll need to set up the WebRTC connection according to your server's configuration
      final Map<String, dynamic> configuration = {
        "iceServers": [
          {"url": "rtsp://192.168.178.60:554/user=view&password=123456&channel=1&stream=1"},
        ],
      };
      _peerConnection = await createPeerConnection(configuration);
      // Add your stream to the peer connection and handle the offer/answer process
      // This part is highly dependent on your specific setup and the media server you're using
  }

  @override
  Widget build(BuildContext context) {
      return Scaffold(
        appBar: AppBar(
          title: Text('RTSP Stream'),
        ),
        body: Center(
          child: RTCVideoView(_remoteRenderer), // Use RTCVideoView to display the video
        ),
      );
  }

  @override
  void dispose() {
      _remoteRenderer.dispose(); // Dispose of the renderer
      _peerConnection?.close();
      super.dispose();
  }
  }

  void main() {
  runApp(MaterialApp(
      home: GroundThruthStreamWidget(),
  ));
  }