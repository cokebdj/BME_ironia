import os
from subprocess import check_output

import boto3

s3 = boto3.client('s3')
out = str(check_output(["gsutil", "ls","gs://miax5ajg/ironiabme/Data"]),'utf-8')
files = [file for file in out.split('\n') if 'data' in file]
for file in files:
    print(f"\nProcessing file: {file}")
    out = str(check_output(["gsutil", "cp",file,"."]),'utf-8')
    print(out)
    local_name = file.split('/')[-1]
    with open(local_name, "rb") as f:
        s3.upload_fileobj(f, "ironiabmeajg", local_name)
    print(f"File {file} uploaded!")
    os.remove(local_name)
    print(f"File {file} removed!\n")

print(f"Process finished")