'''
Created on Mar 6, 2012

@author: ayoung
'''


class Scope(object):
    def __init__(self):
        '''
        Constructor
        '''
scope_map = dict([])


def register(classname, proxy, scope=None):
    if (scope in scope_map):
        proxy_map = scope_map[scope]
        if (classname in proxy_map):
            raise ValueError(classname +
                            "already has creation proxy registered")
    else:
        proxy_map = dict()
        scope_map[scope] = proxy_map
    proxy_map[classname] = proxy


class Resolver(object):
    '''
    classdocs
    '''
    instances = dict()

    def __init__(self, scope=None):
        '''
        Constructor
        '''
        self.proxies = scope_map[scope]

    def resolve(self, classname):
        if (classname in self.instances):
            return  self.instances[classname]
        if classname in self.proxies:
            inst = self.proxies[classname](self)
            self.instances[classname] = inst
            return inst
        else:
            raise KeyError(classname)
