# k8scd

Prerequisites:

General:
1. Store 3 secrets in Github:
    a. DOCKR_USERNAME
    b. DOCKER_PASSWORD
    c. SSH_KEY (vockey)

Bastion:

1. Open 443 for Github Runner connection
2. Deploy self-hosted runner
sudo yum update -y ; sudo yum install -y libicu


Kind (EC2):

1. Create another EC2 for Kind (t3.medium)
2. Open 22 for ssh from runner connection

