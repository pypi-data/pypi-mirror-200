#!/usr/bin/python

# Copyright (C) 2023 Ernesto Lanchares <elancha98@gmail.com>
# 
# This file is part of ebib.
# 
# ebib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3
# of the License, or (at your option) any later version.
#
# ebib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with ebib. If not, see <https://www.gnu.org/licenses/>.

import click
from ebib import add

@click.command()
def webpage():
	print('building webpage...')

@click.command()
def add_tag():
	pass


@click.group(help='CLI tool for bibliography manager integrated with git.')
def cli():
	pass

cli.add_command(webpage)
cli.add_command(add_tag)
cli.add_command(add)

if __name__ == '__main__':
	cli()
