import boto3
import glob
import os
import sys
from dotenv import dotenv_values
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

env_vars = dotenv_values()

# Configuration from environment variables
AWS_ACCESS_KEY_ID = env_vars.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env_vars.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env_vars.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = env_vars.get("AWS_S3_REGION_NAME")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)

def print_progress_bar(iteration, total, prefix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% Complete')
    sys.stdout.flush()

def upload_files_to_s3(local_file_pattern, bucket_name, folder_prefix):
    try:
        # Get list of files matching the pattern
        files = glob.glob(local_file_pattern)
        print(f"Files found for pattern {local_file_pattern}: {files}")
        total_files = len(files)
        
        if total_files == 0:
            print("No files found matching the pattern.")
            return

        print(f"Starting upload of {total_files} files...")
        
        for i, local_file_path in enumerate(files, start=1):
            file_name = os.path.basename(local_file_path)
            s3_key = f'{folder_prefix}/{file_name}'

            content_type = 'image/webp'
            
            # Upload file with specified content type
            s3_client.upload_file(
                local_file_path, 
                bucket_name, 
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            print(f"\nFile {file_name} uploaded successfully to {s3_key} in bucket {bucket_name}.")
            print_progress_bar(i, total_files, prefix='Progress')
        
        print("\nAll files uploaded successfully.")

    except NoCredentialsError:
        print("Credentials not available.")
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    local_file_pattern = 'C:/Users/Name/Desktop/images/*.webp'  # Pattern for files to upload
    folder_prefix = 'blog_app/blog_photo_main'  # Folder in the bucket

    upload_files_to_s3(local_file_pattern, AWS_STORAGE_BUCKET_NAME, folder_prefix)