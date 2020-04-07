# EKS

This module is used by the python-terrascript repo and not within this repo.

### After EKS module is finished, you should be able to update kubeconfig and list EKS cluster nodes:
```bash
$ eval $(assume-role dataops-dev administrator <mfa-code>)
Success! IAM session envars are exported.
$ aws eks update-kubeconfig --name cloudops-dev-eks
Updated context arn:aws:eks:eu-west-1:111111111111:cluster/cloudops-dev-eks in /home/toolkit/.kube/config

$ kubectl get nodes -o wide
NAME                                        STATUS   ROLES    AGE   VERSION              INTERNAL-IP   EXTERNAL-IP      OS-IMAGE         KERNEL-VERSION                  CONTAINER-RUNTIME
ip-10-0-17-187.eu-west-1.compute.internal   Ready    <none>   13m   v1.14.7-eks-1861c5   10.0.17.187   52.XX.21.169     Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1
ip-10-0-19-183.eu-west-1.compute.internal   Ready    <none>   12m   v1.14.7-eks-1861c5   10.0.19.183   34.XXX.65.15     Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1
ip-10-0-21-30.eu-west-1.compute.internal    Ready    <none>   12m   v1.14.7-eks-1861c5   10.0.21.30    34.XXX.249.48    Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1
ip-10-0-22-253.eu-west-1.compute.internal   Ready    <none>   13m   v1.14.7-eks-1861c5   10.0.22.253   63.XX.196.5      Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1
ip-10-0-26-1.eu-west-1.compute.internal     Ready    <none>   12m   v1.14.7-eks-1861c5   10.0.26.1     54.XX.164.8      Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1
ip-10-0-26-132.eu-west-1.compute.internal   Ready    <none>   13m   v1.14.7-eks-1861c5   10.0.26.132   34.XXX.224.198   Amazon Linux 2   4.14.146-119.123.amzn2.x86_64   docker://18.6.1```
