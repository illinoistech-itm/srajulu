#!/bin/bash

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

SGID=$(aws ec2 describe-security-groups --query 'SecurityGroups[0].GroupId')
#SUBNETIDS=$(aws ec2 describe-subnets --query "Subnets[0:2:1].SubnetId")

SUBNETID1=$(aws ec2 describe-subnets --query "Subnets[0].SubnetId")
SUBNETID2=$(aws ec2 describe-subnets --query "Subnets[1].SubnetId")

aws ec2 run-instances \
    --image-id $1 \
    --instance-type $2 \
    --count $3 \
    --subnet-id $SUBNETID1\
    --key-name $4 \
    --security-group-ids 
    --user-data $5

# Need Code to create Target Groups and then dynamically attach instances (3) in this example
# Need Code to register Targets to Target Group (your instance IDs)


# Need code to create an ELB 
# Need to create ELB listener (where you attach the target-group ARN)
# Need WAIT for the operation to complete


# Need code to create an RDS instance with a read-replica


# Need to create 3 10 GB EC2 EBS Volumes and attach one to each of your EC2 instances
# use xvdf as the device name for each volume

