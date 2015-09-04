from flask import request
from flask import Flask,jsonify
from flask import make_response
import json
import subprocess
import uuid
import os
import sys
import create
import destroy_vm
import settings
app = Flask(__name__)
settings.init()          # Call only once

@app.route("/server/vm/create/", methods=['GET'])
def create_vm():
   		    name=request.args.get('name')
		    instance_type=request.args.get('instance_type')
		    image_id=request.args.get('image_id')
		    #print name
		    vm_dict={}
		    vm_dict['name']=name
		    vm_dict['instance_type']=instance_type
		    vm_dict['image_id']=image_id
#		    print machine_list
		    return jsonify(create.createvm(vm_dict))

@app.route("/server/vm/query", methods=['GET'])
def query_vm():
	            vmid=request.args.get('vmid')
		    vm_dict={}
		    flag=0
	            for i in settings.created_vms:
		         if int(i[0])==int(vmid):
			     vm_dict['vmid']=i[0]
			     vm_dict['name']=str(i[1])
			     vm_dict['instance_type']=int(i[2])
			     vm_dict['pmid']=int(i[3])+1
			     flag=1
			     break
		    if flag==0:
		      return jsonify({"status":0})
		    return jsonify(vm_dict)
			     
		    #print settings.created_vms
		    '''try:
		        for i in create_vm.vm_list:
			    if i[0]==vmid:
			        vm_dict['vmid']=i[0]
				vm_dict['name']=i[1]
				vm_dict['instance_type']=i[2]
				vm_dict['pmid']=i[3]+1
				break
	                return jsonify(vm_dict)
	            except:
		        return jsonify({})'''


@app.route("/server/vm/destroy", methods=['GET'])
def destory_vm():
	            vmid=request.args.get('vmid')
		    vm_dict={}
		    vm_dict['vmid']=vmid
		    return jsonify(destroy_vm.destroy(vm_dict))


@app.route("/server/vm/types", methods=['GET'])
def types_vm():
	    types_file=open(var3)
	    lines=types_file.readlines()
	    stri=""
	    for i in range(0,len(lines)):
	    	stri=stri+lines[i]
	    settings.decoded=json.loads(stri)
            return jsonify(settings.decoded)
	    #lines=json.loads(lines)
	    #print lines
	    #vm_dict={}
	    #vm_dict['line']=lines
	    #return jsonify({"vm_dict":vm_dict})


@app.route("/server/image/list", methods=['GET'])
def get_images():
	lis=[]
	for i in range(0,len(settings.imageid_list)):
		dicti={}
		dicti["id"]=settings.imageid_list[i][0]
		dicti["name"]=settings.imageid_list[i][1]
		lis.append(dicti)
	return jsonify({"images":lis})

@app.route("/server/pm/list", methods=['GET'])
def list_pms():
	listi=[]
	for i in range(0,len(settings.machine_list)):
		listi.append(settings.machine_list[i][3])
#	print listi
#	return jsonify({})
	pm_dict={}
	pm_dict['pmids']=listi
#	print pm_dict
	return jsonify(pm_dict)

@app.route("/server/pm/listvms", methods=['GET'])
def list_vms():
	pmid=int(request.args.get('pmid'))
	vm={}
	vm_dict=[]
	flag=0
	for i in settings.created_vms:
	    if i[3]==int(pmid)-1:
	       vm_dict.append(int(i[0]))
	       flag=1
	if flag==0:
	   return jsonify({"status":0})
	vm["vmids"]=vm_dict
	return jsonify(vm)

@app.route("/server/pm/query", methods=['GET'])
def pm_query():
	pmid=request.args.get('pmid')
	vm_dict={}
	vm_dict["pmid"]=pmid
	count=0
	vm_capacity={}
	vm_free={}
	for i in settings.created_vms:
	    if i[3]==int(pmid)-1:
	        count=count+1
        vm_dict["vms"]=count
	username=settings.machine_list[int(pmid)-1][0]
	ip=settings.machine_list[int(pmid)-1][1]
	st = int(subprocess.check_output("ssh "+username+"@"+ip+" nproc",shell=True))
	vm_capacity["cpu"]=st
	#print st
	st =subprocess.check_output("ssh "+username+"@"+ip+" free -m",shell=True)
	st=st.split("\n")
	st=st[1]
	st=" ".join(st.split())
	st=st.split(" ")
	st=st[1]
        vm_capacity["ram"]=int(st)
	#print int(st)
	st = subprocess.check_output("ssh "+username+"@"+ip+" df -h --total | grep 'total'",shell=True)
	st=" ".join(st.split())
	st=st.split(" ")[1]
	st=st[:-1]
	vm_capacity["disk"]=int(st)
	#print int(st)
	st =subprocess.check_output("ssh "+username+"@"+ip+" free -m",shell=True)
	st=st.split("\n")
	st=st[1]
	st=" ".join(st.split())
	st=st.split(" ")
	st=st[3]
	vm_free["ram"]=int(st)
	#print int(st)
	st = subprocess.check_output("ssh "+username+"@"+ip+" df -h --total | grep 'total'",shell=True)
	st=" ".join(st.split())
	st=st.split(" ")[3]
	st=st[:-1]
	vm_free["disk"]=int(st)
	#print int(st)
	st = subprocess.check_output("ssh "+username+"@"+ip+" lscpu | grep 'Socket(s)'",shell=True)
	st=" ".join(st.split())
	st=st.split(" ")[1]
	st=int(st)
	st1 = subprocess.check_output("ssh "+username+"@"+ip+" lscpu | grep 'Core(s)'",shell=True)
        st1=" ".join(st1.split())
	st1=st1.split()
	st1=int(st1[-1])
	vm_free["cpu"]=vm_capacity["cpu"]-st*st1
	#print st*st1
	vm_dict["capacity"]=vm_capacity
	vm_dict["free"]=vm_free
	return jsonify(vm_dict)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def get_machines(filename):
    fp=open(filename)
    lines=fp.readlines()
    i=1
#print machine_list
    for line in lines:
	    line=line[:-1]
	    dummy=line.split("@")
	    dummy.append(uuid.uuid4())
	    dummy.append(i)
	    i=i+1
	    settings.machine_list.append(dummy)
#    print machine_list

def get_images(filename):
    fp=open(filename)
    lines=fp.readlines()
    trial=[]
    count=1
    for line in lines:
	    line=line[:-1]
	    dummy=line.split("@")
	    trial.append(dummy[0])
            t=dummy[1].split(":")
	    trial.append(t[0])
	    trial.append(t[1])
	    prac=[]
	    prac.append(count)
	    prac.append(t[1].split("/")[-1])
	    settings.imageid_list.append(prac)
            count=count+1
	    settings.image_list.append(trial)
	    #print settings.image_list
	    #print settings.imageid_list

         
def get_types(var3):
	    types_file=open(var3)
	    lines=types_file.readlines()
	    stri=""
	    for i in range(0,len(lines)):
	    	stri=stri+lines[i]
	    settings.decoded1=json.loads(stri)


if __name__ == "__main__":
    if len(sys.argv)<4:
        print "Format is ./script pm_file image_file type_file"
        exit(1)
    global var1
    var1=sys.argv[1]
    global var2
    var2=sys.argv[2]
    global var3
    var3=sys.argv[3]
    global count
    get_machines(var1)
    get_images(var2)
    get_types(var3)
    #print settings.created_vms
    app.run(debug=True)

