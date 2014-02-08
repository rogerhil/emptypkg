# Empty Package Pip for Python
# Copyright (C) 2013 Rogerio Hilbert Lima <rogerhil@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import os
import optparse


BASE_PATH = os.path.dirname(__file__)
TEMPLATES_PATH = os.path.abspath(os.path.join(BASE_PATH, '../templates'))


class EmptyPkgExcetion(Exception):
    pass


class Template(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.path, self.filename = os.path.split(filepath)
        self.load_content()

    def load_content(self):
        self.content = ''
        with open(self.filepath) as afile:
            self.content = afile.read()

    def render(self, data):
        return self.content % data

    def render_and_save(self, data, path):
        content = self.render(data)
        filepath = os.path.join(path, self.filename)
        with open(filepath, 'w') as afile:
            afile.write(content)


class EmptyPkg(object):

    def __init__(self, *args):
        self.args = args
        self.parser = None
        self.options = None
        self.argv = None
        self.destiny_path = None
        self._is_valid = False

    def build_parser(self, *args):
        self.parser = optparse.OptionParser()
        group = optparse.OptionGroup(self.parser, 'General')
        group.add_option('-n', '--name',
                         action="store",
                         dest="name",
                         help='Package Name')
        group.add_option('-d', '--description',
                         action="store",
                         dest="description",
                         help='Package Description')
        self.parser.add_option_group(group)
        self.options, self.argv = self.parser.parse_args(*args)
        if len(self.argv) < 2 or not os.path.isdir(self.argv[1]):
            raise EmptyPkgExcetion('No such directory %s' % self.argv)
        self.destiny_path = self.argv[1]

    def is_valid(self):
        try:
            self.build_parser(*self.args)
        except EmptyPkgExcetion, err:
            return False, str(err)
        self._is_valid = True
        return True, ''

    @property
    def data(self):
        data = dict(
            PACKAGE_NAME=self.options.name,
            PACKAGE_DESCRIPTION=self.options.description
        )
        return data

    def build(self):
        if not self._is_valid:
            raise EmptyPkgExcetion("Must be first validated")
        dest = os.path.join(self.destiny_path, self.options.name)
        os.makedirs(dest)
        for filename in os.listdir(TEMPLATES_PATH):
            filepath = os.path.join(TEMPLATES_PATH, filename)
            template = Template(filepath)
            template.render_and_save(self.data, dest)
