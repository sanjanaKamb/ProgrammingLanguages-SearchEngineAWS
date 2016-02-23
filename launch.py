import boto
import boto.ec2
import boto.ec2.securitygroup
import os
import time

region = ''
aws_access_key_id=''
aws_secret_access_key = ''
key_name = 'key'
path = ''

group_name = 'group'
group_description = 'description'
remote_path= ''
file_name='csc326.zip'

install_commands=['sudo apt-get install zip unzip', 'wget https://bootstrap.pypa.io/get-pip.py', 'sudo python get-pip.py', 'sudo pip install BeautifulSoup', 'sudo pip install boto', 'sudo pip install google-api-python-client', 'sudo pip install beaker', 'sudo pip install bottle']


def start_instance():

    #Establish connection to aws
    ec2 = boto.connect_ec2(aws_access_key_id,aws_secret_access_key)
    ec2 = boto.ec2.connect_to_region(region)

    try:
            key = ec2.get_all_key_pairs(keynames=[key_name])[0]
    except ec2.ResponseError, e:
            if e.code == 'InvalidKeyPair.NotFound':
                print e.code
            else:
                raise

    # Check to see if specified security group already exists.
    # If we get an InvalidGroup.NotFound error back from EC2,
    # it means that it doesn't exist and we need to create it.
    try:
            group = ec2.get_all_security_groups(groupnames=[group_name])[0]
    except ec2.ResponseError, e:
            if e.code == 'InvalidGroup.NotFound':
                print e.code
                group = ec2.create_security_group(group_name, group_description)
            else:
                raise

    # Add a rule to the security group to authorize SSH traffic
    # on the specified port.
    try:
            group.authorize(ip_protocol='icmp',from_port=-1, to_port=-1, cidr_ip='0.0.0.0/0')
            group.authorize(ip_protocol='tcp',from_port=22, to_port=22, cidr_ip='0.0.0.0/0')
            group.authorize(ip_protocol='tcp',from_port=80, to_port=80, cidr_ip='0.0.0.0/0')
    except ec2.ResponseError, e:
            if e.code == 'InvalidPermission.Duplicate':
                print e.code
            else:
                raise


    #Start a new instance
    reservation_object=ec2.run_instances(image_id='ami-cd5311fd',key_name=key_name,security_groups=[group_name],instance_type='t1.micro')
    instance = reservation_object.instances[0]

    while(instance.state != 'running'):
        instance.update()

    static_address = ec2.allocate_address()
    static_address.associate(instance.id)
    print 'Instance successfully launched'

    reservations = ec2.get_all_instances(instance_ids=[instance.id])
    instance2 = reservations[0].instances[0]

    #Install packages
    for command in install_commands:
        os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' '+command)

    #Transfer files
    os.system('zip -r csc326 csc326/*')
    os.system('scp -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem '+file_name+' ubuntu@'+static_address.public_ip+':~/'+remote_path)

    #Launch engine
    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' unzip -j csc326.zip')

    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mkdir static')
    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mv QueryMaster-logo4.jpg static')
    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mv main.js static')

    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mkdir views')
    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mv search_result.tpl views')
    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' mv main_search_page.html views')

    os.system('ssh -o StrictHostKeyChecking=no -i '+path+ key_name+'.pem ubuntu@'+static_address.public_ip+' sudo nohup python webserver.py '+instance2.public_dns_name+' &')

    print 'Search Engine launched at ' + instance2.public_dns_name + ' with instance ID: ' + str(instance2.id)

start_instance()