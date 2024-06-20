
import unittest
from bandit.time import Time
from bandit.object import Object

class TestTime(unittest.TestCase):
    def setUp(self):
        self.time_graph = Time()
        self.obj_a = Object()
        self.obj_b = Object()
        self.obj_c = Object()

    def test_add_thread(self):
        self.time_graph.add_thread(self.obj_a, self.obj_b)
        objects_tuple = [(edge[0], edge[1]) for edge in self.time_graph.threads()]
        self.assertIn((self.obj_a, self.obj_b), objects_tuple)

    def test_remove_thread(self):
        self.time_graph.add_thread(self.obj_a, self.obj_b)
        self.time_graph.remove_thread(self.obj_a, self.obj_b)
        
        objects_tuple = [(edge[0], edge[1]) for edge in self.time_graph.threads()]
        
        self.assertNotIn((self.obj_a, self.obj_b), objects_tuple)

    # def test_add_space(self):
    #     space_state = {1: self.obj_a, 2: self.obj_b}
    #     self.time_graph.add_space(space_state)
    #     self.assertIn(1, self.time_graph.nodes())
    #     self.assertIn(2, self.time_graph.nodes())

    def test_threads_between_new_and_old_states(self):
        self.time_graph.add_space({1: self.obj_a})
        self.time_graph.add_space({2: self.obj_b})
        self.time_graph.add_thread(self.obj_a, self.obj_b)
        expected_threads = [(self.obj_a, self.obj_b)]
        actual_threads = list(self.time_graph.edges())
        self.assertEqual(expected_threads, actual_threads)

if __name__ == '__main__':
    unittest.main()