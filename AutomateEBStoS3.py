# Task - Automated EBS Snapshots to S3 using AWS Lambda

import boto3

# Helper function to get all regions
def get_regions(ec2_client):
    return [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]


# Handler
def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    
    # Get list of regions usign helper function
    regions = get_regions(ec2_client)

    # Iterate over regions
    for region in regions:
        print (f"Checking region: {region}")
        reg = region

        # Connect to region
        ec2 = boto3.client('ec2', region_name=reg)
    
        # Get all in-use volumes in regions  
        result = ec2.describe_volumes( 
            Filters=[{
                "Name": 'status', 
                "Values": ['in-use']
            }]
        )
        
        for volume in result['Volumes']:
            print (f"Backing up {volume['VolumeId']} in {volume['AvailabilityZone']}")
        
            # Create snapshot
            result = ec2.create_snapshot(
                VolumeId = volume['VolumeId'],
                Description = "Created by Lambda backup function: ebs-snapshots"
            )
        
            # Get snapshot resource 
            ec2resource = boto3.resource('ec2', region_name=reg)
            snapshot = ec2resource.Snapshot(result['SnapshotId'])
        
            # Find name tag for volume if it exists
            if 'Tags' in volume:
                for tags in volume['Tags']:
                    if tags["Key"] == 'Name':
                        volumename = tags["Value"]   
            else:
                volumename = 'N/A'
                        
        
            # Add volume name to snapshot for easy identification
            snapshot.create_tags(Tags=[{
                'Key': 'Name', 
                'Value': volumename
                }]
            )

    return "Done"


# regions = ec2.describe_regions().get('Regions',[] )