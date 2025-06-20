```makrdown
hybrid cloud data transfer and processing workflow using AWS Transfer Family, S3, and on-premise systems
```

**Steps**

```markdown
1. S3 bucket creation
2. Service Account Creation
      * The SA will have IAM role attached to the service to allow the pod to
            - send data to S3 staging bucket for validation
            - send validated data to the SFTP bucket
            - And these both will be performed by cronjob
3. Workflow
  * The service pod will use IAM role to
      - send data to S3 staging bucket for validation
      - once validated, the data will be send to the SFTP bucket
4. On-Prem control m will then download the data from the SFTP bucket
```

**Configuration**

```markdown
Create S3 bucket specifically for AWS Transfer family SFTP service
The bucket is configured with
      -   AWS Transfer Family SFTP Server --> ensure secure file transfer
      -   SFTP VPC endpoint --> Ensure Traffic flow over private Direct Connect instead of public internet
      -   IAM role --> Grant SFTP server permission to access S3 bucket
      -   Server Side Encryption --> Ensure data is encrypted at rest using AWS KMS

SSH Key to authenticate Transfer Family
Store the key in secret manager
The private key is stored and securely accessed by Control-M
```
**Control M Configuration**

```markdown
Configure a Control-M managed file transfer job to download files from SFTP S3 bucket
Connection Profile:
    Define SFTP endpoint , credentails SSH keys
    Ensure connection uses private SFTP VPC endpoint
File Download Job:
    Schedule a control M job to connect to AWS Transfer family SFTP server
    Download files from S3 bucket to on-premise destination fileshare

Open port 22 on cloud to allow SFTP traffic between Control-M server and AWS Transfer Family SFTP server


File Generation Process

CronJob Scheduling:
a. Kubernetes CronJobs are used to schedule file generation tasks at regular intervals.
b. The CronJob triggers a pod that runs the necessary logic to generate files.

File Creation:
a. The service pod interacts with various APIs and services to gather data and generate files.
b. The files are stored in the Staging Bucket or other specified locations.

File Storage:
a. Files are uploaded to the S3 staging bucket for temporary storage.
b. The generated files are prefixed with a specific naming convention into a folder in sftp bucket for easy identification.

Reporting Configuration

AWS Region: eu-west-2

Staging Bucket: Temporary storage for generated files.

Report Bucket: Final destination for reports. SFTP Bucket

File Prefix: Naming convention for generated files, e.g., eIDVAPPSTORE_EDBH_<ENVIRONMENT>.

File Placement in S3:

Files are uploaded to the S3 bucket by cronjob.

The AWS Transfer Family SFTP server provides secure access to the bucket.

File Download by Control-M:

Control-M connects to the AWS Transfer Family SFTP server using the private SSH key.

Files are downloaded from the S3 bucket to the on-premises destination fileshare.
```
