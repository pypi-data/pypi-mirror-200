[![release](https://github.com/yvthepief/dapl_secure_bucket/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/yvthepief/dapl_secure_bucket/actions/workflows/release.yml)

# DAPL Secure Bucket Construcs

This Secure Bucket construcs extends the S3 Bucket construct. When using this construct, you will create a S3 bucket with default security best practises enabled. These are:

* Block public access
* Enabled versioning
* Enable enforce SSL to connect to bucket
* Enabled Bucket access logging
* Encryption of the bucket with a customer managed KMS key with enabled key rotation and trusted account identities and admins.
* Lifecycle management on objects, move items to Infrequently Access after one month

These best practises are enforced. When creating a SecureBucket with for example versioning disabled, it will be overwritten to enabled.

# Usage

## install package

```bash
npm install @dapl_secure_bucket
```

## Import the secure bucket construct in your code.

```python
// Import necessary packages
import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { SecureBucket } from 'dapl-secure-bucket';

export class SecureBucketStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new SecureBucket(this, 'myEnterpriseLevelSecureBucket',{});
  }
}
```
