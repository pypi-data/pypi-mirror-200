from setuptools import setup

with open("read_me.txt","r") as fh:
    ld=fh.read()

classifiers=[
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
    
]

setup(name="country_call",
version="1.0.0",
description="Introducing a powerful and easy-to-use Python library for country detection from ambiguous text, designed for developers and data scientists alike.",
author="Md Shamim Hasan, Kazi Arman Rahat, Mukitul Islam, Anik Roy",
long_description=ld,

author_email="shihab18015@gmail.com",
install_requires=['re'],
keywords=['country','origin','nlp'],
classifiers=classifiers
)
