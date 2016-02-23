import sys
import boto

region = ''
aws_access_key_id=''
aws_secret_access_key = ''

def terminateInstance(instance_id):
    #Establish connection to aws
    ec2 = boto.connect_ec2(aws_access_key_id,aws_secret_access_key)
    ec2 = boto.ec2.connect_to_region(region)

    ec2.terminate_instances(instance_ids=[instance_id])

    for instance in ec2.get_all_instances():
        if instance.id == instance_id:
            print 'Instance termination fail'
            return

    print 'Instance termination success'

terminateInstance(sys.argv[1])
