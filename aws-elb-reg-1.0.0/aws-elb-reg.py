#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import sys
import os
import boto.ec2
import boto.ec2.elb

##### Config
# Defined ACTION name
ACTIONS = ('add', 'delete', 'status')

##### Functions
def get_instance_data(data_path):
    """
    Return my instance metadata
    """
    url = 'http://169.254.169.254/latest/meta-data/{path}'.format(path = data_path)
    cmd = ['curl', '-s', url]
    ret = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout = subprocess.PIPE).communicate()[0]
    return ret

##### Execution
# Receive data
if len(sys.argv) == 5:
    action = sys.argv[1]
    if action not in ACTIONS:
        print('Undefined action: {act}'.format(act = action).encode('UTF-8'))
    TAG_ELB     = sys.argv[2]
    ACCESS_KEY  = sys.argv[3]
    SECRET_KEY  = sys.argv[4]
else:
    print('Usage: {self} <action> <tag> <access_key> <secret_key>'.
          format(self = os.path.basename(__file__)))
    sys.exit(1)

# Initializing
output = []

# Get my region based on its own AZ
my_az = get_instance_data('placement/availability-zone')
my_region = my_az[:-1]
# Get my instance-id
my_ins_id = get_instance_data('instance-id')

# Connect to EC2
conn = boto.ec2.connect_to_region(my_region, aws_access_key_id = ACCESS_KEY,
                                  aws_secret_access_key = SECRET_KEY)

# Identify ELB belonging from the tag for an instance of their own
insObj = conn.get_only_instances([my_ins_id])[0]
# If don't have the tag, exit
if TAG_ELB not in insObj.tags:
    print("This instance does not have the tag key '{tagname}'.".format(tagname = TAG_ELB))
    sys.exit(1)
else:
    my_elb_list = [ x.strip() for x in insObj.tags[TAG_ELB].split(',') ]

# Connect to ELB
elbconn = boto.ec2.elb.connect_to_region(my_region, aws_access_key_id = ACCESS_KEY,
                                         aws_secret_access_key = SECRET_KEY)

# Register with the ELB based on tag
if action == 'add':
    # Because an exception occurs ELB that does not exist is specified,
    # run the registration work only for ELB that there exist gets all once.
    elbObjs = elbconn.get_all_load_balancers()
    elbObjs = [ e for e in elbObjs if e.name in my_elb_list ]
    for elbObj in elbObjs:
        # instance-id list
        elb_ins_list = [ ins.id for ins in elbObj.instances if ins.id == my_ins_id ]
        # Register if not registered in the ELB
        if my_ins_id not in elb_ins_list:
            elbObj.register_instances([my_ins_id])
            output.append(elbObj.name)

# Delete the registration from all ELB
elif action == 'delete':
    # Get ELB all information when deleting (There may be leakage of registration tag)
    elbObjs = elbconn.get_all_load_balancers()
    for elbObj in elbObjs:
        for insObj in elbObj.instances:
            # Delete from the ELB if there is my instance-id
            if insObj.id == my_ins_id:
                elbObj.deregister_instances([my_ins_id])
                output.append(elbObj.name)

# Display of registration information
elif action == 'status':
    # Check the registered instance by getting the ELB information of all
    elbObjs = elbconn.get_all_load_balancers()
    for elbObj in elbObjs:
        for insObj in elbObj.instances:
            # Display of the ELB if there is my instance-id
            if insObj.id == my_ins_id:
                output.append(elbObj.name)

if output:
    print(' '.join(output))
else:
    print()
