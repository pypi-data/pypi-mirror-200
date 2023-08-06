__import__('com.softalks.debug')

import os
import subprocess
from subprocess import Popen, PIPE

columns = 120
wrotten = 0
delimiter = ' '
encodedDelimiter = '_!_'
encoding = 'utf-8'
pipe = None

def getString(*commands, singleton=True):

    if len(commands) == 1:
        command = commands[0] 
        if  isinstance(command, str) and '|' in command:
            commands = [x.strip() for x in command.split('|')]
            return getString(*commands)
    
    def encode(command):
        return command.group(1).replace(' ', encodedDelimiter)

    def encoded(command):
        import re
        command = re.sub('"([^"]*)"', encode, command)
        return command

    def decoded(command):
        command = command.split()
        tokens = []
        for token in command:
            tokens.append(token.replace(encodedDelimiter, ' '))
        return tokens

    def check_output(command):
        command = decoded(command)
        output = subprocess.check_output(command, stdin=pipe)
        getLines = output.splitlines()
        result = []
        for line in getLines:
            result.append(line.decode(encoding))
        if len(result) == 1 and singleton:
            return result[0]
        return result

    chain = []
    for command in commands:
        chain.append(encoded(command))
    length = len(chain)
    if (length == 1):
        return check_output(chain[0])
    for i in range(length):
        command = chain[i]
        if (i == length - 1):
            return check_output(command)
        else:
            command = decoded(command)
            global pipe
            pipe = Popen(command, stdin=pipe, stdout=PIPE).stdout
            
def getLines(*commands):
    return getString(*commands, singleton=False)
    
def moreCommandInPlace():
    from os import getppid
    ppid = getppid()
    siblings = getLines(f'ps -o ppid= -o args -A | awk "$1 == {ppid}{{print $2}}"')
    for sibling in siblings:
        if (sibling == 'more' or sibling.startswith('more ')):
            return True
    return False

def getColumns():
    return int(getString('tput cols'))
    
tty = getString(f'ps -p {os.getpid()} -o tty=')
if tty.startswith('tty'):
    columns = getColumns()
    static = True
elif tty == '?':
    static = True
else:
    static = False
    
def writeWrapped(content, **parameters):
    if parameters.get('end'):
        raise Exception('Illegal argument: "end"')
    global wrotten
    if not isinstance(content, str):
        word = str(content)
    characters = len(word)
    wrotten = wrotten + characters + 1
    if static:
        global columns
    else:
        columns = getColumns()
    if wrotten > columns:
        word = '\n' + word
        wrotten = characters
    else:
        word = ' ' + word
    print(word, end='', **parameters)
    
def write(content, **parameters):
    if isinstance(content, int):
        return writeWrapped(content, **parameters)
    else:
        return print(content, **parameters)