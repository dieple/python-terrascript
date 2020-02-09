# terrascript_011x

Steps to generate terraform codes (version >= 0.12.0) using python-terrascript to build infrastructure on AWS.

# Introduction

### Contents

1. [Background](#Background)
1. [Pre-requisites](#Prerequisites)
1. [Use K9s To Explore Kubernetes](#Use-K9s-To-Explore-Kubernetes)


## Scope

This document describes how to use this tool to build AWS resources, such as 
* VPC 
* IAMs
* Security Groups
* Lambda functions
* Codebuild/Pipeline
* EKS
* and so on.  

This tool can be built on any accounts/environments in DRY code concept.

## Background

#### DataOps AWS Accounts

* __dev__ - used for infrastructure testing
* __staging__ - used to host dev and test environments
* __prod__ - used to host the production environment

#### Reference Repos

1. https://github.com/dieple/builder_tools.git <<< builder tools
1. https://github.com/dieple/terraform-modules-011x.git <<< terraform repo


### Prerequisites


This module has a few dependencies:

- [Terraform 0.12](https://learn.hashicorp.com/terraform/getting-started/install.html)
- [Cloud native toolkit](https://github.com/dieple/cloud-native-toolkit) - local development env for AWs assume role to build.
- [terraform-modules-012x](https://github.com/dieple/terraform-modules-012x)
- [terraform-dry-framework](https://github.com/dieple/terraform-dry-framework) - if you want to develop and deploy terraform manually
- [python-terrascript](https://github.com/dieple/python-terrascript) - if you want to use python to generate terraform code.


#### General 

1. mkdir -p $HOME/{repos,.aws,.kube, .ssh, .terraform.d/plugin-cache} on your host machine
1. cd $HOME/repos
1. git clone https://github.com/dieple/cloud-native-toolkit toolkit
1. git clone https://github.com/dieple/python-terrascript.git

#### Toolkit

To interact with DataOps AWS accounts and EKS clusters, it is recommended to use the 
`toolkit` Docker image so we all use a consistent toolchain.

---

### Start the Toolkit Docker Image

Note - the `toolkit` container mounts a local directory 
containing your source code to `/repos`, which we use further below! 

```bash
$ cd $HOME/repos/toolkit  # <<< cd to your clone of the toolkit repo...
$ ./run_toolkit.sh
$ # then assume role 
$ eval $(assume-role <account-alias> <role-name> <mfa-code>)
```

This puts you inside the Docker image with a toolchain and AWS access tokens to continue below...


### Access EKS (Post EKS module installation)

Setup config file `~/.kube/config` so you can use `kubectl` command-line tool as follows:

```bash
$ aws eks list-clusters  
# JSON is output...
# Note the EKS cluster name for use in the next command.
# For example, from the sample below, we grab string 'og8-staging-eks-dataops'
$ aws eks update-kubeconfig --name <cluster-name-from-above> --alias <dev|staging|prod>  
# Choose a simple alias name above!
```

Sample output from command `aws eks list-clusters`:
```json
{
    "clusters": [
        "data-ops-staging-eks"
    ]
}
```

Next, to test that the kube context imported successfully, run the following:

```bash
$ kubectl config get-contexts  
```

This should list metadata for all configured Kubernetes clusters,
including the one that you just imported with the alias name that you used.
There is a `*` against the CURRENT context.  

Next, set your kube config file to use the EKS cluster that you want to interact with. 
This is not required if you just imported the config above as it will be set as the current default.

You can also use this command if you just want to switch between administering 
EKS in different environments/accounts.

```bash
$ kubectl config use-context <alias from above>  # <<< use a context name shown in the output of get-contexts above
``` 

Test that you can talk to the EKS cluster by listing available namespaces as follows:

```bash
$ kubectl get ns  # <<< ns is short for namespaces
```

This should list entries like `kube-system` and `default` along with any others created by developers etc.


---

### Use K9s To Explore Kubernetes

`k9s` is an open-source tool that wraps up the `kubectl` CLI tool and Kubernetes API into a visual terminal app.
By default it uses your current `~/.kube/config` context. 

```bash
$ k9s  # <<< launch k9s using your current context; or...
$ k9s --context <an alias in your ~/.kube/config file>  # <<< use an alternative context without having to switch 
```

The tool is quite simple and you can view the available keyboard shortcuts at the top of the screen.

__Examples__

* Use cursor keys to __navigate__
* Hit enter to __select__
* Hit escape to __go back__ 
* Type `:ns`  <<< __view namespaces__
* Type `:po`  <<< __view pods__ in the current namespace
* Cursor up/down to choose a pod, then hit `s` to __ssh to it__
* Cursor up/down to choose a pod, then hit `y` to view its __YAML definition__
* Cursor up/down to choose a pod, then hit `l` to view its __logs__
 
