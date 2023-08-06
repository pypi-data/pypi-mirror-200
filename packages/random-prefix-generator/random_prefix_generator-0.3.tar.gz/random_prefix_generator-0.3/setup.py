from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='random_prefix_generator',
    version='0.3',
    author='Colin MacGiollaEain',
    description='A package for generating random IPv4 and IPv6 addresses and subnets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/colinmacgiolla/random_ip_generator",
    author_email='colin@flat-planet.net',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['ipaddress'],
    python_requires='>=3.6',
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 4 - Beta',

        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
)
