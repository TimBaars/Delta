## Service for the Delta Control

### Bash script for service

```ps
# Open VENV
cd /home/pi
source ./Desktop/Delta/delta/bin/activate

# Go to the Delta Control directory
cd ./Desktop/Delta

# Run the main.py
python main.py
```

### Service definition

Create a new file `/etc/systemd/system/delta_control.service`

```service
[Unit]
Description=Delta control with RRT Pathfinding
After=network.target

[Service]
ExecStart=/var/delta/startup.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

```ps
# Allow everyone to execute
sudo chmod +x /var/delta/startup.sh

# Reload the daemon
sudo systemctl daemon-reload

# Enabling the service
sudo systemctl enable delta_control.service

# Starting the service
sudo systemctl start delta_control.service

# Verify the status
sudo systemctl status delta_control.service

# Reboot the Orange Pi
sudo reboot
```
