#!/usr/bin/env python

from collections import namedtuple
import paramiko
import re
import socket
import sys
import time


# Node = namedtuple('Node', 'keyword description completions')
Node = namedtuple('Node', 'keyword completions')


def new_build_tree(node, recorded_path):
    session.send("\x03")
    time.sleep(.2)
    session.recv(65535)

    path = recorded_path
    path.append(node.keyword)
    cmd = ' '.join(path) + ' ?'
    session.send(cmd)
    time.sleep(.2)
    output = session.recv(65535)
    lines = output.decode('utf8').split('\r\n')

    for line in lines[1:]:
        if line.startswith('vyos') or line.startswith('Possible'):
            continue
        m = re.search(r'^[<|>|\w|\s|\(|\)]+', line)
        if m:
            words = m.group(0).split()

            if len(words) > 1:
                keyword = words[0]
                # description = ' '.join(words[1:])

                # Handle argument and command complete
                m = re.match(r'<(\w+)>', keyword)
                if m:
                    argument = m.groups()[0]
                    if argument == 'Enter':
                        return
                    else:
                        keyword = argument.upper()

                # child = Node(keyword, description, [])
                child = Node(keyword, [])
                node.completions.append(child)

    for child in node.completions:
        new_build_tree(child, recorded_path)


if __name__ == "__main__":
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect('10.211.55.7', 22, 'vyos', 'vyos')
    except paramiko.SSHException or paramiko.socket.error or socket.timeout:
        print("Can't connect!\n")
        sys.exit(1)

    session = client.invoke_shell(width=270, height=79)

    time.sleep(.5)

    # Read banner
    banner = session.recv(65535)

    # new_build_tree(Node('', '', []), [''])
    new_build_tree(Node('', []), [''])
    sys.exit(0)
