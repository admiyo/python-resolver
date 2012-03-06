'''
Created on Mar 6, 2012

@author: ayoung
'''
import unittest
import resolver
import test



class SampleOp:
    def __init__(self):
        self.message = "something"
        
    def operation(self):
        return self.message


def do_something(resolver):
    return  SampleOp()
        

class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testName(self):
        resolver.register(SampleOp, do_something)
        
        res =   resolver.Resolver()  
        
        y= res.resolve(SampleOp)
        
        self.assertEqual("something", y.operation(), "factory got right instance")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()