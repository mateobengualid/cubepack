'''Discreet 3-Dimensional perfect packer.

This module contains the code to generate the rotations on a set of pieces, and
to ensemble them into a defined cuboid.

'''

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

class Progression():
    '''Class that encapsulates a sequence of block value retrieval.'''
    
    def __init__(self, x, y, z, size_x, size_y, size_z):
        '''Initialize the progression of an assignment of a block. 
        
        Parameters:
        * A matrix of booleans. It should be like this: [][][].
        * three generator functions, and the sizes
        for each dimension.
        
        '''
        self.current_piece = block
        self.x = x
        self.y = y
        self.z = z
        self.x_goes_up = x_goes_up
        self.y_goes_up = y_goes_up
        self.z_goes_up = z_goes_up
    
    def assign_value(self, block_value):
        '''Assign the next discreet value to the block being constructed.'''
        cur_x, cur_y, cur_z = self.current_values()
        self.current_piece[cur_x][cur_y][cur_z] = block_value
    
    def current_values(self):
        '''Return the next set of values for the current progression.'''
        g_x = x()
        while g_x.has_next():
            new_x = g_x.next()
            g_y = y()
            while g_y.has_next():
                new_y = g_x.next()
                g_z = z()
                while g_z.has_next():
                    yield (new_x, new_y, g_z.next())

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
    
    result += rotate_for_face(block, sizes, X_INC(x_l), Y_INC(y_l), Z_INC(z_l))
    result += rotate_for_face(block, sizes, Z_INC(z_l), Y_INC(y_l), X_DEC(x_l))
    result += rotate_for_face(block, sizes, X_DEC(x_l), Y_INC(y_l), Z_DEC(z_l))
    result += rotate_for_face(block, sizes, Z_DEC(z_l), Y_INC(y_l), X_INC(x_l))
    result += rotate_for_face(block, sizes, X_INC(x_l), Z_INC(z_l), Y_DEC(y_l))
    result += rotate_for_face(block, sizes, Z_INC(z_l), X_INC(x_l), Y_INC(y_l))
    
    clean_repeated_pieces(result)
    return result
    
def rotate_a(block, sizes):
    '''Rotate the block 90° on the Y axis and 90° on the Z axis.'''
    (size_x, size_y, size_z) = sizes
    (dir_x, dir_y, dir_z) = directions
    new_piece = size_x * [size_y * [size_z * [False]]]

    i_gen = dir_x.generator()
    while(i_gen.has_next()):
        i_new = i_gen.next()
        j_gen = dir_y.generator()
        while(j_gen.has_next()):
            j_new = j_gen.next()
            k_gen = dir_z.generator()
            while(k_gen.has_next()):
                k_new = k_gen.next()
                new_piece[i][j][k] = block[i][j][k]
    result.append(newPiece)
    
def rotate_b(block, sizes):
    '''Rotate the block 270° on the Y axis and 180° on the Z axis.'''
    pass
    
def rotate_through_axis(block, )

def clean_repeated_pieces(pieces):
    pass
    
def from_piece_to_binary(piece):
    '''Transform a piece in a 3d matrix into an integer representation.'''
    
    
def two_pieces_are_equal(piece_a, piece_b):
    '''Compare two non-empty pieces.'''
    
    x = len(piece_a)
    y = len(piece_a[0])
    z = len(piece_a[0][0])
    if x != len(piece_b) or y != len(piece_b[0]) or z != len(piece_b[0][0]):
        return False
    else:
        for i in xrange(x):
            for j in xrange(y):
                for k in xrange(z):
                    if piece_a[i][j][k] != piece_b[i][j][k]:
                        return False
        return True
    
def next_rotated_block(block, rotateChain):
    '''Generate a non-repeating sequence of rotated blocks.'''
    pass
