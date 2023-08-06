

from random import getrandbits, randint
import ipaddress




class RandomPrefixGenerator:

    def __init__(self, version: int, mode='prefix', min_length=16, max_length=24 ) -> None:

        if version == 4 or version == 6:
            self._version = version
        else:
            return None

        self._mode = mode        
        if mode == 'prefix':
            self._min = min_length
            self._max = max_length

    def __iter__(self):
        return self
    
    def __next__(self):
        if self._version == 4:
            bits = getrandbits(32)
            addr = ipaddress.IPv4Address(bits)
            if self._mode == 'ip':
                return str(addr)
            
            mask_bits = randint(self._min, self._max)
            subnet = ipaddress.IPv4Network( (addr,mask_bits), False )
            return str(subnet)

        elif self._version == 6:
            bits = getrandbits(128)
            addr = ipaddress.IPv6Address(bits)
            if self._mode == 'ip':
                return str(addr)
            
            mask_bits = randint(self._min, self._max)
            subnet = ipaddress.IPv6Network( (addr,mask_bits), False )
            return str(subnet)
