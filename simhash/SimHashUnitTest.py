import unittest
import SimHash as sh

class SimHashTests(unittest.TestCase):
    def test_init(self):
        #test_dict = {'a':1 , 'b': 2}
        simHash = sh.SimHash(0.5)
        self.assertEqual(set(),simHash.hashes())
        self.assertEqual(0.5, simHash.threshold())
    
    def test_addOne(self):
        test_dict1 = {'a':1 , 'b': 2}
        simHash = sh.SimHash(0.5)
        similarRes = simHash.similar(test_dict1)

        self.assertFalse(similarRes)
        #print(simHash.hashes())
    
    def test_addTwo(self):
        test_dict1 = {'a':1 , 'b': 2}
        test_dict2 = {'c':1 , 'd': 2}
        simHash = sh.SimHash(1)
        similarRes = simHash.similar(test_dict1)
        similarRes = simHash.similar(test_dict2)
        
        self.assertFalse(similarRes)
    
    def test_addTwoSame(self):
        test_dict1 = {'a':1 , 'b': 2}
        simHash = sh.SimHash(1)
        similarRes = simHash.similar(test_dict1)
        similarRes = simHash.similar(test_dict1)
        
        self.assertTrue(similarRes)
        



if __name__ == '__main__':
    unittest.main()