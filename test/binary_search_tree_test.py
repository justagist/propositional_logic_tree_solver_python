import unittest
from bst_src import NodeType, BinaryTreeNode

import logging

fmt = '[%(levelname)s] -- %(lineno)d: %(message)s\n'
logging.basicConfig(format=fmt, level=logging.DEBUG)

class BinaryTreeUnitTest(unittest.TestCase):

    def test_tree(self):
        typeList = [ NodeType.R, NodeType.P, NodeType.OR, NodeType.TRUE, NodeType.Q, NodeType.NOT, NodeType.AND, NodeType.IMPLIES ]
        logging.debug("typeList: %s"%str(typeList))

        # ====== Construction ======

        pltree = BinaryTreeNode.build_from_reverse_polish(typeList)

        self.assertIsNotNone(pltree,"PLTree construction failed when using: " + str(typeList))

        logging.debug("Constructed: " + pltree.in_prefix_notation())
        logging.debug("Constructed: " + pltree.in_infix_notation())
        
        self.assertEqual(pltree.in_prefix_notation(),"implies(or(R,P),and(true,not(Q)))")
        self.assertEqual(pltree.in_infix_notation(),"((R∨P)→(⊤∧¬Q))")
        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[R, P, OR, TRUE, Q, NOT, AND, IMPLIES]".lower())


        # ===== Apply Bindings ======

        bindings = [(NodeType.P, True), (NodeType.R, False)]

        pltree.apply_variable_bindings(bindings)
        
        logging.debug("Applied bindings : %s to get: %s"%(bindings, pltree.in_prefix_notation()))
        logging.debug("Applied bindings : %s to get: %s"%(bindings, pltree.in_infix_notation()))

        self.assertEqual(pltree.in_prefix_notation(),"implies(or(false,true),and(true,not(Q)))")
        self.assertEqual(pltree.in_infix_notation(),"((⊥∨⊤)→(⊤∧¬Q))")
        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, TRUE, OR, TRUE, Q, NOT, AND, IMPLIES]".lower())


        # ===== Eliminate Implies =====

        pltree.eliminate_implies();

        logging.debug("Eliminate Implies: %s"%pltree.in_prefix_notation())
        logging.debug("Eliminate Implies: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"or(not(or(false,true)),and(true,not(Q)))")
        self.assertEqual(pltree.in_infix_notation(),"(¬(⊥∨⊤)∨(⊤∧¬Q))")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, TRUE, OR, NOT, TRUE, Q, NOT, AND, OR]".lower())


        # ===== Push Not Down ===== 

        # typeList = [ NodeType.R, NodeType.NOT, NodeType.NOT, NodeType.NOT, NodeType.NOT, NodeType.NOT ]
        # logging.debug("typeList: %s"%str(typeList))
        # pltree = BinaryTreeNode.build_from_reverse_polish(typeList)

        pltree.push_not_down()

        logging.debug("Push Not Down: %s"%pltree.in_prefix_notation())
        logging.debug("Push Not Down: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"or(and(not(false),not(true)),and(true,not(Q)))")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, NOT, TRUE, NOT, AND, TRUE, Q, NOT, AND, OR]".lower())


        # ====== Push Or Below And =====



if __name__ == '__main__':
    unittest.main()

