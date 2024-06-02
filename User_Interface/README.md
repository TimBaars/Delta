## User Interface

### Functionalities & status
*Basic UI Layout*
- [x] Basic UI Layout
*Basic UI Functionalities*
- [x] Widget for starting/stopping the delta robot button
- [x] Widget for the ground-truth-image
- [x] Widget for the masked results image
- [x] Widget for the RRT path image
- [x] Auto-updating image data from specific file-path
- [x] Widget for Delta Robot location
- [x] Widget for Delta Robot test-based data
- [x] Widget for Delta Robot data visualization
- [x] Widget for Actuator status
*HTTP connection to server - Test cases*
- [x] Connection to the server using http
- [x] Authorization over http using APIKEY
*HTTP connection to server - Production Environment*
- [x] Connection to the server using http
- [x] Translating information from the server to the UI

### Usage
1. Go to User_Interface/windows
```cmd
cd ./User_Interface/windows
```
2. For the first run use the following commands (or when an error occurs)
```cmd
flutter clean
flutter pub get
```
3. Run the following command
```cmd
flutter run
```

### Testing over http (localhost) communacation
*Beware that this only has limited functionality built in on the Python side, with merely a focus on being able to test the http communacation*
1. Open 2 Command Promps
2. In the both Command Promps, navigate to the User_Interface/windows directory
3. In the first Command Promp, run the following command
```cmd
flutter run
```
4. In the second command promp, install the Python dependencies by running the following command (Only required before first run)
```cmd
pip install -r lib/api/requirements.txt
```
5. In the second Command Promp, run the following command
```cmd
py lib/api/api_endpoint.py
```
6. The UI should now be running and the Python script should be running