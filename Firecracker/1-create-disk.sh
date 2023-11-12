#!/bin/bash
VM_DISK_SIZE=512

dd if=/dev/zero of=rootfs.ext4 bs=1M count=$VM_DISK_SIZE
mkfs.ext4 rootfs.ext4
mkdir /tmp/my-rootfs
sudo mount rootfs.ext4 /tmp/my-rootfs
docker run -it --rm -v /tmp/my-rootfs:/my-rootfs alpine
