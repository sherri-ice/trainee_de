import boto3

if __name__ == '__main__':
    aws_endpoint_url = 'localhost:4566'
    aws_access_key = 'mock_access_key'
    aws_secret_key = 'mock_secret_key'
    aws_region_name = 'us-east-1'
    s3_resource = boto3.resource('s3',
                                 endpoint_url="http://172.25.0.6:4566",
                                 aws_access_key_id=aws_access_key,
                                 aws_secret_access_key=aws_secret_key,
                                 region_name=aws_region_name)
    print(aws_region_name)

    for b in s3_resource.buckets.all():
        print(b.name)
