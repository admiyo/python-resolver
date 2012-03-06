'''
Created on Mar 6, 2012

@author: ayoung
'''
import unittest
import Resolver.resolver
import ResolverTest



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

        Resolver.resolver.register(ResolverTest.resolver_test.SampleOp, do_something)
        
        res =   Resolver.resolver.Resolver()  
        
        y= res.resolve(ResolverTest.resolver_test.SampleOp)
        
        self.assertEqual("something", y.operation(), "factory got right instance")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()