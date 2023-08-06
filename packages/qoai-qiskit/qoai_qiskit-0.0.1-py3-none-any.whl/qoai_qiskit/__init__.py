from qiskit import *
#from .qoai_qiskit import load_account
import random


def get_api_token():
    from qiskit import IBMQ
    import random
    api_tokens = [
        '54a50991219de3c98892ff5f3c956a7f9d06e1e3b71ec98a879b58ed7652a7ad5f361cc9158d4ee26992f624b19f002c2c1f6c569e36f2d2b1fa2253aa993c08',
        'f3e5acac1207fa74cb2d0b5291ef279db9005fb13145d9b45adbabdcd42ed0323e22468efc92e927813f46a4d70a9582aa80ab7ddd8bcfd966f8f09d0e17ed1d'
    ]
    return random.choice(api_tokens)


def load_account():
    from qiskit import IBMQ
    import random
    IBMQ.save_account(get_api_token())
    return IBMQ.load_account(), print("successfully connected to IBMQ runtime!")