derpconf
========

[![Build Status](https://secure.travis-ci.org/globocom/derpconf.png?branch=master)](http://travis-ci.org/globocom/derpconf)

derpconf abstracts loading configuration files for your app. derpconf was
extracted from [thumbor](http://github.com/globocom/thumbor/).

Intalling
---------

Installing derpconf is as easy as:

    pip install derpconf

Usage
-----

Using it is as simple as:

    from derpconf.config import Config

    conf = Config.load('/path/to/my/cfg.conf')

    assert conf.MY_KEY == 'MY_VALUE' # assuming there's a key called MY_KEY in
                                     # the configuration file.

Settings Defaults
-----------------

If you want to set default values for your configurations, just call:

    Config.define('MY-KEY', 'DEFAULT VALUE', 'Description for my key', 'Section')

The values that define gets are:

* the configuration key;
* the default value for that key if it's not found in the configuration file;
* the description for this key. This is very useful for generating
configuration file examples.
* the section that this key belongs to. Again very useful for generating
configuration file examples.

Generating Configuration Examples
---------------------------------

To generate a configuration example, you just need to call the
`get_config_text` method. Let's see an example:

    from derpconf.config import Config

    Config.define('foo', 'fooval', 'Foo is always a foo', 'FooValues')
    Config.define('bar', 'barval', 'Bar is not always a bar', 'BarValues')
    Config.define('baz', 'bazval', 'Baz is never a bar', 'BarValues')

    config_sample = Config.get_config_text()
    print config_sample # or instead of both, just call generate_config()

The following text will be print into the standard output:

    ################################## FooValues ###################################

    ## Foo is always a foo
    ## Defaults to: fooval
    #foo = 'fooval'

    ################################################################################


    ################################## BarValues ###################################

    ## Bar is not always a bar
    ## Defaults to: barval
    #bar = 'barval'

    ## Baz is never a bar
    ## Defaults to: bazval
    #baz = 'bazval'

    ################################################################################

A good sample of using derpconf can be seen at [thumbor's configuration
file](https://github.com/globocom/thumbor/blob/master/thumbor/config.py).

Verifying a Configuration File
------------------------------

derpconf includes a configuration file verifier. The purpose of this verifier
is to help you quickly understand what configuration files are missing what
keys and what values will be used for them instead.

Running it is as simple as including a call to `verify_config` in your
`config.py` file:

    verify_config(file_path)

Or you can leave it blank and derpconf will get the file path from `sys.argv`:

    verify_config()

The output of the verifier is something like this:

    Configuration "baz" not found in file /Users/bernardo/dev/derpconf/vows/fixtures/missing.conf. Using "bazval" instead.
    Configuration "foo" not found in file /Users/bernardo/dev/derpconf/vows/fixtures/missing.conf. Using "fooval" instead.
    Configuration "bar" not found in file /Users/bernardo/dev/derpconf/vows/fixtures/missing.conf. Using "barval" instead.

You can see it in use at [derpconf's code](https://github.com/globocom/derpconf/blob/master/derpconf/config.py).

License
-------

derpconf is licensed under the MIT License:

The MIT License

Copyright (c) 2012 globo.com timehome@corp.globo.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
