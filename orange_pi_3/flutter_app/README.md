## Setting up Orange Pi 3 flutter application

### Prerequisites

Orange Pi is setup with a Linux/Armbian OS installed and updated/upgraded.
For information see [README](../README.md).

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

### Preparation flutter

```ps
cd ./User_Interface/windows
flutter build web
```

### Copying files to Orange Pi

Copy over [Folder](../../User_Interface/windows/build/web) to `/var/www/html` on the Orange Pi.

On your local machine run the following command to copy the files to the Orange Pi.

```ps
sftp root@<ipaddress>
# First time you will be asked to accept the fingerprint
# Insert root's password
put -r ./build/web /var/www/html
```
