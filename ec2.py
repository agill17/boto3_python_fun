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


def create_instance(name, tag_key, tag_val, region='us-east-1'):
	ec2 = boto3.resource('ec2', region_name=region)
	instance = ec2.create_instances(
		ImageId = 'ami-aa2ea6d0',
	    MinCount = 1,
	    MaxCount = 1,
	    KeyName = 'imac_new',
	    InstanceType = 't2.micro'
	)
	ec2.create_tags(
                    Resources = ['i-06531c6653fdaed9e'],
                    Tags = [{'Key': tag_key, 'Value': tag_val}]
                    )


def terminate_instance(instance_id=None, region='us-east-1'):
	ec2 = boto3.resource('ec2', region_name=region)
	if instance_id == None:
		### destory them all
		instances = get_all_instances(region)
		for each in instances:
			each.terminate()
	else:
		ec2.instances.filter(InstanceIds=instance_id).terminate()


create_instance('test', 'Key_name', 'Value_amrit-test')
get_all_instances()
terminate_instance()


