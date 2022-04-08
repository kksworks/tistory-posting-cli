#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import click
import pathlib
import proc_api


cur_working_dir = str(pathlib.Path(__file__).resolve().parent)

@click.group()
def cli():
    pass


@click.command()
# @click.option('--test', is_flag=True, default=False, help='test run (not publish) - verbos test mode')
@click.argument('filename', type = click.Path(exists=True))
def publish(filename):
	""" markdown publish tool for tistory webpage"""
	# check argument
	if filename is None:
		raise click.ClickException('invalid arguments')

	try :
		proc_api.publish_post(filename)
	except Exception as e: 
		raise click.ClickException('command fail : ' + str(e))

@click.command()
@click.option('--category', '-c', is_flag=True, default=False, help='get category info (save to json file)')
@click.argument('blogname', type = str)
def get_info(category, blogname) :
	"""get tistory info"""
	if category == True :
		proc_api.get_category_info(blogname)

#  ./tistory_posting_cli.py get-info -c xenoserver

cli.add_command(publish)
cli.add_command(get_info)
if __name__ == '__main__':
    cli()