## RabbitMQ

### Installation

Full installation instructions can be found [here](https://www.rabbitmq.com/docs/install-debian#manual-installation).

```ps
# Add the Cloudsmith repository
echo "deb https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/deb/debian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/rabbitmq.list

# Add the Cloudsmith repository key
wget -O- https://dl.cloudsmith.io/public/rabbitmq/rabbitmq-erlang/gpg.key | sudo apt-key add -

# Update the package lists
sudo apt-get update

# Install Erlang
sudo apt-get install -y erlang

# Install RabbitMQ
sudo apt-get install -y rabbitmq-server

# Enable and start the RabbitMQ service
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```

### Add account

```ps
# Create user
sudo rabbitmqctl add_user "rabbitmq" "<password>"
sudo rabbitmqctl set_permissions -p / "rabbitmq" ".*" ".*" ".*"
```
