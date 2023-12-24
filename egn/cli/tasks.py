#!/home/saeranv/miniconda3/envs/thermal/bin/python

import os
import sys
from invoke import task

@task
def test(ctx):
    print('hello world')
