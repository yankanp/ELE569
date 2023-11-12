VM_MEMORY=256
VM_CPU_CORES=1
sudo umount /tmp/my-rootfs


sudo ip tuntap add tap0 mode tap
sudo ip addr add 172.20.0.1/24 dev tap0
sudo ip link set tap0 up
DEVICE_NAME=ens4
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"
sudo iptables -t nat -A POSTROUTING -o $DEVICE_NAME -j MASQUERADE
sudo iptables -A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i tap0 -o $DEVICE_NAME -j ACCEPT
MAC="$(cat /sys/class/net/tap0/address)"


curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/boot-source' -H 'Accept: application/json' -H 'Content-Type: application/json' \
  -d '{"kernel_image_path":"./hello-vmlinux.bin","boot_args":"console=ttyS0 reboot=k panic=1 pci=off"}'

curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/drives/rootfs' -H 'Accept: application/json' -H 'Content-Type: application/json' \
  -d '{"drive_id":"rootfs","path_on_host":"./rootfs.ext4","is_root_device":true,"is_read_only":false}'

vcpu_count=$(printf "%d\n" "$VM_CPU_CORES")
mem_size_mib=$(printf "%d\n" "$VM_MEMORY")

curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/machine-config' -H 'Accept: application/json' -H 'Content-Type: application/json' \
  -d '{"vcpu_count":'$vcpu_count',"mem_size_mib":'$mem_size_mib',"ht_enabled":false}'

curl --unix-socket /tmp/firecracker.sock -i \
   -X PUT 'http://localhost/network-interfaces/ens4' -H 'Accept: application/json' -H 'Content-Type: application/json' \
   -d '{"iface_id": "ens4","guest_mac": "62:35:ea:ab:98:44","host_dev_name": "tap0","state": "Attached"
    }' 

curl --unix-socket /tmp/firecracker.sock -i \
  -X PUT 'http://localhost/actions' -H  'Accept: application/json' -H  'Content-Type: application/json' \
  -d '{"action_type":"InstanceStart"}'
