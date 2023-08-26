import boto3

client = boto3.client('ecr')

repository_name = "my-cloud-native-repo-for-monitoring"

response = client.create_repository(repositoryName = repository_name)

repository_uri = response['repository']['repositoryUri']
print(repository_uri)
