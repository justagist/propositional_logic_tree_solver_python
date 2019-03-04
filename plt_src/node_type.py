

class NodeTypeBase():

    def __init__(self, prefix_name, infix_name, arity, is_var = False):
        '''
            Construct an NodeType: this cannot be called by the programmer
            
            @Args:
                prefix_name     : The name that appears when printed in prefix notation format
                infix_name      : The name that appears when printed in infix notation format
                arity  (int)    : The number of arguments that this propositional logic term takes
                is_var (bool)   : True if this element is a variable

        '''
        self._prefix_name = prefix_name
        self._infix_name = infix_name
        self._arity = arity
        self._is_var = is_var

    @property
    def prefix_name(self):
        return self._prefix_name

    @property
    def infix_name(self):
        return self._infix_name
    
    @property
    def arity(self):
        return self._arity

    def is_var(self):
        return self._is_var

    @classmethod
    def Variable(cls, val : str):
        '''
            Create a NodeType of Variables (any from A - Z)
            @Args:
                val (char): single char from "A" to "Z"
        '''
        if isinstance(val,str) and val.isalpha and len(val) == 1:
            return cls(val.upper(), val.upper(), 0, True)
        else:
            raise ValueError("%s is not a valid name for NodeType object"%val)

    def __str__(self):
        return self.prefix_name

    def __repr__(self):
        return self.prefix_name

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    


class NodeType():
    '''
        Constructs the different possible nodes in a binary tree

    ''' 

    IMPLIES = NodeTypeBase( "implies",   u"\u2192" , 2 )
    AND     = NodeTypeBase( "and",       u"\u2227" , 2 )
    OR      = NodeTypeBase( "or",        u"\u2228" , 2 )
    NOT     = NodeTypeBase( "not",       u"\u00AC" , 1 )

    TRUE    = NodeTypeBase( "true",      u"\u22A4" , 0 )
    FALSE   = NodeTypeBase( "false",     u"\u22A5" , 0 )

    
    import string
    '''
        Create NodeTypeBase objects of type A = NodeTypeBase.Variable("A") for all uppercase alphabets A - Z
    '''
    for a in list(string.ascii_letters):
        exec("%s = NodeTypeBase.Variable('%s')" % (a, a))



if __name__ == '__main__':
    # print NodeType.IMPLIES
    # a = NodeType("a")
    a = NodeType.b
    # print (test(2))


    print( a._prefix_name, a._infix_name, a._arity)
    print( NodeType.AND.infix_name)

