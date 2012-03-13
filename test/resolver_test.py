'''
Created on Mar 6, 2012

@author: ayoung
'''
import unittest
import resolver

import test


class SampleBase:
    message = "Base"

    def operation(self):
        return self.message


class SampleSub(SampleBase):
    message = "sub"


def create_base(resolver):
    return SampleSub()


class SampleOp:

    def __init__(self, base):
        self.message = "something"
        self.base = base

    def operation(self):
        return self.base.operation()


def do_something(resolver):
    return  SampleOp(resolver.resolve(SampleBase))


class RequestObject:
    def __init__(self, global_object):
        self.global_object = global_object

    def do_op(self):
        return self.global_object.operation()


def request_object_factory(resolver):
    global_object = resolver.resolve(SampleBase)
    return RequestObject(global_object)


class Test(unittest.TestCase):
    def setUp(self):
        resolver.register(SampleOp, do_something)
        resolver.register(SampleBase, create_base)
        resolver.register(RequestObject, request_object_factory,
                          resolver.REQUEST_SCOPE)

    def tearDown(self):
        resolver.scope_map = {resolver.GLOBAL_SCOPE.name: dict(),
                              resolver.REQUEST_SCOPE.name: dict()}
        resolver.global_resolver.factories = dict()

    def testName(self):
        res = resolver.Resolver()
        op = res.resolve(SampleOp)
        self.assertEqual("sub", op.operation(), "factory got right instance")

        base = res.resolve(SampleBase)
        self.assertEqual("sub", base.operation())

    def test_delegation(self):
        params = dict()
        headers = dict()
        request_resolver = resolver.RequestResolver(params, headers)
        op = request_resolver.resolve(RequestObject)
        self.assertEqual("sub", op.do_op(), "factory got right instance")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
