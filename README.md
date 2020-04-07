# python-terrascript

# Introduction
Python Terrascript Terraform Module Generator:- This repo used Python code in conjunction with the 
 [python-terrascript](https://github.com/mjuenema/python-terrascript) package along with the 
[terraform-framework](https://github.com/dieple/terraform-framework) to generate terraform code and apply terraform
 to build AWS resources against a target AWS account. We normally assume role into the "build account" to run python-terrascript. 
 All the S3 state files are saved locally within the build account and there is no need to store the state file on the destination account.


## Scope

This document describes how to use this tool to build AWS resources, such as 
* VPC 
* IAMs
* Lambda functions
* Codebuild/Pipeline
* EKS
* Dynamodb
* and so on.  

This tool can be built on any accounts/environments in a DRY code concept.


## Background

#### Reference Repos

1. https://github.com/dieple/cloud-native-toolkit.git <<< builder tools - docker image for local development environment
1. https://github.com/dieple/terraform-framework.git <<< terraform repo - contains generic terraform modules to be invoked by python-terrascript


This repo has a few dependencies:

- [docker](https://www.docker.com/products/docker-desktop)
- [Terraform 0.12](https://learn.hashicorp.com/terraform/getting-started/install.html)
- [Cloud native toolkit](https://github.com/dieple/cloud-native-toolkit) - local development env for AWS assume role to build.
- [terraform-framework](https://github.com/dieple/terraform-framework) - if you want to develop and deploy terraform manually
- [python-terrascript](https://github.com/dieple/python-terrascript) - if you want to use python to generate terraform code.


### Prerequisites
- Setup AWS credentials:
```bash
$ #Modify AWs account to your env
$ cat $HOME/.aws/accounts
{
  "dataops-dev": "1111111111111",
  "dataops-staging": "2222222222222",
  "dataops-prod": "3333333333333",
  "cloudops-dev": "4444444444444",
  "cloudops-staging": "5555555555555",
  "cloudops-prod": "6666666666666",
  "platform-dev": "7777777777777"
}
```

```bash
$ cat $HOME/.aws/config
[default]
region = eu-west-1
output = json
mfa_serial=<your-organisation-mfa-serial-arn>
```

```bash
$ cat $HOME/.aws/credentials
[default]
aws_access_key_id = <your-aws-access-key-id>
aws_secret_access_key = <your-aws-secret-access-key>
```

- mkdir -p $HOME/{repos,.aws,.kube, .ssh, .terraform.d/plugin-cache} on your host machine
- cd $HOME/repos
- git clone https://github.com/dieple/cloud-native-toolkit toolkit
- git clone https://github.com/dieple/python-terrascript.git terrascript

#### Toolkit

To interact with DataOps AWS accounts and EKS clusters, it is recommended to use the 
`toolkit` Docker image so we all use a consistent toolchain.

---

### Start the Toolkit Docker Image

Note - the `toolkit` container mounts a local directory 
containing your source code to `/repos`, which we use further below! 

```bash
$ cd $HOME/repos/toolkit  # <<< cd to your clone of the toolkit repo...
$ ./run_toolkit.sh -v 0.0.6
$ # then assume role 
$ #eval $(assume-role <account-alias-as-defined-in-$HOME/.aws/account> <role-name> <mfa-code>)
$ eval $(assume-role dataops-dev administrator 123456)
$ cd terrascript 
$ # read the README file how to start python-terrascript development and building AWS resources
```

This puts you inside the Docker image  ready for local development env.
