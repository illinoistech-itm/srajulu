#!/bin/bash

# Make extensive use of: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/index.html
# Adding URLs of the syntax above each command

# Example Script to dynamically terminate all running EC2 instances
IDSARRAY=$(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Code==`16`].InstanceId' --output text)

aws ec2 terminate-instances --instance-ids $IDSARRAY

#remove target groupss

# Need code to dynamically terminate RDS instances

# Need code to dynamically detach instances from targets and then terminate target groups 

# Need code to dynamically terminate ELBs

# Need code to detach and delete additional EC2 EBS volumes

