#!/usr/bin/python
# -*- coding: utf-8 -*-

# derpconf
# https://github.com/globocom/derpconf

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2012 globo.com timehome@corp.globo.com

import os
from os.path import abspath, join, dirname
from collections import defaultdict

from pyvows import Vows, expect

from derpconf.config import Config, ConfigurationError

fix = lambda name: abspath(join(dirname(__file__), 'fixtures', name))


@Vows.batch
class Configuration(Vows.Context):
    class WhenLoading(Vows.Context):
        class WhenFileDoesNotExist(Vows.Context):
            def topic(self):
                err = expect.error_to_happen(ConfigurationError)

                with err:
                    Config.load(fix('not-existent.conf'))

                return err

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

        class WhenPathIsDirectory(Vows.Context):
            def topic(self):
                return Config.load(fix('conf.d'), defaults={
                    'PROPER': 'PROPERVALUE'
                })

            def should_have_default_value(self, topic):
                expect(topic.PROPER).to_equal('PROPERVALUE')

            def should_have_overridden_value(self, topic):
                expect(topic.FOO).to_equal('override')

            def should_have_new_value(self, topic):
                expect(topic.NEW).to_equal('thing')

            def should_not_have_lower_case_value(self, topic):
                expect(hasattr(topic, 'baz')).to_be_false()

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

    class WhenVerifying(Vows.Context):
        def topic(self):
            class SpecialConfig(Config):
                class_defaults = {}
                class_group_items = defaultdict(list)
                class_groups = []
                class_descriptions = {}

            SpecialConfig.define('some_key', 'default', 'test key')

            return SpecialConfig.verify(fix('missing.conf'))

        def should_be_lengthy(self, topic):
            expect(topic).to_length(1)

    class WhenUsedAsDict(Vows.Context):
        def topic(self):
            return Config.load(fix('sample.conf'))

        def should_have_get_value_as_dict(self, topic):
            expect(topic['FOO']).to_equal('bar')

        def should_have_set_value_as_dict(self, topic):
            topic['X'] = 'something'
            expect(topic['X']).to_equal('something')

        class WithError(Vows.Context):
            def topic(self, parent_topic):
                err = expect.error_to_happen(KeyError)

                with err:
                    parent_topic['INVALID_KEY']

                return err

            def should_raise_key_error(self, topic):
                expect(topic).to_be_an_error_like(KeyError)

    class WhenGetDescription(Vows.Context):
        def topic(self):
            Config.define('some_key', 'default', 'test key')

            return Config.load(fix('missing.conf'))

        def should_have_description(self, topic):
            expect(topic.get_description('some_key')).to_equal('test key')


    class WhenEnvironmentVariablesIsDisabled(Vows.Context):
        def topic(self):
            Config._allow_environment_variables = False
            config = Config.load(fix('sample.conf'))

            try:
                os.environ['FOO'] = "baz"

                return config.FOO
            finally:
                del os.environ['FOO']

        def should_be_equal_to_env(self, topic):
            expect(topic).to_equal("bar")

    class WhenGettingFromEnvironment(Vows.Context):
        class WhenKeyDoesNotExistInConfiguration(Vows.Context):
            def topic(self):
                os.environ['SOME_CONFIGURATION'] = "test value"
                config = Config()

                Config.allow_environment_variables()

                return config.SOME_CONFIGURATION

            def should_be_equal_to_env(self, topic):
                expect(topic).to_equal("test value")


        class WhenKeyExistsInConfigurationFile(Vows.Context):
            def topic(self):
                config = Config.load(fix('sample.conf'))
                Config.allow_environment_variables()

                try:
                    os.environ['FOO'] = "baz"

                    return config.FOO
                finally:
                    del os.environ['FOO']

            def should_be_equal_to_env(self, topic):
                expect(topic).to_equal("baz")

    class WhenReloading(Vows.Context):
        def topic(self):
            class SpecialConfig(Config):
                class_defaults = {}
                class_group_items = defaultdict(list)
                class_groups = []
                class_descriptions = {}

            config = SpecialConfig.load(fix('sample.conf'), defaults={
                'PROPER': 'PROPERVALUE'
            })

            SpecialConfig.define('UBERFOO', 'baz', 'something', 'else')

            config.reload()

            return config

        def should_have_uberfoo(self, topic):
            expect(hasattr(topic, 'UBERFOO')).to_be_true()
            expect(topic.UBERFOO).to_equal('baz')

    class WhenGeneratingConfig(Vows.Context):
        def topic(self):
            class SpecialConfig(Config):
                class_defaults = {}
                class_group_items = defaultdict(list)
                class_groups = []
                class_descriptions = {}

            SpecialConfig.define(
                'SOME_TUPLE_VAR',
                ('foo', 'bar'),
                'Tuple var from config',
                'some config'
            )

            text = SpecialConfig.get_config_text()

            return text.split('\n')

        def should_have_uberfoo(self, topic):
            expect(topic).to_equal([
                '################################# some config ##################################',
                '',
                '## Tuple var from config',
                '## Defaults to: (',
                "#    'foo',",
                "#    'bar',",
                '#)',
                '',
                '#SOME_TUPLE_VAR = (',
                "#    'foo',",
                "#    'bar',",
                '#)',
                '',
                '',
                '################################################################################',
                '',
                ''
            ])
