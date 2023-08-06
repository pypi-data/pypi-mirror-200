import dir_ops as do
import os

_Dir = do.Dir( os.path.abspath( __file__ ) ).ascend()   #Dir that contains the package 

from .AWS_Creds import AWS_Creds
from .Client import Client

client = Client()

Cred = None
cred_dict = {}

if client.cfg['role'] != None:
    Cred = client.Creds[ client.cfg['role'] ]
    cred_dict = Cred.dict