#!/bin/bash

export AWS_PAGER="" 
#https://stackoverflow.com/questions/60122188/how-to-turn-off-the-pager-for-aws-cli-return-value

# Reuse all the code from mp1 - remove the RDS content, no need for that in this project

# Use the AWS CLI to Create a S3 Bucket
aws s3 mb s3://${11}

# Create DynamoDB Table
# I am giving you the table creation script for DynamoDB

aws dynamodb create-table --table-name ${10} \
    --attribute-definitions AttributeName=RecordNumber,AttributeType=S AttributeName=Email,AttributeType=S \
    --key-schema AttributeName=Email,KeyType=HASH AttributeName=RecordNumber,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
    --stream-specification StreamEnabled=TRUE,StreamViewType=NEW_AND_OLD_IMAGES

# Create SNS topic (to subscribe the users phone number to)
# Use the AWS CLI to create the SNS
aws sns create-topic \
    --name $9


# Install ELB and EC2 instances here -- remember to add waiters and provide and --iam-instance-profile so that your EC2 instances have permission to access SNS, S3, and DynamoDB
# Sample
#  --iam-instance-profile Name=$8

# Fetching required values

echo "CREATING MP2 ENVIRONMENT"
SGID=$(aws ec2 describe-security-groups --query 'SecurityGroups[0].GroupId')
echo $SGID

SUBNETID1=$(aws ec2 describe-subnets --query "Subnets[0].SubnetId")
SUBNETID2=$(aws ec2 describe-subnets --query "Subnets[1].SubnetId")
echo $SUBNETID1
#echo $SUBNETID2

#Using arrays for subnetids
#SUBNETARRAY=($(aws ec2 describe-subnets --query "Subnets[*].SubnetId" --output text))
#echo ${SUBNETARRAY[0]}
#SUBNETIDS=$(aws ec2 describe-subnets --query "Subnets[0:2:1].SubnetId")

#Launching EC2 instances with tags 

echo "Launching EC2 Instances"

aws ec2 run-instances \
    --image-id $1 \
    --instance-type $2 \
    --count $3 \
    --subnet-id $SUBNETID1\
    --key-name $4 \
    --security-group-ids $SGID \
    --user-data $5 \
    --iam-instance-profile Name=$8 \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=mini-project,Value=mp2}]'


#Fetching only instances related to mp1, optimised for ec2 waiter
IDSWAITARRAY=($(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`pending` && Tags[?Value==`mp2`]].InstanceId'))

# AWS EC2 Waiters
aws ec2 wait instance-running \
    --instance-ids ${IDSWAITARRAY[@]}

IDSARRAY=($(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running` && Tags[?Value==`mp2`]].InstanceId'))

echo "Intances are up and running"
echo ${IDSARRAY[@]}
echo "--------------------------------------------------------------------"

# Need Code to create Target Groups and then dynamically attach instances (3) in this example
echo "Creating Target groups"
VPCID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId')
aws elbv2 create-target-group  \
    --name $6 \
    --protocol HTTP \
    --port 3300 \
    --vpc-id $VPCID \
    --health-check-protocol HTTP \
    --health-check-port 3300 \
    --target-type instance 

echo "--------------------------------------------------------------------"

# Need Code to register Targets to Target Group (your instance IDs)
echo "Registering Target group"
TGARN=$(aws elbv2 describe-target-groups --query 'TargetGroups[0].TargetGroupArn')

for ID in ${IDSARRAY[@]};
do
aws elbv2 register-targets \
    --target-group-arn $TGARN \
    --targets Id=$ID
done

echo "--------------------------------------------------------------------"

# Need code to create an ELB 
echo "Creating ELB"
aws elbv2 create-load-balancer \
    --name $7 \
    --subnets $SUBNETID1 $SUBNETID2 \
    --security-group $SGID

#ELB waiter; wait till ELB is available
aws elbv2 wait load-balancer-available \
    --names $7

echo "ELB Created"
echo "--------------------------------------------------------------------"

# Need to create ELB listener (where you attach the target-group ARN)

#Fetchnig ELB ARN
ELBARN=$(aws elbv2 describe-load-balancers --name $7 --query 'LoadBalancers[0].LoadBalancerArn')

aws elbv2 create-listener \
    --load-balancer-arn  $ELBARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$TGARN

ELBDNSNAME=$(aws elbv2 describe-load-balancers --query 'LoadBalancers[0].DNSName')

echo "ELB URL:" $ELBDNSNAME

#links $ELBDNSNAME

echo "MP2 Environment created"