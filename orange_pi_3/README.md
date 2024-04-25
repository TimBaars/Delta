### Preparation
Install os to sd-card
Get orangepi's ip
Connect through `PuTTY`
- Insert ip
- Connect using `SSH`

### Change Passwords
Change `root` and `orangepi` User passwords
1. Login as the `<username>`
2. Execute
```ps
passwd
```
3. Insert current passwd
4. Insert new passwd
5. Insert new passwd [Confirm]

### Update
Continue as `orangepi` user
```ps
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

### In case of Failure do...
#### Sudo commands fail
Following commands, `vim` then `:wq`
```ps
	sudo vim /var/lib/dpkg/lock-frontend
	sudo vim /var/lib/dpkg/lock
```

### Following steps
#### Delta software

#### Actuator software

#### User Experience software
See [README](./flutter_app/README.md)