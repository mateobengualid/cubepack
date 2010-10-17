'''Discreet 3-Dimensional perfect packer.

This module contains the code to generate the rotations on a set of pieces, and
to ensemble them into a defined cuboid.

'''

class VarDirection:
    def __init__(self, name, top, goes_up=True):
        self.name = name
        self.goes_up = goes_up
        self.top = top
        
    def generator(self):
        if self.goes_up:
            for i in xrange(self.top):
                yield i
        else:
            for i in reversed(xrange(self.top)):
                yield i

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
          z
    ^    ╮
    |   /
    |  /
    | /
    |/
    ╰----------> x
    '''
    pass
        
x_inc = lambda x : VarDirection("x", x)
y_inc = lambda x : VarDirection("y", x)
z_inc = lambda x : VarDirection("z", x)
x_dec = lambda x : VarDirection("x", x, goes_up=False)
y_dec = lambda x : VarDirection("y", x, goes_up=False)
z_dec = lambda x : VarDirection("z", x, goes_up=False)

def get_rotation_chain(block, sizes):
    '''Generate a list with the unique rotations of a block.
    
    This function is necessarily ugly, because I'm retarded and I couldn't find
    a fancy way to put it. Since it will be a hairy function anyway, just do it
    ugly.
    
    '''
    result = list()
    x_l = sizes.x
    y_l = sizes.y
    z_l = sizes.z
    
    result += rotate_for_face(block, sizes, x_inc(x_l), y_inc(y_l), z_inc(z_l))
    result += rotate_for_face(block, sizes, z_inc(z_l), y_inc(y_l), x_dec(x_l))
    result += rotate_for_face(block, sizes, x_dec(x_l), y_inc(y_l), z_dec(z_l))
    result += rotate_for_face(block, sizes, z_dec(z_l), y_inc(y_l), x_inc(x_l))
    result += rotate_for_face(block, sizes, x_inc(x_l), z_inc(z_l), y_dec(y_l))
    result += rotate_for_face(block, sizes, z_inc(z_l), x_inc(x_l), y_inc(y_l))
    
    clean_repeated_pieces(result)
    return result
    
def rotate_for_face(block, sizes, directions):
    '''Rotate the current block over the front face (x and y).'''
    (size_x, size_y, size_z) = sizes
    (dir_x, dir_y, dir_z) = directions
    new_piece = size_x * [size_y * [size_z * [False]]]

    i_gen = dir_x.generator()
    for i in xrange(dir_x.top):
        i_new = i_gen.next()
        j_gen = dir_y.generator()
        for j in xrange(dir_y.top):
            j_new = j_gen.next()
            k_gen = dir_z.generator()
            for k in xrange(dir_z.top):
                k_new = k_gen.next()
                new_piece[i][j][k] = block[i][j][k]
    result.append(newPiece)
    
def two_pieces_are_equal(piece_a, piece_b):
    '''Compare two non-empty pieces.'''
    
    x = len(piece_a)
    y = len(piece_a[0])
    z = len(piece_a[0][0])
    if x != len(piece_b) or y != len(piece_b[0]) or z != len(piece_b[0][0]):
        return false
    else:
        for i in xrange(x):
            for j in xrange(y):
                for k in xrange(z):
                    if piece_a[i][j][k] != piece_b[i][j][k]:
                        return false
        return true
    
def next_rotated_block(block, rotateChain):
    '''Generate a non-repeating sequence of rotated blocks.'''
    pass
