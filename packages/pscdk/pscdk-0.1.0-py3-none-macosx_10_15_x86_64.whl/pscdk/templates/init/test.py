import os
import hashlib
import platform

from ipyeos import eos
from ipyeos import chaintester
from ipyeos.chaintester import ChainTester
from ipyeos import log

chaintester.chain_config['contracts_console'] = True
eos.set_log_level("default", 3)

logger = log.get_logger(__name__)

dir_name = os.path.dirname(os.path.abspath(__file__))

def update_auth(chain, account):
    a = {
        "account": account,
        "permission": "active",
        "parent": "owner",
        "auth": {
            "threshold": 1,
            "keys": [
                {
                    "key": 'EOS6AjF6hvF7GSuSd4sCgfPKq5uWaXvGM2aQtEUCwmEHygQaqxBSV',
                    "weight": 1
                }
            ],
            "accounts": [{"permission":{"actor":account,"permission": 'eosio.code'}, "weight":1}],
            "waits": []
        }
    }
    chain.push_action('eosio', 'updateauth', a, {account:'active'})

def init_test():
    t = ChainTester(True)
    update_auth(t, 'hello')
    wasm_file = os.path.join(dir_name, '{{name}}.wasm')
    with open(wasm_file, 'rb') as f:
        code = f.read()

    abi_file = os.path.join(dir_name, '{{name}}.abi')
    with open(abi_file, 'r') as f:
        abi = f.read()

    t.deploy_contract('hello', code, abi)
    t.produce_block()
    eos.set_log_level("default", 1)

    # eos.enable_debug(True)
    # native_lib = os.path.join(dir_name, 'libhello.so')
    # native_lib = os.path.abspath(native_lib)
    # t.chain.set_native_contract('hello', native_lib)

    return t

# print('pid:', os.getpid())
# input("Press Enter to continue...")

def test_hello():
    t = init_test()
    args = {'name': 'alice'}
    ret = t.push_action('hello', 'sayhello', args, {'hello': 'active'})
    t.produce_block()
    logger.info("++++++++++%s\n", ret['elapsed'])
