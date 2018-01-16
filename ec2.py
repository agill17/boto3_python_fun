import boto3


### TODO: Wait till instance state is running and then append to list
def get_all_instances(region='us-east-1'):
	ec2 = boto3.resource('ec2',region_name=region)
	all_instances = ec2.instances.all()
	active_instances = []
	for each in all_instances:
		current_state = each.state.get('Name')
		if current_state == 'running':
			active_instances.append(each)
	return active_instances


def create_instance(name="tomcat_elb",maxx=1,region='us-east-1'):
	ec2_name = name+"{:%Y%m%d%H%M%S}".format(datetime.datetime.now())
	ec2 = boto3.resource('ec2', region_name=region)
	instance = ec2.create_instances(
		ImageId = 'ami-aa2ea6d0',
		MinCount = 1,
		MaxCount = maxx,
		InstanceType = 't2.micro',
		KeyName='imac_2018',
		TagSpecifications=[
			{
				'ResourceType':'instance',
				'Tags':[
					{
						'Key': 'Name',
						'Value':ec2_name
					}
				]
			}
		]
	)
	ins = instance[0]
	ins.wait_until_running()
	ins.load() ## reload
	instances = ins.id
	print "Instance Initliazed %s " % instances
	return instances


def desc_instances(ins_ids,region='us-east-1'):
	ec2 = boto3.client('ec2')
	bootstrap = {}
	all_bootstraps = []
	ins = ec2.describe_instances(InstanceIds=ins_ids)

	for each_running in ins['Reservations']:
		key = None
		fqdn = None
		name = None
		ins_id = None

		for each in each_running['Instances']:
			
			key = each['KeyName']
			fqdn = each['PublicDnsName']
			name = each['Tags'][0]['Value']
			ins_id = each['InstanceId'] 
			break

		bootstrap = {'key':key, 'fqdn':fqdn,'name':name, 'ins_id':ins_id}
		all_bootstraps.append(bootstrap)
	print all_bootstraps
	return all_bootstraps


def terminate_instance(instance_id=None, region='us-east-1'):
	ec2 = boto3.resource('ec2', region_name=region)
	if instance_id == None:
		### destory them all
		instances = get_all_instances(region)
		for each in instances:
			each.terminate()
			print ("Terminating: %s " % each)
	else:
		ec2.instances.filter(InstanceIds=instance_id).terminate()


create_instance('test', 'state', 'non_stop')
# get_all_instances()
# terminate_instance()


