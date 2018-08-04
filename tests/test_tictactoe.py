import unittest
import logging
import logging.config
import time
import minimax_tree
import tictactoe_solver


class TestTicTacToe(unittest.TestCase):

    DEPTH = 5

    def setUp(self):
        root_board = [['.'] * 3 for _ in range(3)]
        self.node = tictactoe_solver.TicTacToeNode(root_board)

        self.logger = logging.getLogger("minimax")
        self.logger.setLevel(logging.DEBUG)
        debug_filehandler = logging.FileHandler("tictac.log",mode="w")
        info_filehandler = logging.FileHandler("tictac_metrics.log", mode="a")
        info_filehandler.setLevel(logging.INFO)
        formatter = logging.Formatter(r"%(name)s: \n %(levelname)s: \n %(msg)s")

        debug_filehandler.setFormatter(formatter)
        info_filehandler.setFormatter(formatter)
        self.logger.addHandler(info_filehandler)
        self.logger.addHandler(debug_filehandler)

    def tearDown(self):
        # truncates log file
        pass

    @classmethod
    def tearDownClass(cls):
        logfile = open("tictac.log","w+")
        logfile.close()

    def test_next_moves(self):
        '''
        Tests if 9 boards are generated for root board
        :return:
        '''
        moves_lst = self.node.generate_moves(True)
        self.assertEqual(moves_lst[0].state[0][0], 'x')
        self.assertEqual(moves_lst[4].state[1][1], 'x')
        self.assertEqual(len(moves_lst), 9)

    def test_minimax(self):
        '''
        Tests minimax algo on root board of xo
        It will output time elapsed.
        :return:
        '''
        start = time.time()

        (_,final_val) = minimax_tree.minimax(self.node, True)

        end = time.time()
        print('Time elapsed : {}'.format(end - start))
        self.assertEqual(final_val, 0,msg="Result is not a draw")
        print(final_val)

    def test_compute_heuristic(self):
        '''
        Tests if the heuristic returns appropriate value
        :return:
        '''
        board1 = [['o','x',' .'],['x','o','x'],['.','.','.']]
        board2 = [['x','.',' .'],['.','o','o'],['x','.','x']]

        self.assertAlmostEqual(tictactoe_solver.compute_simple_heuristic(board1,True),-1, delta=1)
        self.assertAlmostEqual(tictactoe_solver.compute_simple_heuristic(board2,True),1,delta=1)

    def test_minimax_depth_limited(self):
        '''
        Tests depth limited minimax algorithm
        :return:
        '''
        start = time.time()

        val = minimax_tree.depth_limited_minimax(self.node, self.DEPTH, True)

        end = time.time()
        self.logger.info('Minimax depth {} \tTime elapsed: {}'.format(self.DEPTH, end - start))
        self.assertEqual(val, 0,msg="Result is not a draw")
        print(val)


    def test_alpha_beta_minimax(self):
        '''
        Tests alpha beta pruning algorithm
        :return:
        '''
        start = time.time()
        val = minimax_tree.alpha_beta_pruning_minimax(self.node, True, minimax_tree.NINF, minimax_tree.PINF)
        end = time.time()
        self.logger.info('\t:Alpha Beta pruning: \tTime elapsed: {}'.format( end - start))
        self.assertEqual(val, 0, msg="Result is not a draw")
        print(val)




    def test_evaluate(self):
        '''
        Test if node value is None as it is not leaf
        '''

        self.assertEqual(self.node.evaluate(),0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
