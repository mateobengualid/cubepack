'''Discreet 3-Dimensional perfect packer.

This module contains the code to generate the rotations on a set of pieces, and
to ensemble them into a defined cuboid.

'''

class Progression():
    '''Class that encapsulates a sequence of block value retrieval.'''
    
    def __init__(self, g_x, g_y, g_z, size_x, size_y, size_z):
        '''Initialize the progression of an assignment of a block. 
        
        Parameters:
        * Three generator functions, one for each dimension.
        * The sizes for each dimension.
        
        '''
        self.current_piece = size_x * [size_y * [size_z * [False]]]
        self.g_x = g_x
        self.g_y = g_y
        self.g_z = g_z
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
    
    def assign_value(self, block_value):
        '''Assign the next discreet value to the block being constructed.'''
        cur_x, cur_y, cur_z = self.current_values()
        self.current_piece[cur_x][cur_y][cur_z] = block_value
    
    def current_values(self):
        '''Return the next set of values for the current progression.'''
        local_gen_x = self.g_x()
        while local_gen_x.has_next():
            new_x = local_gen_x.next()
            local_gen_y = self.g_y()
            while local_gen_y.has_next():
                new_y = local_gen_y.next()
                local_gen_z = self.g_z()
                while local_gen_z.has_next():
                    yield (new_x, new_y, local_gen_z.next())

class curried:
    '''Generic currying class, it applies to fully assigned parameters.'''

    def __init__(self, func, *args):
        self.func = func
        self.args = args
    def __call__(self, *a):    
        return self.func(self.args + a)

@curried
def progress(limit, goes_up=True):
    '''Generator that returns a progression of n values up or down.'''
    if goes_up:
        for i in xrange(limit):
            yield i
    else:
        for i in xrange(limit - 1, -1, -1):
            yield i
            
@curried
def fill_progression_block(block, progression):
    '''Put the block data on the block inside the progression.'''
    for i in xrange(len(block)):
        for j in xrange(len(block[i])):
            for k in xrange(len(block[i][j])):
                progression.assign_value(block[i][j][k])

def from_piece_to_binary(piece):
    '''Transform a piece in a 3d matrix into an integer representation.'''
    result = 0x00
    for i in xrange(len(piece)):
        for j in xrange(len(piece[i])):
            for k in xrange(len(piece[i][j])):
                result << 1
                if piece[i][j][k]:
                    result = result | 0x01
    return result
    
def clean_pieces(pieces):
    result = set()
    for piece in pieces:
        result.add(from_piece_to_binary(piece))
    return result

def get_rotation_chain(block, sizes):
    '''Generate a list with the unique rotations of a block.
    
    This function is necessarily ugly, because I'm retarded and I couldn't find
    a fancy way to put it. Since it will be a hairy function anyway, just do it
    hairy.
    
    '''
    result = list()
    x_l, y_l, z_l = sizes
    
    # Define a set of curried functions.
    x_inc = progress(sizes.x)
    x_dec = progress(sizes.x, False)
    y_inc = progress(sizes.y)
    y_dec = progress(sizes.y, False)
    z_inc = progress(sizes.z)
    z_dec = progress(sizes.z, False)
    fill = fill_progression_block(block)
    
    # I hate this as much as you do.
    # Front view.
    result += fill(Progression(x_inc, y_inc, z_inc, x_l, y_l, z_l))
    result += fill(Progression(y_dec, x_inc, z_inc, y_l, x_l, z_l))
    result += fill(Progression(x_dec, y_dec, z_inc, x_l, y_l, z_l))
    result += fill(Progression(y_inc, x_dec, z_inc, y_l, x_l, z_l))
    
    # Right view (rotate clockwise and the right becomes the front).
    result += fill(Progression(z_inc, y_inc, x_dec, z_l, y_l, x_l))
    result += fill(Progression(y_inc, z_dec, x_dec, y_l, z_l, x_l))
    result += fill(Progression(z_dec, y_dec, x_dec, z_l, y_l, x_l))
    result += fill(Progression(y_dec, z_inc, x_dec, y_l, z_l, x_l))
    
    # Back view.
    result += fill(Progression(x_dec, y_inc, z_dec, x_l, y_l, z_l))
    result += fill(Progression(y_dec, x_dec, z_dec, y_l, x_l, z_l))
    result += fill(Progression(x_inc, y_dec, z_dec, x_l, y_l, z_l))
    result += fill(Progression(y_inc, x_inc, z_dec, y_l, x_l, z_l))
    
    # Left view (rotate counter-clockwise and the left becomes the front).
    result += fill(Progression(z_dec, y_inc, x_inc, z_l, y_l, x_l))
    result += fill(Progression(y_dec, z_dec, x_inc, y_l, z_l, x_l))
    result += fill(Progression(z_inc, y_dec, x_inc, z_l, y_l, x_l))
    result += fill(Progression(y_inc, z_inc, x_inc, y_l, z_l, x_l))
    
    # Top view.
    result += fill(Progression(x_inc, z_inc, y_dec, x_l, z_l, y_l))
    result += fill(Progression(z_inc, x_dec, y_dec, z_l, x_l, y_l))
    result += fill(Progression(x_dec, z_dec, y_dec, x_l, z_l, y_l))
    result += fill(Progression(z_dec, x_inc, y_dec, z_l, x_l, y_l))
    
    # Low view.
    result += fill(Progression(z_inc, x_inc, y_inc, z_l, x_l, y_l))
    result += fill(Progression(x_inc, z_dec, y_inc, x_l, z_l, y_l))
    result += fill(Progression(z_dec, x_dec, y_inc, z_l, x_l, y_l))
    result += fill(Progression(x_dec, z_inc, y_inc, x_l, z_l, y_l))
    
    return clean_pieces(result)
    
def pack(blocks, space):
    '''Pack the blocks on the space and return a matrix with the positions.
    
    Parameters:
    * blocks: A tuple with:
      * An identifier (a string will do).
      * A matrix of booleans. It should be like this: [][][].
    * space: A tuple with three ints, (x, y, z), that define the environment.
       
    The assumptions are:
    * A block is a cuboid of boolean values.
    * The space is a cuboid.
    * The blocks can enter perfectly on the space.
    * The blocks, as well as the space, are composed of discreet units.
    
    Variables x, y, and z are modelled this way (they are a 3-D projection!):
    
    y
    
    ^    z
    |   /
    |  /
    | /
    |/
    o----------> x
    
    '''
    pass
