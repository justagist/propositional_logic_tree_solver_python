import unittest
from plt_src import NodeType, PLTreeNode

import logging

fmt = '[%(levelname)s] -- %(lineno)d: %(message)s\n'
logging.basicConfig(format=fmt, level=logging.DEBUG)

class PLTreeUnitTest(unittest.TestCase):

    def test_tree(self):
        typeList = [ NodeType.R, NodeType.P, NodeType.OR, NodeType.TRUE, NodeType.Q, NodeType.NOT, NodeType.AND, NodeType.IMPLIES ]
        logging.debug("typeList: %s"%str(typeList))

        # ====== Construction ======

        pltree = PLTreeNode.build_from_reverse_polish(typeList)

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


        pltree.push_not_down()

        logging.debug("Push Not Down: %s"%pltree.in_prefix_notation())
        logging.debug("Push Not Down: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"or(and(not(false),not(true)),and(true,not(Q)))")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, NOT, TRUE, NOT, AND, TRUE, Q, NOT, AND, OR]".lower())


        # ===== Push Or Below And =====

        # typeList = [ NodeType.P, NodeType.Q, NodeType.R, NodeType.AND,  NodeType.OR]
        # logging.debug("typeList: %s"%str(typeList))
        # pltree = PLTreeNode.build_from_reverse_polish(typeList)
        pltree.push_or_below_and()

        logging.debug("Push Or Below And: %s"%pltree.in_prefix_notation())
        logging.debug("Push Or Below And: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"and(and(or(not(false),true),or(not(false),not(Q))),and(or(not(true),true),or(not(true),not(Q))))")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, NOT, TRUE, OR, FALSE, NOT, Q, NOT, OR, AND, TRUE, NOT, TRUE, OR, TRUE, NOT, Q, NOT, OR, AND, AND]".lower())


        # ===== Make And Or Right Deep ===== 

        pltree.make_and_or_right_deep()

        logging.debug("Make And Or Right Deep: %s"%pltree.in_prefix_notation())
        logging.debug("Make And Or Right Deep: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"and(or(not(false),true),and(or(not(false),not(Q)),and(or(not(true),true),or(not(true),not(Q)))))")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[FALSE, NOT, TRUE, OR, FALSE, NOT, Q, NOT, OR, TRUE, NOT, TRUE, OR, TRUE, NOT, Q, NOT, OR, AND, AND, AND]".lower())


        # ===== Evaluate Constant Sub-Trees ===== 

        pltree.evaluate_constant_subtrees()

        logging.debug("Evaluate Constant Sub-Trees: %s"%pltree.in_prefix_notation())
        logging.debug("Evaluate Constant Sub-Trees: %s"%pltree.in_infix_notation())

        self.assertEqual(pltree.in_prefix_notation(),"not(Q)")

        typeListReturned = pltree.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[Q, NOT]".lower())

    # def test2(self):

        typeList2 = [NodeType.R, NodeType.P, NodeType.IMPLIES, NodeType.S, NodeType.IMPLIES, NodeType.NOT, NodeType.Q, NodeType.IMPLIES]
        logging.debug("typeList: %s"%str(typeList2))

        # ====== Construction ======

        pltree2 = PLTreeNode.build_from_reverse_polish(typeList2)

        self.assertIsNotNone(pltree2,"PLTree construction failed when using: " + str(typeList2))

        logging.debug("Constructed: " + pltree2.in_prefix_notation())
        logging.debug("Constructed: " + pltree2.in_infix_notation())

        # ===== Reduce to CNF ===== 
        pltree2.reduce_to_CNF()

        logging.debug("Reduced to CNF: " + pltree2.in_prefix_notation())
        logging.debug("Reduced to CNF: " + pltree2.in_infix_notation())

        self.assertEqual(pltree2.in_prefix_notation(),"and(or(R,or(S,Q)),or(not(P),or(S,Q)))")

        typeListReturned = pltree2.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

        self.assertEqual(str(typeListReturned).lower(),"[R, S, Q, OR, OR, P, NOT, S, Q, OR, OR, AND]".lower())

        # ===== Evaluate Constant Sub-Trees =====
        pltree2.evaluate_constant_subtrees()

        logging.debug("Evaluate Constant Sub-Trees: %s"%pltree2.in_prefix_notation())
        logging.debug("Evaluate Constant Sub-Trees: %s"%pltree2.in_infix_notation())

        self.assertEqual(pltree2.in_prefix_notation(),"and(or(R,or(S,Q)),or(not(P),or(S,Q)))")

        typeListReturned = pltree2.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))


    # def test3(self):
        logging.info("\nTest for Push Or Below And\n")

        typeList2 = [NodeType.A, NodeType.B, NodeType.AND, NodeType.C, NodeType.OR, NodeType.D, NodeType.OR, NodeType.E, NodeType.OR, NodeType.F, NodeType.OR, NodeType.G, NodeType.OR, NodeType.H, NodeType.OR]
        logging.debug("typeList: %s"%str(typeList2))

        # ====== Construction ======

        pltree2 = PLTreeNode.build_from_reverse_polish(typeList2)

        self.assertIsNotNone(pltree2,"PLTree construction failed when using: " + str(typeList2))

        logging.debug("Constructed: " + pltree2.in_prefix_notation())
        logging.debug("Constructed: " + pltree2.in_infix_notation())

        # ===== Reduce to CNF ===== 
        pltree2.push_or_below_and()

        logging.debug("Push Or Below And: " + pltree2.in_prefix_notation())
        logging.debug("Push Or Below And: " + pltree2.in_infix_notation())

        self.assertEqual(pltree2.in_prefix_notation(),"and(or(or(or(or(or(or(A,C),D),E),F),G),H),or(or(or(or(or(or(B,C),D),E),F),G),H))")

        typeListReturned = pltree2.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))

    # def test3(self):
        logging.info("\nExtra Test for Push Or Below And\n")

        typeList2 = [NodeType.A, NodeType.B, NodeType.AND, NodeType.C, NodeType.AND, NodeType.D, NodeType.OR, NodeType.E, NodeType.OR]
        logging.debug("typeList: %s"%str(typeList2))

        # ====== Construction ======

        pltree2 = PLTreeNode.build_from_reverse_polish(typeList2)

        self.assertIsNotNone(pltree2,"PLTree construction failed when using: " + str(typeList2))

        logging.debug("Constructed: " + pltree2.in_prefix_notation())
        logging.debug("Constructed: " + pltree2.in_infix_notation())

        # ===== Reduce to CNF ===== 
        pltree2.push_or_below_and()

        logging.debug("Push Or Below And: " + pltree2.in_prefix_notation())
        logging.debug("Push Or Below And: " + pltree2.in_infix_notation())

        self.assertEqual(pltree2.in_prefix_notation(),"and(and(or(or(A,D),E),or(or(B,D),E)),or(or(C,D),E))")

        typeListReturned = pltree2.get_reverse_polish()
        logging.debug("typeListReturned: " + str(typeListReturned))






        
if __name__ == '__main__':
    unittest.main()

