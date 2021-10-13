# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 18:20:50 2021

@author: Wayky
"""

import yaml

yaml_file = open(r"C:\Users\Wayky\Documents\GitHub\JOptimizer\tests\yaml_examples\example.alg", 'r')
yaml_content = yaml.load(yaml_file)

print(yaml_content)

with open(r"C:\Users\Wayky\Documents\GitHub\JOptimizer\tests\yaml_examples\example_out.alg", 'w') as file:
    documents = yaml.dump(yaml_content, file)