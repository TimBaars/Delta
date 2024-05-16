## Compiling and placing files on Orange Pi

### Copying files to Orange Pi

Copy over [Folder](../../User_Interface/backend) to `/var/backend` on the Orange Pi.

On your local machine run the following command to copy the files to the Orange Pi.

```ps
sftp root@<ipaddress>
# First time you will be asked to accept the fingerprint
# Insert root's password
put -r ./ /var/backend
```

### Setting up the server

```ps
# Login on the OrangePi
# Go to /var/backend
cd /var/backend

# Install dependencies
sudo ~/dart-sdk/bin/dart pub get
```

Create a new file `/etc/systemd/system/ui_backend.service`

```service
[Unit]
Description=Backend for the UI
After=network.target

[Service]
ExecStart=/var/backend/startup.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```ps
# Allow everyone to execute
sudo chmod +x /var/backend/startup.sh

# Reload the daemon
sudo systemctl daemon-reload

# Enabling the service
sudo systemctl enable ui_backend.service

# Starting the service
sudo systemctl start ui_backend.service

# Verify the status
sudo systemctl status ui_backend.service

# Reboot the Orange Pi
sudo reboot
```

Allow the port 8080 on the Orange Pi
 
```ps
sudo ufw allow 8080
```