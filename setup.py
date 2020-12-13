#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distribute_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='BufferedQueue',
    version='1.0',
    description='Buffer Messages in Redis Queues Based on Group Id Of Payload And Send Buffered Data To Kafka On Threshold',
    author='Sahil Batla',
    author_email='sahilbathla1@gmail.com',
    install_requires = [
        "redis==2.10.3",
        "simplejson==3.10.0",
        "pyyaml==5.1",
        "kafka==1.3.1"
    ]
)