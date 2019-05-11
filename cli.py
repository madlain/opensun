#!/usr/bin/env python

from collections import namedtuple
import paramiko
import re
import socket
import sys
import time


# Node = namedtuple('Node', 'keyword description completions')
Node = namedtuple('Node', 'keyword completions')


def new_build_tree(node, path):
    session.send("\x03")
    time.sleep(.2)
    session.recv(65535)

    local_path = path.copy()
    local_path.append(node.keyword)
    cmd = ' '.join(local_path) + ' ?'
    session.send(cmd)
    time.sleep(.2)
    output = session.recv(65535)
    lines = output.decode('utf8').split('\r\n')

    for line in lines[1:]:
        if line.startswith('vyos') or line.startswith('Possible'):
            continue
        m = re.search(r'^[<|>|\w|\s|\(|\)|-]+', line)
        if m:
            words = m.group(0).split()

            if len(words) > 1 or (len(words) == 1 and re.match(r'^[<|\w]', words[0])):
                keyword = words[0]
                if len(keyword) > 13:
                    print('Fix multiline completion for', len(keyword), '-char', keyword)
                    sys.exit(1)
                # description = ' '.join(words[1:])

                # Handle argument and command complete
                m = re.match(r'<(\w+)>', keyword)
                if m:
                    keyword = m.groups()[0].upper()

                # child = Node(keyword, description, [])
                child = Node(keyword, [])
                node.completions.append(child)

    # 'ENTER' as a possible completion normally comes first
    # ['ENTER', 'foo', 'bar'] or ['ENTER']
    if ('ENTER', []) in node.completions:
        node.completions.pop(0)
        list_len = len(node.completions)
        if list_len == 0:
            print(' '.join(local_path[1:]))
            return

    for child in node.completions:
        new_build_tree(child, local_path)


if __name__ == "__main__":
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect('172.23.62.73', 22, 'vyos', 'vyos')
    except paramiko.SSHException or paramiko.socket.error or socket.timeout:
        print("Can't connect!\n")
        sys.exit(1)

    session = client.invoke_shell(width=270, height=79)

    time.sleep(.5)

    # Read banner
    banner = session.recv(65535)

    # new_build_tree(Node('', '', []), [''])
    new_build_tree(Node('', []), [])
    sys.exit(0)
