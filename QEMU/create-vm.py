from flask import Flask, render_template, request, redirect
import subprocess
import threading

app = Flask(__name__)

def execute_bash_script():
    try:
        subprocess.Popen(["bash", "user_vm_script.sh"])
    except Exception as e:
        print(f"Error running script: {e}")

@app.route('/', methods=['GET', 'POST'])
def create_vm():
    if request.method == 'GET' and 'show_vms' in request.args:
        vm_list = get_vm_list()
        return render_template('create_vm.html', vm_list=vm_list)

    if request.method == 'POST':
        VM_NAME = request.form['VM_NAME']
        VM_MEMORY = request.form['VM_MEMORY']
        VM_DISK_SIZE = request.form['VM_DISK_SIZE']
        VM_CPU_CORES = request.form['VM_CPU_CORES']

        # Construct the bash script with user input
        bash_script = f"""#!/bin/bash

VM_NAME="{VM_NAME}"
VM_MEMORY="{VM_MEMORY}"
VM_DISK_SIZE="{VM_DISK_SIZE}"
VM_CPU_CORES="{VM_CPU_CORES}"

# Create a disk image for the VM
qemu-img create -f qcow2 "$VM_NAME.qcow2" "$VM_DISK_SIZE"

# Create the VM
virt-install \\
  --name "$VM_NAME" \\
  --memory "$VM_MEMORY" \\
  --vcpus "$VM_CPU_CORES" \\
  --os-variant alpinelinux3.8 \\
  --cdrom alpine-virt-3.18.4-x86_64.iso \\
  --network network=default,model=virtio  # Use NAT \\
  --graphics none \\
  --disk "$VM_NAME.qcow2",device=disk,bus=virtio \\
  --boot hd,cdrom
"""

        # Save the bash script to a file
        with open("user_vm_script.sh", "w") as script_file:
            script_file.write(bash_script)

        t = threading.Thread(target=execute_bash_script)
        t.start()

    return render_template('create_vm.html')

def get_vm_list():
    result = subprocess.run(["virsh", "list", "--all"], text=True, capture_output=True, check=True)
    lines = result.stdout.splitlines()
    vm_list = []

    for line in lines[2:]:  # Skip the first two header lines
        parts = line.split()
        if len(parts) == 3:
            vm_id, vm_name, vm_status = parts
            vm_list.append({"name": vm_name, "status": vm_status})

    return vm_list

@app.route('/delete_vm/<vm_name>', methods=['POST'])
def delete_vm(vm_name):
    try:
        # Execute virsh undefine <vm_name>
        print(vm_name)
        subprocess.Popen(["virsh", "destroy", vm_name])
        subprocess.Popen(["virsh", "undefine", vm_name])

    except Exception as e:
        print(f"Error deleting VM {vm_name}: {e}")

    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

