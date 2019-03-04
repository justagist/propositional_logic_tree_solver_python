import copy
from plt_src import NodeType


class PLTreeNode:

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
        
    def get_reverse_polish(self, node_queue = None):
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
        if node_queue is None: # ----- setting default function arg value = [] does not work for some reason
            node_queue = []

        if self._child1 is not None:
            self._child1.get_reverse_polish(node_queue)
        if self._child2 is not None:
            self._child2.get_reverse_polish(node_queue)

        node_queue.append(self._type)

        # print(node_queue)

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

    def apply_variable_bindings(self, val_bindings_map):

        '''
            Applies a set of variable bindings recursively to the propositional logic
            expression represented by the current <PLTreeNode>
            
            @Args: bindings
                       A map that maps NodeType objects to boolean
                       values. Any variable in bindings that does not
                       appear in the tree will be ignored. Any NodeType
                       in bindings that is not a variable will be ignored.
            
        '''
        # print (self._type, self._child1, self._child2, "type")

        if not self._type.is_var():
            if self._child1 is not None:
                self._child1.apply_variable_bindings(val_bindings_map)
            if self._child2 is not None:
                self._child2.apply_variable_bindings(val_bindings_map)

        else:
            for val, binding in val_bindings_map:
                if val == self._type:
                    self._type = NodeType.TRUE if binding == True else NodeType.FALSE

    def eliminate_implies(self):

        '''
            Recursively replace in place every occurrence of the
            pattern x→y with ¬x∨y, for sub-trees x and y           

        '''
        if self._child1 is not None:
            self._child1.eliminate_implies()
        if self._child2 is not None:
            self._child2.eliminate_implies()

        if self._type == NodeType.IMPLIES:
            self._type = NodeType.OR

            new_child = copy.deepcopy(self._child1)
            self._child1._type = NodeType.NOT
            self._child1._child1 = new_child
            self._child1._child2 = None


    def push_not_down(self):

        '''
            Recursively replace in-place, for sub-trees
            x and y, every occurrence of:
            ¬¬x with x
            ¬(x∨y) with (¬x∧¬y)
            ¬(x∧y) with (¬x∨¬y)
            ¬¬¬¬¬x should be reduced to x
            
        '''

        if self._type == NodeType.NOT:
            if self._child1._type == NodeType.NOT:

                # print (self.in_infix_notation(),"this")
                childcopy = copy.deepcopy(self._child1._child1)
                self._type = childcopy._type
                self._child1 = childcopy._child1
                self._child2 = childcopy._child2

                # print (self.in_infix_notation(),"this")

            elif self._child1._type == NodeType.AND:
                
                self_copy1 = copy.deepcopy(self) 
                self_copy1._child1 = copy.deepcopy(self._child1._child1)
                self_copy1._child2 = None

                self_copy2 = copy.deepcopy(self)
                self_copy2._child1 = copy.deepcopy(self._child1._child2)
                self_copy2._child2 = None

                self._type = NodeType.OR

                self._child1 = self_copy1

                self._child2 = self_copy2

            elif self._child1._type == NodeType.OR:
                
                # ----- create new NOT TreeNodes 
                self_copy1 = copy.deepcopy(self) 
                self_copy1._child1 = copy.deepcopy(self._child1._child1)
                self_copy1._child2 = None

                self_copy2 = copy.deepcopy(self)
                self_copy2._child1 = copy.deepcopy(self._child1._child2)
                self_copy2._child2 = None

                self._type = NodeType.AND

                self._child1 = self_copy1

                self._child2 = self_copy2


        if self._child1 is not None:
            self._child1.push_not_down()
        if self._child2 is not None:
            self._child2.push_not_down()


    def push_or_below_and(self):

        '''
            Recursively replace in place, for sub-trees x, y, and z, every occurrence of:
            
            x∨(y∧z) with (x∨y)∧(x∨z)
            (x∧y)∨z with (x∨z)∧(y∨z)

            This step is also knows as "distributing OR over AND"
            
        '''

        if self._child1 is not None:
            self._child1.push_or_below_and()
        if self._child2 is not None:
            self._child2.push_or_below_and()


        if self._type == NodeType.OR:
            if self._child1._type == NodeType.AND:
                self_copy = copy.deepcopy(self)
                childcopy = copy.deepcopy(self._child2)
                child12_copy = copy.deepcopy(self._child1._child2)

                self._type = NodeType.AND
                
                self._child1._type = NodeType.OR
                self._child1._child2 = copy.deepcopy(childcopy)

                self._child2._type = NodeType.OR
                self._child2._child1 = copy.deepcopy(child12_copy)
                self._child2._child2 = copy.deepcopy(childcopy)

            elif self._child2._type == NodeType.AND:
                self_copy = copy.deepcopy(self)
                childcopy = copy.deepcopy(self._child1)
                child21_copy = copy.deepcopy(self._child2._child1)

                self._type = NodeType.AND
                
                self._child2._type = NodeType.OR
                self._child2._child1 = copy.deepcopy(childcopy)

                self._child1._type = NodeType.OR
                self._child1._child2 = copy.deepcopy(child21_copy)
                self._child1._child1 = copy.deepcopy(childcopy)

            self._child1.push_or_below_and()
            self._child2.push_or_below_and()

    def make_and_or_right_deep(self):

        '''
            Recursively replace in place, for sub-trees
            W, X, Y and Z, every
            occurrence of:
            
            (X∨Y)∨Z with X∨(Y∨Z)
            (X∧Y)∧Z with X∧(Y∧Z)
           
            This is the closest we can come in a binary tree representation to
            "flattening" the conjunctions and disjunctions as the last step in
            producing Conjunctive Normal Form. The result is to turn complex trees of
            nested conjunctions into a simple right deep tree of conjunctions and
            similarly for disjunctions Thus this will change:
            
            (W∨X)∨(Y∨Z) into W∨(X∨(Y∨Z))
            ((W∨X)∨Y)∨Z into W∨(X∨(Y∨Z))
            
        '''

        if self._type == NodeType.OR and self._child1._type == NodeType.OR:
            child11copy = copy.deepcopy(self._child1._child1)
            child12copy = copy.deepcopy(self._child1._child2)
            child2copy  = copy.deepcopy(self._child2)

            self._child1 = child11copy

            self._child2._type = NodeType.OR
            self._child2._child1 = child12copy
            self._child2._child2 = child2copy

        elif self._type == NodeType.AND and self._child1._type == NodeType.AND:
            child11copy = copy.deepcopy(self._child1._child1)
            child12copy = copy.deepcopy(self._child1._child2)
            child2copy  = copy.deepcopy(self._child2)

            self._child1 = child11copy

            self._child2._type = NodeType.AND
            self._child2._child1 = child12copy
            self._child2._child2 = child2copy

        if self._child1 is not None:
            self._child1.make_and_or_right_deep()
        if self._child2 is not None:
            self._child2.make_and_or_right_deep()


    def evaluate_constant_subtrees(self):
        '''
            Evaluate the logical expression tree recursively, updating it in
            place to reduce constant sub-trees (i.e. those containing no
            variables) and make simplifications that do not require deep comparisons.
            
            Thus ⊥∧A should be reduced to ⊥, as it has to
            be ⊥ no matter what value A takes.
    
            Similarly ⊥∧(A∨B) should be reduced to ⊥, as it
            has to be ⊥ no matter what value the right sub-expression
            (A∨B) takes.
            
            A further example: A tree that is the logical AND of one expression and
            the logical NOT of the same expression must be false. However, that can
            only be discovered by doing a deep comparison of the two sub-trees and
            therefore should not be done. A simple example of this is
            A∧¬A. In this case, although both sub-expressions are the
            same variable and are easy to compare, we should not make the evaluation
            to ⊥ because we should not make comparisons that two
            sub-expressions are equal
    
            
            @Return:
                    True if this tree evaluates to true,
                    False if this tree evaluates to false
                    None if this tree cannot be fully evaluated to either true or false
            
        '''

        if self._type == NodeType.TRUE:
            return True
        elif self._type == NodeType.FALSE:
            return False

        if self._type._arity == 0:
            return None
        elif self._type._arity == 1:
            val = self._child1.evaluate_constant_subtrees()
            if val is not None:
                if val == True:
                    self._type = NodeType.TRUE
                    self._child1 = None
                    self._child2 = None
                elif val == False:
                    self._type = NodeType.FALSE
                    self._child1 = None
                    self._child2 = None
            else:
                return None

        elif self._type.arity == 2:
            child1_val = self._child1.evaluate_constant_subtrees()
            child2_val = self._child2.evaluate_constant_subtrees()
            child1_copy = copy.deepcopy(self._child1)
            child2_copy = copy.deepcopy(self._child2)

            if child1_val == None and child2_val == None:
                return None

            elif child1_val == True and child2_val == True:
                self._type = NodeType.TRUE
                self._child1 = None
                self._child2 = None
                

            elif self._type == NodeType.AND:
                if child1_val == False or child2_val == False:
                    self._type = NodeType.FALSE
                    self._child1 = None
                    self._child2 = None
                    

                elif child1_val == True:

                    self._type = child2_copy._type
                    self._child1 = child2_copy._child1
                    self._child2 = child2_copy._child2

                elif child2_val == True:
                    self._type = child1_copy._type
                    self._child1 = child1_copy._child1
                    self._child2 = child1_copy._child2

            elif child1_val == True:

                if child2_val == False:
                    if self._type == NodeType.OR:
                        self._type = NodeType.TRUE
                        self._child1 = None
                        self._child2 = None
                        
                    elif self._type == NodeType.IMPLIES:
                        self._type = NodeType.FALSE
                        self._child1 = None
                        self._child2 = None

                if child2_val is None:
                    if self._type == NodeType.OR:
                        self._type = NodeType.TRUE
                        self._child1 = None
                        self._child2 = None
                        
                    elif self._type == NodeType.IMPLIES:
                        self._type = child2_copy._type
                        self._child1 = child2_copy._child1
                        self._child2 = child2_copy._child2

            elif child1_val == False:
                if child2_val == True:
                    # input()
                    self._type = NodeType.TRUE
                    self._child1 = None
                    self._child2 = None
                    

                elif child2_val == False:
                    if self._type == NodeType.OR:
                        self._type = NodeType.FALSE
                        self._child1 = None
                        self._child2 = None
                        
                    elif self._type == NodeType.IMPLIES:
                        self._type = NodeType.TRUE
                        self._child1 = None
                        self._child2 = None
                elif child2_val is None:
                    if self._type == NodeType.OR:
                        self._type = child2_copy._type
                        self._child1 = child2_copy._child1
                        self._child2 = child2_copy._child2

                    elif self._type == NodeType.IMPLIES:
                        self._type = NodeType.TRUE
                        self._child1 = None
                        self._child2 = None

            elif child1_val is None:
                if child2_val == True:
                    self._type = NodeType.TRUE
                    self._child1 = None
                    self._child2 = None
                    
                elif child2_val == False:
                    self._type = child1_copy._type
                    self._child1 = child1_copy._child1
                    self._child2 = child1_copy._child2

                elif child2_val is None:
                    self._type = NodeType.NOT
                    self._child1 = child1_copy

        return self.evaluate_constant_subtrees()

    def reduce_to_CNF(self):
        '''
            This takes the tree and executes all steps in
            the correct order to reduce it to Conjunctive Normal Form (CNF)
            
            Note that it does NOT call evaluateConstantSubtrees(). This does not change the fact that
            the result is in CNF, it just means that it is perhaps larger than it need be. Feel free to call
            it at any time to simplify the results.
            
            Note that if you call the contained methods below in a different order, you are not guaranteed
            to end up with an expression in CNF     

        '''
        self.eliminate_implies()
        self.push_not_down()
        self.push_or_below_and()
        self.make_and_or_right_deep()



    def __str__(self):
        return self.in_prefix_notation()

    def __repr__(self):
        return str(self._type)

    def __eq__(self,other):
        return self.__dict__ == other.__dict__


if __name__ == '__main__':
    
    c1 = PLTreeNode(NodeType.A)
    c2 = PLTreeNode(NodeType.B)
    a = PLTreeNode(NodeType.AND, c1, c2)

    types = [NodeType.R, NodeType.P, NodeType.OR, NodeType.TRUE, NodeType.Q, NodeType.NOT, NodeType.AND, NodeType.IMPLIES]

    tree = PLTreeNode.build_from_reverse_polish(types)

    print (tree.in_infix_notation())

