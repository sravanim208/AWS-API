import boto3

def list_aws_resources():
    # Create a session using your AWS credentials
    session = boto3.Session()
    
    # Get a list of all available regions for the services
    regions = session.get_available_regions('ec2')

    # Dictionary to hold resources by region
    resources_by_region = {}

    for region in regions:
        print(f"Listing resources in region: {region}")
        resources_by_region[region] = {}

        # Create a session for the specific region
        regional_session = boto3.Session(region_name=region)

        # List EC2 instances
        ec2 = regional_session.resource('ec2')
        instances = ec2.instances.all()
        resources_by_region[region]['EC2'] = []
        for instance in instances:
            resources_by_region[region]['EC2'].append({
                'InstanceId': instance.id,
                'InstanceType': instance.instance_type,
                'State': instance.state['Name'],
                'PublicIpAddress': instance.public_ip_address,
                'LaunchTime': instance.launch_time
            })

        # List RDS instances
        rds = regional_session.client('rds')
        rds_instances = rds.describe_db_instances()
        resources_by_region[region]['RDS'] = []
        for db_instance in rds_instances['DBInstances']:
            resources_by_region[region]['RDS'].append({
                'DBInstanceIdentifier': db_instance['DBInstanceIdentifier'],
                'DBInstanceClass': db_instance['DBInstanceClass'],
                'Engine': db_instance['Engine'],
                'DBInstanceStatus': db_instance['DBInstanceStatus'],
                'Endpoint': db_instance.get('Endpoint', {}).get('Address', 'N/A')
            })

        # List S3 buckets
        s3 = regional_session.client('s3')
        s3_buckets = s3.list_buckets()
        resources_by_region[region]['S3'] = []
        for bucket in s3_buckets['Buckets']:
            resources_by_region[region]['S3'].append({
                'BucketName': bucket['Name'],
                'CreationDate': bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")
            })

        # List Lambda functions
        lambda_client = regional_session.client('lambda')
        lambda_functions = lambda_client.list_functions()
        resources_by_region[region]['Lambda'] = []
        for function in lambda_functions['Functions']:
            resources_by_region[region]['Lambda'].append({
                'FunctionName': function['FunctionName'],
                'Runtime': function['Runtime'],
                'State': function['State'],
                'LastModified': function['LastModified']
            })

        # List VPCs
        vpc_client = regional_session.client('ec2')
        vpcs = vpc_client.describe_vpcs()
        resources_by_region[region]['VPC'] = []
        for vpc in vpcs['Vpcs']:
            resources_by_region[region]['VPC'].append({
                'VpcId': vpc['VpcId'],
                'CidrBlock': vpc['CidrBlock'],
                'State': vpc['State'],
                'IsDefault': vpc['IsDefault']
            })

    return resources_by_region

def print_resources(resources):
    for region, services in resources.items():
        print(f"\nRegion: {region}")
        for service, details in services.items():
            print(f"  Service: {service}")
            for resource in details:
                print(f"    {resource}")

if __name__ == "__main__":
    resources = list_aws_resources()
    print_resources(resources)
