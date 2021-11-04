#!/bin/bash

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

# Fetching required values


SGID=$(aws ec2 describe-security-groups --query 'SecurityGroups[0].GroupId')
#SUBNETIDS=$(aws ec2 describe-subnets --query "Subnets[0:2:1].SubnetId")
echo $SGID

SUBNETID1=$(aws ec2 describe-subnets --query "Subnets[0].SubnetId")
SUBNETID2=$(aws ec2 describe-subnets --query "Subnets[1].SubnetId")
echo $SUBNETID1
echo $SUBNETID2

#Using arrays for subnetids
SUBNETARRAY=($(aws ec2 describe-subnets --query "Subnets[*].SubnetId" --output text))
#echo ${SUBNETARRAY[0]}

IDS=$(aws ec2 run-instances \
    --image-id $1 \
    --instance-type $2 \
    --count $3 \
    --subnet-id $SUBNETID1\
    --key-name $4 \
    --security-group-ids $SGID
    --user-data $5]
    --tag-specifications 'ResourceType=instance,Tags=[{Key=mini-project,Value=mp1}]')

IDSARRAY=($( aws ec2 describe-instances --query 'Reservations[].Instances[*].InstanceId' --output text))
echo "Instances created successfully:" 
echo ${IDSARRAY[@]}


# AWS EC2 Waiters
aws ec2 wait instance-running \
    --instance-ids ${IDSARRAY[@]}

echo "Intances are up and running"


#Commented out for testing
:' 
# Need Code to create Target Groups and then dynamically attach instances (3) in this example
VPCID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId')
aws elbv2 create-target-group  \
    --name $6 \
    --protocol HTTP \
    --port 80 \
    --vpc-id $VPCID \
    --health-check-protocol HTTP \
    --health-check-port 80 \
    --target-type instance \

# Need Code to register Targets to Target Group (your instance IDs)
TGARN=$(aws elbv2 describe-target-groups --query 'TargetGroups[0].TargetGroupArn')

for ID in ${IDSARRAY[@]};
do
aws elbv2 register-targets \
    --target-group-arn $TGARN \
    --targets Id=$ID
done


# Need code to create an ELB 
aws elbv2 create-load-balancer \
    --name $7 \
    --subnets $SUBNETID1 $SUBNETID2

aws elbv2 wait load-balancer-available \
    --names $7


# Need to create ELB listener (where you attach the target-group ARN)

#Fetchnig ELB ARN
ELBARN=$(aws elbv2 describe-load-balancers --query 'LoadBalancers[0].LoadBalancerArn')

aws elbv2 create-listener \
    --load-balancer-arn  $ELBARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$TGARN

# Need WAIT for the operation to complete


# Need code to create an RDS instance with a read-replica


# Need to create 3 10 GB EC2 EBS Volumes and attach one to each of your EC2 instances
# use xvdf as the device name for each volume

'