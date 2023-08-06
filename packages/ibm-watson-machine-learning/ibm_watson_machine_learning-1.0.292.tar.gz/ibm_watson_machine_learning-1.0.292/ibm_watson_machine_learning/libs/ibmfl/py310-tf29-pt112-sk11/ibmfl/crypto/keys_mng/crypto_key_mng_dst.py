#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2022- 2023.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------
from ibmfl.crypto.keys_mng.crypto_key_mng_int import KeyManager
from ibmfl.crypto.crypto_exceptions import KeyManagerException

class DistributionKeyManager(KeyManager):

    def __init__(self, config):
        """ Initialize Key from local key file"""
        if config and 'distribution' not in config:
            raise KeyManagerException('keys distribution configuration is not provided')
        self.keys = config

    def initialize_keys(self, **kwargs):
        """ Initialize the keys directly from the config file"""
        return self.keys
