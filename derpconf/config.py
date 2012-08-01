#!/usr/bin/python
# -*- coding: utf-8 -*-

# derpconf 
# https://github.com/globocom/derpconf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 globo.com timehome@corp.globo.com

import logging
from collections import defaultdict
from os.path import join, exists, abspath
import imp

from textwrap import fill

class ConfigurationError(RuntimeError):
    pass

class Config(object):
    class_defaults = {}
    class_group_items = defaultdict(list)
    class_groups = []
    class_descriptions = {}

    class_aliases = defaultdict(list)
    class_aliased_items = {}

    @classmethod
    def define(cls, key, value, description, group='General'):
        cls.class_defaults[key] = value
        cls.class_descriptions[key] = description
        cls.class_group_items[group].append(key)
        if not group in cls.class_groups:
            cls.class_groups.append(group)

    @classmethod
    def alias(cls, new_key, aliased_key):
        if aliased_key in cls.class_aliased_items:
            aliased_key = cls.class_aliased_items[aliased_key]
        cls.class_aliases[aliased_key].append(new_key)
        cls.class_aliased_items[new_key] = aliased_key

    @classmethod
    def get_conf_file(cls, conf_name, lookup_paths):
        for conf_path in lookup_paths:
            conf_path_file = abspath(join(conf_path, conf_name))
            if exists(conf_path_file):
                return conf_path_file

        raise ConfigurationError('%s file not passed and not found on the lookup paths %s' % (conf_name, lookup_paths))

    @classmethod
    def load(cls, path, conf_name=None, lookup_paths=[], defaults={}):
        if path is None and conf_name is not None and lookup_paths:
            path = cls.get_conf_file(conf_name, lookup_paths)

        if not exists(path):
            raise ConfigurationError('Configuration file not found at path %s' % path)

        with open(path) as config_file:
            name='configuration'
            code = config_file.read()
            module = imp.new_module(name)
            exec code in module.__dict__

            conf = cls(defaults=defaults)
            conf.config_file = path
            for name, value in module.__dict__.iteritems():
                if name.upper() == name:
                    setattr(conf, name, value)

            return conf

    def __init__(self, **kw):
        if 'defaults' in kw:
            self.defaults = kw['defaults']

        for key, value in kw.iteritems():
            setattr(self, key, value)

    def validates_presence_of(self, *args):
        for arg in args:
            if not hasattr(self, arg):
                raise ConfigurationError('Configuration %s was not found and does not have a default value. Please verify your thumbor.conf file' % arg)

    def get(self, name, default=None):
        if hasattr(self, name):
            return getattr(self, name)
        return default

    def __setattr__(self, name, value):
        if name in Config.class_aliased_items:
            logging.warn('Option %s is marked as deprecated please use %s instead.' % (name, Config.class_aliased_items[name]))
            self.__setattr__(Config.class_aliased_items[name], value)
        else:
            super(Config, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]

        if name in Config.class_aliased_items:
            logging.warn('Option %s is marked as deprecated please use %s instead.' % (name, Config.class_aliased_items[name]))
            return self.__getattr__(Config.class_aliased_items[name])

        if 'defaults' in self.__dict__ and name in self.__dict__['defaults']:
            return self.__dict__['defaults'][name]

        if name in Config.class_defaults:
            return Config.class_defaults[name]

        raise AttributeError(name)

def generate_config():
    MAX_LEN = 80
    SEPARATOR = '#'
    for group in Config.class_groups:
        keys = Config.class_group_items[group]
        sep_size = int(round((MAX_LEN - len(group)) / 2, 0)) - 1
        group_name = SEPARATOR * sep_size + ' ' + group + ' ' + SEPARATOR * sep_size
        if len(group_name) < MAX_LEN:
            group_name += SEPARATOR
        print group_name
        for key in keys:
            print
            value = Config.class_defaults[key]
            description = Config.class_descriptions[key]

            wrapped = fill(description, width=78, subsequent_indent='## ')

            print '## %s' % wrapped
            if key in Config.class_aliases:
                print '## Aliases: %s' % ', '.join(Config.class_aliases[key])
            print '## Defaults to: %s' % value
            print '#%s = %s' % (key, format_value(value))
        print
        print SEPARATOR * MAX_LEN
        print
        print

def format_value(value):
    if isinstance(value, basestring):
        return "'%s'" % value
    if isinstance(value, (tuple, list, set)):
        representation = '[\n'
        for item in value:
            representation += '#    %s' % item
        representation += '#]'
        return representation
    return value

if __name__ == '__main__':
    generate_config()
