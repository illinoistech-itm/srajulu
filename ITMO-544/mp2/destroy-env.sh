#!/bin/bash
export AWS_PAGER="" 
#https://stackoverflow.com/questions/60122188/how-to-turn-off-the-pager-for-aws-cli-return-value

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

#Deleting S3 bucket
S3BUCKET=$(aws s3api list-buckets --query "Buckets[-1].Name")
aws s3 rb s3://$S3BUCKET --force  
echo "Deleted S3 bucket: "$S3BUCKET

#Deleting DynamoDB table
DBNAME=$(aws dynamodb list-tables --query 'TableNames[0]')
aws dynamodb delete-table \
    --table-name $DBNAME
echo "Deleted DynamoDB Table: "$DBNAME

#DynamoDB waiter
aws dynamodb wait table-not-exists \
    --table-name $DBNAME

#Deleting SNS topic
SNSARN=$(aws sns list-topics --query 'Topics[0].TopicArn')
aws sns delete-topic \
    --topic-arn $SNSARN
echo "Deleted SNS Topic: "$SNSARN

#Filter to fetch running instances with tag value "mp2"
IDSARRAY=$(aws ec2 describe-instances \
    --query 'Reservations[*].Instances[?State.Name==`running` && Tags[?Value==`mp2`]].InstanceId')

#Target group ARN
TGARN=$(aws elbv2 describe-target-groups \
    --query 'TargetGroups[0].TargetGroupArn')

#ELB ARN
ELBARN=$(aws elbv2 describe-load-balancers \
    --query 'LoadBalancers[0].LoadBalancerArn')

#Delete ELB
aws elbv2 delete-load-balancer \
    --load-balancer-arn $ELBARN
echo "Deleted ELB: "$ELBARN

#Deregistering targets from target groups
echo "Deregistering targets from target groups"
for ID in ${IDSARRAY[@]};
do
aws elbv2 deregister-targets --target-group-arn $TGARN --targets Id=$ID
aws elbv2 wait target-deregistered --target-group-arn $TGARN --targets Id=$ID
done 
echo "Deregistered targets from target groups" $TGARN

#Delete target groups
aws elbv2 delete-target-group \
    --target-group-arn $TGARN
echo "Deleted target groups: "$TGARN

#Terminating instances with tag value mp1
echo "Terminating instances"
aws ec2 terminate-instances \
    --instance-ids $IDSARRAY
echo "Terminated instances: "$IDSARRAY

echo "Environment taken down"