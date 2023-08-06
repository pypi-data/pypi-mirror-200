from simple_term_menu import TerminalMenu
import platform
from os.path import expanduser

def render_choices(options:list):
  options.append("Back")
  terminal_menu = TerminalMenu(options)
  menu_entry_index = terminal_menu.show()
  result = options[menu_entry_index]
  if "Back" in result :
    return False
  return result

def get_executable():
  if platform.system()=='Darwin':
    executable = "/bin/zsh"
  else:
    executable = "/bin/bash"
  return executable

def get_config_path(path):
  path = path.split("~")[1]
  return expanduser("~")+path

def exist_handler(signum, frame):
  exit(1)
  
def ex_stacks(stacks: list): 
  i = 0
  while i < len(stacks) and i!= -1:
    r = stacks[i]()
    if r == True :
      i += 1
    elif r == False :
      i-=1
      
  if i != -1:
    return True
  return False