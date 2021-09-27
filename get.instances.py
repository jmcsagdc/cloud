import os

# INPUT

print "Requires Amazon's aws ec2 CLI tools to function."

# TODO: Make every occurence of keyname here a variable instead of a hardcode

# In the popen, change keyname to the name of your pem file (omit the .pem)
myFile=os.popen('aws ec2 describe-instances --query "Reservations[*].Instances[*].[KeyName, PublicIpAddress, PrivateIpAddress]" --output=text | grep keyname').read()

# Clean up data

myData=myFile.strip().split()

myYaml=""

# Change the pem to yours. The script looks for this in your instances query, so look for the other place as well

myLeader="""# set path to ssh private key so we can ssh into each node for provisioning
ssh_key_path: .ssh/amazon/keyname.pem

# kubernetes_version (optional...I leave blank)
kubernetes_version:

# list of nodes including internal addresses, defaults to all roles

nodes:\n"""

myUser = "ubuntu" # TODO: Make user flexible. Currently hardcoded for EC2 ubuntu user.

myRoles = "[etcd, controlplane, worker]" # TODO: Make roles flexible. Currently a string.

myYaml += myLeader

for i in range (0, len(myData)):
    # change keyname to the name of your .pem (omit the .pem)
    if "keyname" in myData[i]:
        print "\n****   " + str(i) + "   ***"
        # DEBUG: print myData[i] + "\t\t", "External:\t" + myData[i+1], "\tInternal:\t" + myData[i+2]
        myYaml += "  - address: " + myData[i+1] + "\n"
        myYaml += "    internal_address: " + myData[i+2] + "\n"
        myYaml += "    user: " + myUser + "\n"
        myYaml += "    role: " + myRoles + "\n"

        # Build ssh command
        sshLine="ssh ubuntu@" + myData[i+1] + " -oStrictHostKeyChecking=no -i ~/.ssh/amazon/keyname.pem "  # <--- change to your keyname
        sshLine += "'curl https://releases.rancher.com/install-docker/20.10.sh | sh && sudo usermod -aG docker ubuntu'"
        print "\n"
        print sshLine

    else: pass # Skip anything without my keyname in data

print "\n\n"
print myYaml
