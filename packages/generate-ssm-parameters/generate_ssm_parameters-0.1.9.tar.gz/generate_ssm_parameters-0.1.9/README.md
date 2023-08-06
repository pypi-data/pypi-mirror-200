# ssm-parameter-generator

This script generates SSM parameters in an AWS account based on the contents of a CSV file.
The CSV file should have the following headers: 
- Name (string)
- Type ("String" | "StringList" | "SecureString")
- Value (string)
- Description (string)

## Usage
To run the script:
- generate-ssm-parameters CSV-FILE-NAME --profile AWS-PROFILE --region AWS-REGION

The script supports the following options:
- profile: specifies the aws profile to use while running the script. Defaults to "default". If no default profile is found, it will try to use the AWS environment variables.
- region: specifies the aws region to use while running the script. Defaults to "us-east-1". # generate-ssm-parameters
