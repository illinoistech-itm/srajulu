#!/bin/bash

export AWS_PAGER="" 
#https://stackoverflow.com/questions/60122188/how-to-turn-off-the-pager-for-aws-cli-return-value

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

# Fetching required values

echo "CREATING MP1 ENVIRONMENT"
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
    --tag-specifications 'ResourceType=instance,Tags=[{Key=mini-project,Value=mp1}]'


#Fetching only instances related to mp1, optimised for ec2 waiter
IDSWAITARRAY=($(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`pending` && Tags[?Value==`mp1`]].InstanceId'))

# AWS EC2 Waiters
aws ec2 wait instance-running \
    --instance-ids ${IDSWAITARRAY[@]}

IDSARRAY=($(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running` && Tags[?Value==`mp1`]].InstanceId'))

echo "Intances are up and running"
echo ${IDSARRAY[@]}
echo "--------------------------------------------------------------------"

# Need Code to create Target Groups and then dynamically attach instances (3) in this example
echo "Creating Target groups"
VPCID=$(aws ec2 describe-vpcs --query 'Vpcs[0].VpcId')
aws elbv2 create-target-group  \
    --name $6 \
    --protocol HTTP \
    --port 80 \
    --vpc-id $VPCID \
    --health-check-protocol HTTP \
    --health-check-port 80 \
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

# Need WAIT for the operation to complete


# Need code to create an RDS instance with a read-replica
echo "Creating RDS instance"

aws rds create-db-instance \
    --db-instance-identifier $8 \
    --db-instance-class $9 \
    --engine ${10} \
    --master-username ${11} \
    --master-user-password ${12} \
    --allocated-storage ${13}

#RDS waiter
aws rds wait db-instance-available \
    --db-instance-identifier $8

echo "RDS Instance created."

echo "Creating read replicas"
aws rds create-db-instance-read-replica \
    --db-instance-identifier db-sgr-replica \
    --source-db-instance-identifier $8
echo "Read replica created"

echo "Waiting for db-instance to become available"

#RDS waiter
aws rds wait db-instance-available \
    --db-instance-identifier db-sgr-replica

echo "MP1 Environment created"