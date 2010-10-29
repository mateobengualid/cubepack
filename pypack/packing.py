'''Discreet 3-Dimensional perfect packer.

This module contains the code to generate the rotations on a set of pieces, and
to ensemble them into a defined cuboid.

'''

import itertools

class Progression():
    '''Class that encapsulates a sequence of block value retrieval.'''
    
    def __init__(self, g_x, g_y, g_z, sizes):
        '''Initialize the progression of an assignment of a block. 
        
        Parameters:
        * Three generator functions, one for each dimension.
        * A set with the sizes for each dimension.
        
        '''
        size_x, size_y, size_z = sizes
        self.current_piece = size_x * [size_y * [size_z * [False]]]
        self.g_x = g_x
        self.g_y = g_y
        self.g_z = g_z
    
    def assign_value(self, block_value):
        '''Assign the next discreet value to the block being constructed.'''
        cur_x, cur_y, cur_z = self.current_values()
        self.current_piece[cur_x][cur_y][cur_z] = block_value
    
    def current_values(self):
        '''Return the next set of values for the current progression.'''
        for new_x in self.g_x():
            for new_y in self.g_y():
                for new_z in self.g_z():
                    yield (new_x, new_y, new_z)

class Curried:
    '''Generic currying class, it applies to fully assigned parameters.'''

    def __init__(self, func, *args):
        self.func = func
        self.args = args
        self.can_call = True

    def __call__(self, *a):
        args = self.args + a

        # Check that all parameters have been submitted.
        if not self.can_call or len(args) < self.func.func_code.co_argcount:
            return Curried(self.func, *args)
        else:
            return self.func(*args)

@Curried
def progress(limit, goes_up):
    '''Generator that returns a progression of n values up or down.'''
    if goes_up:
        for i in xrange(limit):
            yield i
    else:
        for i in xrange(limit - 1, -1, -1):
            yield i
            
@Curried
def fill_progression_block(block, progression):
    '''Put the block data on the block inside the progression.'''
    for i in xrange(len(block)):
        for j in xrange(len(block[i])):
            for k in xrange(len(block[i][j])):
                progression.assign_value(block[i][j][k])

def from_piece_to_binary(piece, space):
    '''Transform a piece in a 3d matrix into an integer representation.'''
    # Print them in inverse order, it's easier that way.
    rev_result = 0x00
    for i in xrange(len(piece)):
        for j in xrange(len(piece[i])):
            for k in xrange(len(piece[i][j])):
                rev_result = rev_result << 1
                if piece[i][j][k]:
                    rev_result |=  0x01
            rev_result << space[2] - 1 - k
        rev_result << (space[1] - 1 - j) * space[2]
    
    # Turn everything around.
    result = 0
    while not rev_result == 0:
        result = result << 1
        result |= rev_result & 0x01
        rev_result = rev_result >> 1
    return result
    
def clean_pieces(pieces):
    '''Remove repeated pieces and transform them into binary representation.'''
    result = set()
    for piece in pieces:
        result.add(from_piece_to_binary(piece))
    return list(result)

def get_rotation_chain(block, sizes):
    '''Generate a list with the unique rotations of a block.
    
    This function is necessarily ugly, because I'm a noob and I couldn't find
    a fancy way to put it. Since it will be a hairy function anyway, just do it
    hairy.
    
    '''
    result = list()
    x_l, y_l, z_l = sizes
    
    # Define a set of curried functions.
    x_inc = progress(x_l, True)
    x_dec = progress(x_l, False)
    y_inc = progress(y_l, True)
    y_dec = progress(y_l, False)
    z_inc = progress(z_l, True)
    z_dec = progress(z_l, False)
    fill = fill_progression_block(block)
    
    # I hate this as much as you do.
    # Front view.
    result += fill(Progression(x_inc, y_inc, z_inc, (x_l, y_l, z_l)))
    result += fill(Progression(y_dec, x_inc, z_inc, (y_l, x_l, z_l)))
    result += fill(Progression(x_dec, y_dec, z_inc, (x_l, y_l, z_l)))
    result += fill(Progression(y_inc, x_dec, z_inc, (y_l, x_l, z_l)))
    
    # Right view (rotate clockwise and the right becomes the front).
    result += fill(Progression(z_inc, y_inc, x_dec, (z_l, y_l, x_l)))
    result += fill(Progression(y_inc, z_dec, x_dec, (y_l, z_l, x_l)))
    result += fill(Progression(z_dec, y_dec, x_dec, (z_l, y_l, x_l)))
    result += fill(Progression(y_dec, z_inc, x_dec, (y_l, z_l, x_l)))
    
    # Back view.
    result += fill(Progression(x_dec, y_inc, z_dec, (x_l, y_l, z_l)))
    result += fill(Progression(y_dec, x_dec, z_dec, (y_l, x_l, z_l)))
    result += fill(Progression(x_inc, y_dec, z_dec, (x_l, y_l, z_l)))
    result += fill(Progression(y_inc, x_inc, z_dec, (y_l, x_l, z_l)))
    
    # Left view (rotate counter-clockwise and the left becomes the front).
    result += fill(Progression(z_dec, y_inc, x_inc, (z_l, y_l, x_l)))
    result += fill(Progression(y_dec, z_dec, x_inc, (y_l, z_l, x_l)))
    result += fill(Progression(z_inc, y_dec, x_inc, (z_l, y_l, x_l)))
    result += fill(Progression(y_inc, z_inc, x_inc, (y_l, z_l, x_l)))
    
    # Top view.
    result += fill(Progression(x_inc, z_inc, y_dec, (x_l, z_l, y_l)))
    result += fill(Progression(z_inc, x_dec, y_dec, (z_l, x_l, y_l)))
    result += fill(Progression(x_dec, z_dec, y_dec, (x_l, z_l, y_l)))
    result += fill(Progression(z_dec, x_inc, y_dec, (z_l, x_l, y_l)))
    
    # Low view.
    result += fill(Progression(z_inc, x_inc, y_inc, (z_l, x_l, y_l)))
    result += fill(Progression(x_inc, z_dec, y_inc, (x_l, z_l, y_l)))
    result += fill(Progression(z_dec, x_dec, y_inc, (z_l, x_l, y_l)))
    result += fill(Progression(x_dec, z_inc, y_inc, (x_l, z_l, y_l)))
    
    return clean_pieces(result)
    
def try_to_fit(stack, target, pieces_order, rotations, my_piece):
    '''Try to fit a piece.'''
    p, state, ignore = stack[-1]
    for rotation in rotations[my_piece]:
        # Try a rotation.
        placed_rotation = rotation << p
        if placed_rotation < target and not placed_rotation & state:
            # If it fits, stack the new values.
            new_p = p
            new_state = state | placed_rotation
            while 0x01 << new_p & new_state:
                new_p = new_p + 1            
            stack.append((new_p, new_state, placed_rotation))
            if my_piece + 1 == len(pieces_order):
                # The last piece fitted. Return with the good news.
                return True
            elif try_to_fit(stack, target, pieces_order, rotations,
                my_piece + 1):
                # The remaining pieces fitted. Return with the good news.
                return True
        # It it doesn't fit immediately or exceedes the space, try a different
        # rotation.
    # If it runned out of rotations, try a different permutation.
    stack.pop()
    return False

def try_to_solve(rotations, space):
    '''Try permutations until it's solved.'''
    # Set the initial variables.
    target = 0
    state = 0
    p = 0
    for i in xrange(space[0] * space[1] * space[2]):
        target = target << 1 | 0x01
    
    permutations = itertools.permutations(xrange(len(rotations)))
    for a_permutation in permutations:
        # Try a permutation.
        stack = [(0, 0, 0),]
        if try_to_fit(stack, target, a_permutation, rotations, 0):
            return (a_permutation, stack)
    return (None, None)
    
def pack(blocks, space):
    '''Pack the blocks on the space and return a matrix with the positions.
    
    Parameters:
    * blocks: A list with a matrix of booleans. It should be like this: [][][].
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
    
    # Construct the set of rotations for each piece.
    rotations = {}
    for block in blocks:
        sizes = (len(block), len(block[0]), len(block[0][0]))
        rotations[len(rotations)] = get_rotation_chain(block, sizes)
    
    # Try iterating and getting a result.
    result = try_to_solve(rotations, space)
    
    # Return a result based on the previous result.
    if not result:
        print "You asked the impossible. BTW, entropy can't be reversed..yet."
    else:
        print "Congrats! There is a solution:", result
