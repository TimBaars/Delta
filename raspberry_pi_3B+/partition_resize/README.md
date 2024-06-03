## Resizing SD-Card partition size

```ps
# Using parted to resize the partition
sudo parted /dev/mmcblk0
(parted) resizepart 2
(parted) quit

# Using resize2fs to resize the filesystem
sudo resize2fs /dev/mmcblk0p2 32000M
```
*Might require a re-connect to the server*

#### Example
```ps
Using /dev/mmcblk0
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) resizepart 2
Warning: Partition /dev/mmcblk0p2 is being used. Are you sure you want to
continue?
Yes/No? Yes
End?  [1477MB]? 100%
(parted) quit
```