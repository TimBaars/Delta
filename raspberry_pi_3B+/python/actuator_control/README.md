## Service for the Delta Control

### Bash script for service

```ps
# Open VENV
cd ~
source ~/Desktop/Delta/delta/bin/activate

# Go to the Actuator Control directory
cd ~/Desktop/Delta/Actuator

# Run the main.py
python main.py
```

### Service definition

Create a new file `/etc/systemd/system/actuator_control.service`

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
sudo systemctl enable actuator_control.service

# Starting the service
sudo systemctl start actuator_control.service

# Verify the status
sudo systemctl status actuator_control.service

# Reboot the Orange Pi
sudo reboot
```