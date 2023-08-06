# -*- coding: utf-8 -*-
import os
import sys
from navconfig import config, BASE_DIR

'''
TROC-Navigator Local Settings
'''

# Partner Key
PARTNER_KEY = config.get('PARTNER_KEY')
PARTNER_SESSION_TIMEOUT = 200000  # in seconds
CYPHER_TYPE = 'RNC'
