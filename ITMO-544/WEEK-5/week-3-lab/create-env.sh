aws ec2 run-instances \
 --image-id ami-00399ec92321828f5 \
 --count 1 \
 --subnet-id subnet-0cb78376 \
 --instance-type t2.micro \
 --key-name linux-itmo-vbox-script \
 --security-group-ids sg-071131c8e585d8604 \
 --user-data file://install-env.sh