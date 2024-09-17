# AWS Resource Listing Script
This repository contains a Python script that uses the `boto3` library to list all AWS resources in an account, organized by region. The script retrieves details for various resource types, including EC2 instances, RDS databases, S3 buckets, Lambda functions, and VPCs.

## Prerequisites
Before we begin, need following installed:

- [Python](https://www.python.org/downloads/) (version 3.6 or later)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) library. we need to it using pip:
  ```bash
  pip install boto3
