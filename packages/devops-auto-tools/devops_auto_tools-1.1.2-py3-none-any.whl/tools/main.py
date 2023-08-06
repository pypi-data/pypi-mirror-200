from tools.functions import aws, utils, ssh, jump
import signal

def eksm():
  
  stacks = [
    aws.set_profile,
    aws.set_region,
    aws.set_eks_name
  ]
  if utils.ex_stacks(stacks) :
    aws.set_cluster()  

def sshm():
  stacks = [
    ssh.set_profile,
    ssh.set_ssh
  ]
  if utils.ex_stacks(stacks) :
    ssh.set_profile() 

def jumpm():
  stacks = [
    jump.set_profile,
    jump.set_cidr,
    jump.set_proxy
  ]
  if utils.ex_stacks(stacks) :
    jump.set_cidr()

signal.signal(signal.SIGINT, utils.exist_handler)
