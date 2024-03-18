import boto3
import zipfile
import os
import configparser
from dotenv import load_dotenv
import argparse

parser = argparse.ArgumentParser(description="zip lamda source code")
parser.add_argument("-n", "--function_name", type=str, help="The name to be given to the function")
parser.add_argument("-d", "--function_dir", type=str, help="The directory to package lambda source code")
parser.add_argument("-l", "--handler_name", type=str, help="handler file and file name directory_name.handler_name ex: lambda.handler")
args = parser.parse_args()

load_dotenv("./config.env")

# Access the environment variable
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID")
AWS_ROLE = os.getenv("AWS_ROLE")

# lambda config
function_name = args.function_name
handler = args.handler_name
runtime = "python3.9"
role = AWS_ROLE
zip_file_path = "lambda_function.zip"
current_directory = os.getcwd()

print(f"\n-----current dir\n {current_directory}")
source_code_path = current_directory + f"/src/aws/{args.function_dir}"
print(f"\n-----src code dir\n {source_code_path}")

# lambda client initialized
lambda_client = boto3.client("lambda",
                             region_name=AWS_REGION,
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY)
# Create a ZIP file containing your Lambda function code
with zipfile.ZipFile(zip_file_path, "w") as zip:
    print(f"\n---what is zip\n{zip}")
    for root, dirs, files in os.walk(source_code_path):
        for file in files:
            print(f"----FILE\n {file}")
            zip.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), source_code_path))

with open(zip_file_path, "rb") as f:
    lambda_client.create_function(FunctionName=function_name, Runtime=runtime, Role=role, Code={"ZipFile": f.read()},
                                  Handler=handler)
    # lambda_client.update_function_code(FunctionName=function_name, ZipFile=f.read())
