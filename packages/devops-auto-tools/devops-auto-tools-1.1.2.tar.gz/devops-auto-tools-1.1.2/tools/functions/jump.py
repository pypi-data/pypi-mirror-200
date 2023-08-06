from subprocess import call
import os

from tools.functions import utils
from tools.dtos.jump_var import var

def get_profiles():
  f = open(utils.get_config_path("~/.ssh/config"), 'r')
  lines = f.readlines()
  f.close()
  profiles = []
  for line in lines:
    if "Host " in line and "*" not in line:
      profiles.append(line.split("Host ")[1].split("\n")[0])
  return profiles

def get_cidr():
  return [
    "All traffics",
    "Specific cidrs"
  ]

def set_profile():
  var.profile = utils.render_choices(get_profiles())
  if var.profile != False:
    return True
  return False

def set_cidr():
  var.cidr = utils.render_choices(get_cidr())
  if var.cidr != False:
    if "All traffics" in var.cidr:
      var.cidr = "0.0.0.0/0"
    else:
      try:
        var.cidr = input("Enter cidr: ")
      except:
        pass
    return True
  else:
    return False
  
def set_proxy():
  try:
    call([ 
      'sshuttle',
      '-r', 
      var.profile,
      var.cidr, 
      '-vv' 
    ])
    return False
  except:
    return False