# 1. DESIGN
In this section, I will design the system using AWS services with 3-tiers as following:
- Front-end layer: interactive with user
- Back-end layer: processing business logic
- Database layer: Storing user data 

![image](https://user-images.githubusercontent.com/28616641/203497996-efb3faa9-6899-47a7-a30b-3af415ee86dd.png)

## 1.1 Overview infrastructure
### 1.1.1 Components
- For high availability, the system and all its application will sit in 2 AZs and in each AZ will have 1 public, 1 private subnet, 1 bastion host, 1 NAT gateway.

- For CICD, I use Github Action and CodePipline

- Beside, I also use other common AWS services:
+ Route 53: Redirect domain to cloudfront
+ WAF: Limit access and filter malicious traffic
+ ACM: Provision, manage, and deploy certificates.
+ Cloudfront: Content delivery network (CDN) service for increasing speed the static and dynamic content.
+ EKS: Managed Kubernetes service to run Kubernetes in the AWS
+ GuarDuty:  Threat detection service that continuously monitors for malicious activity and unauthorized behavior.
+ Cloudtrail: Monitors and records account activity 
+ S3: object file storage and will set with life cycle policy: after 30 days move to S3 Intelligent-Tiering and 90 days move to S3 Glacier 
      And after 180 days will move to S3 Glacier Deep Archive
+ KMS: for envelop encryption S3 object and EKS secret.

### 1.1.2 Data workflow
- When user access to domain, Route53 will redirect the traffic to Cloudfront which put the WAF rules.
On these WAF rules, we will set for limiting the IP, regrex pattern, number requests,...
- After passing these rules, the traffic will continue going to ELB. Security group will be applied here for limiting which IP and port can access.
In the case denied specific IP, we can use NACLS.
- Then the traffic will go to target group which integrated service by EKS cluster.
- At the EKS cluster level, we have 2 services: front end and back end. The traffic after goes through front end and will connect to backend.
  The backend will connect to database for storing and quering data. 
- For improving latency and speed, we have additional caching layer using Elastic cache.

### 1.1.3 CICD workflow
- I use Github action and Codebuild for CICD
- When a developer push and create new pull request, it will trigger Github action and push manifest to S3 bucket.
- New event in S3 will trigger the Codpipeline and after that, it will be build and deploy application on EKS cluster.

### 1.1.5 Logging
- Logs(system, EKS, application) will be stored in S3 and filter by Cloudwatch to trigger and then send alert to monitoring system.

### 1.1.4 Monitoring
- I use Cloudwatch, third parties product(Newrelic/Datadog) for monitoring

## 1.2 Security
- Limiting IP and filter vulnerability traffic by WAF, security group and NACLs.
- IAM role for technicians when accessing services in private subnet.
- Using KMS for encryption objects in S3, secret in EKS.
- Using GuarDuty for threat detection service that continuously monitors for malicious activity and unauthorized behavior.
- Cloudtrail for Monitoring and recording account activity for auditing.

## 1.3 Performance
- Cloudfront for caching static and dynamic content
- Elastic cache for caching database queries