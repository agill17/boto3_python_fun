import boto3


b_name = 'amrit-test-boto3-bucket'


def get_all_bucket_names():
	s3 = boto3.client('s3')
	bucket_names = []
	all_buckets = s3.list_buckets()
	for each_bucket in all_buckets['Buckets']:
		bucket_names.append(each_bucket['Name'])

	return bucket_names

def bucket_exists(name):
	s3 = boto3.client('s3')
	bucket_names = get_all_bucket_names()
	if name in bucket_names:
		print ("INFO: The bucket %s already exists" % name)
		return True
	else:
		print ("INFO: The bucket %s does not exists" % name)
		return False


def create_bucket(name):
	s3 = boto3.client('s3')
	exists = bucket_exists(name)
	if name != None and exists == False:
		s3.create_bucket(Bucket=name)
		print ("Created new s3 bucket: %s" % name)


def delete_bucket(name):
	s3 = boto3.client('s3')
	if name != None and bucket_exists(name) == True:
		s3.delete_bucket(Bucket=name)
		print ("Bucket %s deleted!" % name)


# create_bucket("amrit-test-boto3-bucket2")
delete_bucket("amrit-test-boto3-bucket2")
# bucket_exists("amrit-test-boto3-bucket2")