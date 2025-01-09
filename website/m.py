from minio import Minio

if __name__ == '__main__':
    client = Minio("127.0.0.1:9000",
                   access_key="YOUR_ACCESS_KEY",
                   secret_key="YOUR_SECRET_KEY",
                   secure=False
                   )
    bucket_name = "docs"
    destination_file = "19.docx"
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
        print("Created bucket", bucket_name)
    else:
        print("Bucket", bucket_name, "already exists")

    response, document = None, None
    try:
        response = client.get_object(bucket_name, destination_file)
        document = response.data    # Read data from response.
    finally:
        if response:
            response.close()
            response.release_conn()

    print(document)