
def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))

def cromulon():
    ascii_img = '''
                    ___          
                . -^   `--,      
               /# =========`-_   
              /# (--====___====\ 
             /#   .- --.  . --.| 
            /##   |  * ) (   * ),
            |##   \    /\ \   / |
            |###   ---   \ ---  |     _______________________________
            |####      ___)    #|   /                                |
            |######           ##|  /  I like what you got. Good Job. |
             \##### ---------- /  /                                  |
              \####           (  <___________________________________|
               `\###          |  
                 \###         |  
                  \##        |   
                   \###.    .)   
                    `======/  
                    '''
    return ascii_img

