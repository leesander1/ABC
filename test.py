''' Tests '''
from block import Block
import block
from block.block import genesis_block
# from client import core
from client.core import initialize, save_conf

conf = initialize()
print(conf["height"])
save_conf(conf)
# test block class
b = genesis_block()
b.print_info()
b.print_header()
