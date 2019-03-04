
from bst_src import NodeType


class BinaryTreeNode:

    def __init__(self, nodetype:NodeType, child1 = None, child2 = None):
        '''
            The usual constructor used internally in this class.

            @Args 
                type: The NodeType represented by this node
                child1: The first child, if there is one, or null if there isn't
                child2: The second child, if there is one, or null if there isn't

        '''

        self._type = nodetype
        self._child1 = child1
        self._child2 = child2

    @classmethod
    def build_from_reverse_polish(cls, list_of_nodetypes):
        '''
            Takes a list of NodeType values describing a valid propositional logic expression in reverse polish notation and constructs
            the corresponding expression tree
            
            @Args: list_of_nodetypes    : List of NodeType objects in a valid propositional logic expression in reverse polish notation
            
            @Return : the PLTreeNode of the root of the tree representing
                      the expression constructed for the reverse polish order
                            
                [ R, P, OR, TRUE, Q, NOT, AND, IMPLIES ] represents ((R∨P)→(⊤∧¬Q))
             
        '''
        if len(list_of_nodetypes) == 0:

            raise ValueError("NodeType list empty")

        retval = []

        for node in list_of_nodetypes:
            arity = node.arity

            if arity == 0:
                retval.append(cls(node))
            elif arity == 1:
                child1 = retval.pop()
                retval.append(cls(node,child1))
            elif arity == 2:
                child2 = retval.pop()
                child1 = retval.pop()
                retval.append(cls(node,child1,child2))

        if len(retval) != 1:
            raise ValueError("Incomplete or wrong sequence given. Tree creation failed.")

        return retval.pop()
        
    def get_reverse_polish(self, node_queue = []):
        '''
            Returns the list of NodeType entries which, if provide to
            reversePolishBuilder, would construct the current tree.
            Recurrence used to accumulate the elements of the reverse 
            polish notation description of the current tree
         
            @Args: nodeQueue
                    A list of NodeType objects used to accumulate
                    the values of the reverse polish notation description of the
                    current tree

            @Return  A NodeType array of the reverse polish notation
                      specification of this tree
     
        '''
        if self._child1 != None:
            self._child1.get_reverse_polish(node_queue)
        if self._child2 != None:
            self._child2.get_reverse_polish(node_queue)

        node_queue.append(self._type)

        return node_queue

    def in_prefix_notation(self):
        '''
            Prints out the string in prefix notation. 
            
            The following are examples of prefix notation:
            
            implies(or(R,P),and(true,not(Q)))
            or(not(or(false,true)),and(true,not(Q)))
            and(or(not(false),true),and(or(not(false),not(Q)),and(or(not(true),true),or(not(true),not(Q)))))
            
            
            @Return:  the string representation of the tree rooted at this node in
                      prefix notation
            
        '''
        arity = self._type.arity

        if arity == 0:
            return self._type.prefix_name
        elif arity == 1:
            return "%s(%s)"%(self._type.prefix_name, self._child1.in_prefix_notation())
        elif arity == 2:
            return "%s(%s,%s)"%(self._type.prefix_name, self._child1.in_prefix_notation(), self._child2.in_prefix_notation())
        else:
            raise ValueError("Invalid Arity")

    def in_infix_notation(self):
        '''
            Prints out the string in infix notation. 
            
            The following are examples of infix notations:
            
            ((R∨P)→(⊤∧¬Q))
            (¬(⊥∨⊤)∨(⊤∧¬Q))
            ((¬⊥∨⊤)∧((¬⊥∨¬Q)∧((¬⊤∨⊤)∧(¬⊤∨¬Q))))
            

            @Return:  the string representation of the tree rooted at this node in
                      infix notation
            
        '''
        arity = self._type.arity

        if arity == 0:
            return self._type.infix_name
        elif arity == 1:
            return "%s%s"%(self._type.infix_name, self._child1.in_infix_notation())
        elif arity == 2:
            return "(%s%s%s)"%(self._child1.in_infix_notation(), self._type.infix_name, self._child2.in_infix_notation())
        else:
            raise ValueError("Invalid Arity")



    def __str__(self):
        return self.in_prefix_notation()

    def __repr__(self):
        return str(self._type)


if __name__ == '__main__':
    
    c1 = BinaryTreeNode(NodeType.A)
    c2 = BinaryTreeNode(NodeType.B)
    a = BinaryTreeNode(NodeType.AND, c1, c2)

    types = [NodeType.R, NodeType.P, NodeType.OR, NodeType.TRUE, NodeType.Q, NodeType.NOT, NodeType.AND, NodeType.IMPLIES]

    tree = BinaryTreeNode.build_from_reverse_polish(types)

    print (tree.in_infix_notation())

