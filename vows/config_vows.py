#!/usr/bin/python
# -*- coding: utf-8 -*-

# derpconf 
# https://github.com/globocom/derpconf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 globo.com timehome@corp.globo.com

from os.path import abspath, join, dirname

from pyvows import Vows, expect

from derpconf.config import Config, ConfigurationError

fix = lambda name: abspath(join(dirname(__file__), 'fixtures', name))

@Vows.batch
class Configuration(Vows.Context):
    class WhenLoading(Vows.Context):
        class WhenFileDoesNotExist(Vows.Context):
            def topic(self):
                Config.load(fix('not-existent.conf'))

            def should_be_an_error(self, topic):
                expect(topic).to_be_an_error()
                expect(topic).to_be_an_error_like(ConfigurationError)

        class WhenFileExists(Vows.Context):
            def topic(self):
                return Config.load(fix('sample.conf'), defaults={
                    'PROPER': 'PROPERVALUE'
                })

            def should_have_default_value(self, topic):
                expect(topic.PROPER).to_equal('PROPERVALUE')

            def should_have_set_value(self, topic):
                expect(topic.FOO).to_equal('bar')

            def should_not_have_lower_case_value(self, topic):
                expect(hasattr(topic, 'baz')).to_be_false()

        class WhenPathIsNone(Vows.Context):
            class AndConfNameExists(Vows.Context):
                def topic(self):
                    return Config.load(None, conf_name='sample.conf', lookup_paths=['vows/fixtures/'])

                def should_have_set_value(self, topic):
                    expect(topic.FOO).to_equal('bar')

            class AndConfNameDoesNotExist(Vows.Context):
                def topic(self):
                    return Config.load(
                        None, conf_name='not-existent.conf',
                        lookup_paths=['vows/fixtures/'],
                        defaults={'DEFAULT': 'DEFAULTVALUE'}
                    )

                def should_have_default_values(self, topic):
                    expect(topic.DEFAULT).to_equal('DEFAULTVALUE')

            class AndConfNameIsNone(Vows.Context):
                def topic(self):
                    return Config.load(None, defaults={'DEFAULT': 'DEFAULTVALUE'})

                def should_have_default_values(self, topic):
                    expect(topic.DEFAULT).to_equal('DEFAULTVALUE')

    class WhenSettingAnAlias(Vows.Context):

        def topic(self):
            Config.alias('OTHER_ENGINE', 'ENGINE')
            return Config(OTHER_ENGINE='x')

        def should_set_engine_attribute(self, config):
            expect(config.ENGINE).to_equal('x')

        def should_set_other_engine_attribute(self, config):
            expect(config.OTHER_ENGINE).to_equal('x')

    class WhenSettingAnAliasedKey(Vows.Context):
        def topic(self):
            Config.alias('LOADER_ALIAS', 'LOADER')
            return Config(LOADER='y')

        def should_set_loader_attribute(self, config):
            expect(config.LOADER).to_equal('y')

        def should_set_loader_alias_attribute(self, config):
            expect(config.LOADER_ALIAS).to_equal('y')

    class WithAliasedAliases(Vows.Context):
        def topic(self):
            Config.alias('STORAGE_ALIAS', 'STORAGE')
            Config.alias('STORAGE_ALIAS_ALIAS', 'STORAGE_ALIAS')
            return Config(STORAGE_ALIAS_ALIAS='z')

        def should_set_storage_attribute(self, config):
            expect(config.STORAGE).to_equal('z')

        def should_set_storage_alias_attribute(self, config):
            expect(config.STORAGE_ALIAS).to_equal('z')

        def should_set_storage_alias_alias_attribute(self, config):
            expect(config.STORAGE_ALIAS_ALIAS).to_equal('z')

        class WithDefaultValues(Vows.Context):
            def topic(self):
                return Config()

