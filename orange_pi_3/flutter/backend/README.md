## Compiling and placing files on Orange Pi

### Copying files to Orange Pi

Copy over [Folder](../../User_Interface/frontend/build/web) to `/var/www/html` on the Orange Pi.

On your local machine run the following command to copy the files to the Orange Pi.

```ps
sftp root@<ipaddress>
# First time you will be asked to accept the fingerprint
# Insert root's password
put -r ./build/web /var/www/html
```
