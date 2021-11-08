#!/bin/bash

export AWS_PAGER="" 
#https://stackoverflow.com/questions/60122188/how-to-turn-off-the-pager-for-aws-cli-return-value

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

# Example Script to dynamically terminate all running EC2 instances
#IDSARRAY=$(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Code==`16`].InstanceId' --output text)

#Fetching the values needed to take down the environment

#Filter to fetch running instances with tag value "mp1"
IDSARRAY=$(aws ec2 describe-instances \
    --query 'Reservations[*].Instances[?State.Name==`running` && Tags[?Value==`mp1`]].InstanceId')

#Target group ARN
TGARN=$(aws elbv2 describe-target-groups \
    --query 'TargetGroups[0].TargetGroupArn')

#DB-ids
DBID=$(aws rds describe-db-instances \
    --query 'DBInstances[?DBInstanceStatus==`available`].DBInstanceIdentifier')

#ELB ARN
ELBARN=$(aws elbv2 describe-load-balancers \
    --query 'LoadBalancers[0].LoadBalancerArn')

#Delete db-instance
echo "Deleting database instances and read replicas"
for DBID in ${DBIDSARRAY[@]};
do
    aws rds delete-db-instance --db-instance-identifier $DBID --skip-final-snapshot
    aws rds wait db-instance-deleted --db-instance-identifier $DBID
done

#Terminating instances with tag value mp1
aws ec2 terminate-instances \
    --instance-ids $IDSARRAY

aws ec2 instance-terminated \
    --instance-ids $IDSARRAY

#Delete ELB
aws elbv2 delete-load-balancer \
    --load-balancer-arn $ELBARN

#Deregistering targets from target groups
for ID in ${IDSARRAY[@]};
do
aws elbv2 deregister-targets --target-group-arn $TGARN --targets Id=$ID
aws elbv2 wait target-deregistered --target-group-arn $TGARN --targets Id=$ID
done

#Delete target groupss
aws elbv2 delete-target-group \
    --target-group-arn $TGARN

