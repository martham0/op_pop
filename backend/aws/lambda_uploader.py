import boto3
import zipfile
import os
import configparser


config = configparser.ConfigParser()
config.read('./aws/config.ini')

# lambda config
function_name = 'op_pop'
# handler = directory_name.handler_name
handler = 'handler.handler'
runtime = 'python3.9'
role = f'arn:aws:iam::{config["aws"]["account_id"]}:role/service-role/demo-lambda-role-kiozgbxt'
zip_file_path = 'lambda_function.zip'
current_directory=os.getcwd()
# print(f'\n-----\n {current_directory}')
source_code_path = current_directory + '/aws/lambda'

# lambda client initialized
lambda_client = boto3.client('lambda',
                             region_name=config['aws']['region'],
                             aws_access_key_id=config['aws']['access_key'],
                             aws_secret_access_key=config['aws']['secret_key'])
# Create a ZIP file containing your Lambda function code
with zipfile.ZipFile(zip_file_path, 'w') as zip:
    print(f'\n---\n{zip}')
    for root, dirs, files in os.walk(source_code_path):
        for file in files:
            print(f'----\n {file}')
            zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_code_path))

with open(zip_file_path,'rb') as f:
    lambda_client.create_function(FunctionName=function_name, Runtime=runtime, Role=role, Code={'ZipFile': f.read()}, Handler=handler)
    # lambda_client.update_function_code(FunctionName=function_name, ZipFile=f.read())

print(f'----\n{lambda_client}')