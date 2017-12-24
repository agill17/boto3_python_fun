import boto3
import os
import random

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
		print ("INFO: The bucket '%s' exists" % name)
		return True
	else:
		print ("INFO: The bucket '%s' does not exists" % name)
		return False


def create_bucket(name):
	s3 = boto3.client('s3')
	exists = bucket_exists(name)
	if name != None and exists == False:
		s3.create_bucket(Bucket=name)
		print ("INFO: Created new s3 bucket: %s" % name)


def create_folder_in_bucket(bucket_name, folder_name = 'test_bucket'):
	s3 = boto3.client('s3')
	if bucket_exists(bucket_name):
		s3.put_object(Bucket=bucket_name,Key=folder_name+'/')
	else:
		print ('ERROR: Bucket %s does not exist!!!' % bucket_name)


def delete_bucket(name):
	s3 = boto3.client('s3')
	if name != None and bucket_exists(name) == True:
		s3.delete_bucket(Bucket=name)
		print ("Bucket %s deleted!" % name)

create_bucket("amrit-test-boto3-bucket2")
# delete_bucket("amrit-test-boto3-bucket")
# bucket_exists("amrit-test-boto3-bucket2")
create_folder_in_bucket("amrit-test-boto3-bucket2")