import libvirt
import main_mini
import sys
import os
import settings
import subprocess
from uuid import uuid4

settings.init()          # Call only once
def create_xml(hypervisor,vm_name,ram,uuid,cpu,arch_type,driver,source_path):
    xml = "<domain type='" + hypervisor + 			\
	    "'><name>" + vm_name + "</name>				\
		<uuid>" + uuid + "</uuid> \
	      <memory>" + ram + "</memory>					\
	      <vcpu>" + cpu + "</vcpu>						\
	      <os>							\
	        <type arch='" + arch_type + "' machine='pc'>hvm</type>		\
		<boot dev='hd'/>					\
	      </os>							\
	      <features>						\
	        <acpi/>							\
          	<apic/>							\
	      	<pae/>							\
	      </features>						\
              <clock offset='utc'/>                                     \
	      <on_poweroff>destroy</on_poweroff>			\
  	      <on_reboot>restart</on_reboot>				\
	      <on_crash>restart</on_crash>				\
	      <devices>							\
	        <disk type='file' device='disk'>			\
		<driver name=" + driver + " type='raw'/>			\
		<source file='" + source_path + "'/>		\
		<target dev='hda' bus='ide'/>				\
		<address type='drive' controller='0' bus='0' unit='0'/>	\
		</disk>							\
	      </devices>						\
   	      </domain>"

    return xml

def createvm(vm_dict):
	vmname=vm_dict["name"]
	instance_type=int(vm_dict["instance_type"])
	#print vmname, instance_type
	#print settings.machine_list
	#print settings.image_list
	vcpu= settings.decoded1['types'][instance_type-1]['cpu']
	#print vcpu
	vram = settings.decoded1['types'][instance_type-1]['ram']
	vram = vram*1024
	#print vram
	total_no_of_pm=1
	username=settings.machine_list[settings.pmid][0]
	ip=settings.machine_list[settings.pmid][1]
	#print username,ip
	available_cpu=int(subprocess.check_output("ssh " + username + "@" + ip + " nproc" ,shell=True))
	#print available_cpu
	available_ram = (subprocess.check_output("ssh " + username + "@" + ip + " free -m",shell=True))
	available_ram = available_ram.split("\n")
	available_ram = available_ram[1].split()
	available_ram = int(available_ram[3])
	available_ram = available_ram*1024
	#print available_ram
	while(available_cpu < vcpu or available_ram < vram):
		settings.pmid=(settings.pmid+1)%(len(settings.machine_list))
		total_no_of_pm=total_no_of_pm+1
		if(total_no_of_pm > len(settings.machine_list)):
			return {"Error" : "Virtual Machine could not be created.Some of the specifications could not be met"}
		username = settings.machine_list[settings.pmid][0]
		ip = settings.machine_list[settings.pmid][1]
		available_cpu=int(subprocess.check_output("ssh " + username + "@" + ip + " nproc" ,shell=True))
	        available_ram = (subprocess.check_output("ssh " + username + "@" + ip + " free -m",shell=True))
	        available_ram = available_ram.split("\n")
	        available_ram = available_ram[1].split()
	        available_ram = int(available_ram[3])
	        available_ram = available_ram*1024
	
	settings.vmid=settings.vmid + 1
	settings.created_vms.append([settings.vmid,str(vmname),instance_type,settings.pmid])
	settings.pmid=(settings.pmid+1)%(len(settings.machine_list))
	uid = str(uuid4())
	#print settings.created_vms
	connect = libvirt.open('remote+ssh://' + username + '@' + ip + '/')
	pm_info = connect.getCapabilities()
	emulator = pm_info.split("<domain type=")
	emulator = emulator[1].split(">")[0]
	#print emulator
	arch_type = pm_info.split("<arch>")
	arch_type = arch_type[1].split("</arch>")[0]
	#print arch_type
	image_id=vm_dict['image_id']
	username1=settings.image_list[int(image_id)-1][0]
	ip1=settings.image_list[int(image_id)-1][1]
	path1=settings.image_list[int(image_id)-1][2]
	#print path1
	os.system("scp "+username1+"@"+ip1+":"+path1+" ~/image.img")
	my_path="/home/"+username+"/image.img"
	os.system("scp ~/image.img "+username+"@"+ip+":"+my_path)
        


	#source_path="/home/kanika/cloud_computing/MiniProject/linux.img"
	request = connect.defineXML(create_xml(connect.getType().lower(),vmname,str(vram),uid,str(vcpu),arch_type,emulator,my_path))
	#print request
	try:
		request.create()
		return {"vmid": settings.vmid}
	except:
		return {"vmid" : 0 }

	

	





