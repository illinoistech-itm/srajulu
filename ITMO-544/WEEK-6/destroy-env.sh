#!/bin/bash

aws ec2 terminate-instances \
        --instance-ids $IDS $(aws ec2 describe-instances --query 'Reservations[*].Instances[?State.Name==`running`].InstanceId')