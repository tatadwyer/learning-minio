#import urllib3
from minio import Minio

# Acessar mc client já criado e que tenha as chaves
# Connect to minio and run code: 
# pip3 install minio
# python3 bucket_trial.py

client = Minio(endpoint="192.168.0.10:9000",
               access_key="minioadmin", #userID
               secret_key="minioadmin", #password
               secure=False)
print(client)
print("Total buckets:", len(client.list_buckets()))

# O ideal é usar secure=True, porém seria necessária configuração de TLS e gerar certificado, ao usar o True
# aqui, apresenta erro SSL:WRONG_VERSION_NUMBER e HTTPSConnectionPool
# ver documentação: https://min.io/docs/minio/linux/operations/network-encryption.html?ref=docs-redirect


# Criar um bucket

bucket_name = "bucket-teste-python"

client.make_bucket(bucket_name)

if client.bucket_exists(bucket_name):
    print(bucket_name, "exists.")
else:
    print(bucket_name, "does not exist.")


# Upload de arquivo para o bucket

object_name = "nome_da_imagem.jpg"
file_path = "/tmp/trial/zebuscape.jpg"
content_type = "image/jpg"

result = client.fput_object(bucket_name, object_name, file_path, content_type)
print(
    "Created {0} with etag: {1}, version-id {2}".format(result.object_name, result.etag, result.version_id)
)

# Download de arquivo do bucket

download_path = "/tmp/trial/zebuscape.jpg"

result = client.fget_object(bucket_name, object_name, download_path)
print(
    "Download {0} with etag: {1}, version-id: {2}".format(result.object_name, result.etag, result.version_id)
)

# List buckets

buckets = client.list_buckets()
for bucket in buckets:
    print("Name:", bucket.name, "Creation date:", bucket.creation_date)

# List objects

objects = client.list_objects(bucket_name)
for obj in objects:
    print(obj)