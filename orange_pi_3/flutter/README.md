## Setting up Orange Pi 3 flutter application

### Prerequisites

Orange Pi is setup with a Linux/Armbian OS installed and updated/upgraded.
For information see [README](../README.md).

### Installing Flutter

#### Windows

Follow the [official installation guide](https://docs.flutter.dev/get-started/install/windows/web?tab=download#install-the-flutter-sdk).

#### Linux

Follow the [official installation guide](https://docs.flutter.dev/get-started/install/linux/desktop?tab=download#install-the-flutter-sdk).

### Preparation Orange Pi

#### Installing Apache2

Login as `orangepi` user
Download and install Apache2

```ps
sudo apt-get install apache2
```

If a firewall is active disable port 80 and 443

```ps
sudo ufw allow 80
sudo ufw allow 443
```

#### Installing RabbitMQ

Make sure RabbitMQ is installed and setup, information to be found in [README](../rabbitmq/README.md).

### Frontend application

Read more at [README](./frontend/README.md).

### Backend application

Read more at [README](./backend/README.md).
