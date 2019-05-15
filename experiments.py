#!/usr/bin/env python

import re

class Person():
    def __init__(self, name):
        self.name = name


hunter = Person('Elmer Fudd')


class Car():
    def exclaim(self):
        print("I'm a car!")


class Yugo(Car):
    def exclaim(self):
        print("I'm a Yugo! Much like a car, but more Yugo-ish.")


give_me_a_car = Car()

give_me_a_yugo = Yugo()

command_tree = ('run', [('show', [('date', [()'\n', ])]), ('poweroff', [])])

(keyword, description, completions)
(token, description, completions)
('add', 'Add an object to a service', [])

pattern = re.compile(ur'', re.UNICODE)

pattern.search('')
