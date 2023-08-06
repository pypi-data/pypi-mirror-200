import pytz
import re
import random
import os
from datetime import *
import string
from typing import *
from bs4 import *
import aiohttp
import requests
import logging
from pyrogram.errors import *
from typing import Union

class temp(object):
    BANNED_USERS = []
    BANNED_CHATS = []
    ME = None
    CURRENT = 0
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None
    SETTINGS = {}
