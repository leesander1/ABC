''' Main File '''
# from block import Block
import _thread, time
from src.client import CLI
from src.network.network import start_server, seed_peers

_thread.start_new_thread(start_server, ())
time.sleep(1)
CLI().cmdloop()
