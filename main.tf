terraform {
  required_providers {
    minio = {
      # ATTENTION: use the current version here!
      version = "RELEASE.2023-04-07T05-28-58Z"
      source  = "refaktory/minio"
    }
  }
}

provider "minio" {
    endpoint = "localhost:9000"
    access_key = "adminio"
    secret_key = "adminio"
    #ssl = false
}

# Create a bucket.
resource "minio_bucket" "bucket" {
  name = "bucket1"
}

# Create a policy.
# User de NF, pode ver o bucket, fazer upload e donwload apenas para esse bucket.
resource "minio_canned_policy" "policy1" {
  name = "policy1"
  policy = <<EOT
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": [
                "s3:ListAllMyBuckets"
            ],
            "Resource": [
                "arn:aws:s3:::*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::bucket1"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListMultipartUploadParts",
                "s3:AbortMultipartUpload"
            ],
            "Resource": [
                "arn:aws:s3:::bucket1/*"
            ]
        }
    ]
}
EOT
}

# Create a user with specified access credentials, policies and group membership.
resource "minio_user" "user1" {
  name = "user1"
  access_key = "user-access-key"
  secret_key = "user-secret-key"
  policies = [minio_canned_policy.policy1.name]
}
