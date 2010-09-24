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
    
    '''
    pass
    
def get_rotation_chain(block, x, y, z):
    '''Generate a list with the unique rotations of a block.
    
    This function is necessarily ugly, because I'm retarded and I couldn't find
    a fancy way to put it. Since it will be a hairy function anyway, just do it
    ugly.
    
    '''
    # Get the rotation once per face
    result = list()
    
    # Rotations for the front view.
    newPiece = x * [y * [z * [False]]]
    for i in xrange(x):
        for j in xrange(y):
            for k in xrange(z):
                newPiece[i][j][k] = block[i][j][k]
    result.add(newPiece)
    
    newPiece = z * [y * [x * [False]]]
    for i in xrange(z):
        for j in xrange(y):
            for k in xrange(x):
                newPiece[i][j][k] = block[z-k][j][i]
    result.add(newPiece)

    newPiece = x * [y * [z * [False]]]
    for i in xrange(x):
        for j in xrange(y):
            for k in xrange(z):
                newPiece[i][j][k] = block[x-i][j][z-k]
    result.add(newPiece)
    
    newPiece = z * [y * [x * [False]]]
    for i in xrange(z):
        for j in xrange(y):
            for k in xrange(x):
                newPiece[i][j][k] = block[k][j][x-i]
    result.add(newPiece)
    
def next_rotated_block(block, rotateChain):
    '''Generate a non-repeating sequence of rotated blocks.'''
    pass
