''' Tests '''
# from client import core
from client.core import initialize, save_conf
from core.blocks import genesis_block

conf = initialize()
print(conf["height"])
save_conf(conf)
# test block class
b = genesis_block()
b.print_info()
b.print_header()
