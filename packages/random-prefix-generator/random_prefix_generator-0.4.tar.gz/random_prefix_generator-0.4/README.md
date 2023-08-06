# Random IP/Prefix Generator

`randomprefixgenerator` is a simple Python module for generating random IPv4 and IPv6 addresses and subnets.

## Features
* Generate random IPv4 or IPv6 addresses.
* Generate random IPv4 or IPv6 subnets with a specified prefix length.
* Control the range of prefix lengths for generated subnets.


## Installation

You can install myIp using pip:
```
pip install randomprefixgenerator
```


## Usage
```
from randomprefixgenerator import RandomPrefixGenerator

# Create a new myIp object for generating IPv4 addresses
ipv4_gen = RandomPrefixGenerator(4, mode='ip')

# Generate a random IPv4 address
ipv4_addr = next(ipv4_gen)

# Create a new myIp object for generating IPv6 subnets with prefix lengths between 64 and 120
ipv6_gen = RandomPrefixGenerator(6, mode='prefix', min_length=64, max_length=120)

# Generate a random IPv6 subnet
ipv6_subnet = next(ipv6_gen)
```

## Dependancies
* Python 3.x
* `ipaddress` module
