# python-s3-upload

In this guide it shows on how to upload s3 with multiple files.

# How to use
1. Install the pip packages

```bash
pip install -r requirements.txt
```

2. Edit the local_file_pattern and folder_prefix to your S3

```python
if __name__ == "__main__":
    local_file_pattern = 'C:/Users/Name/Desktop/images/*.jpg'  # Pattern for files to upload
    folder_prefix = 'Main_Folder/Folder_Example'  # Folder in the bucket

    upload_files_to_s3(local_file_pattern, AWS_STORAGE_BUCKET_NAME, folder_prefix)
```

3. Run the python s3 upload script
```bash
python s3-upload.py
```