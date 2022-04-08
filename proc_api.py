#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pathlib

from tools import tistoryPub
cur_working_dir = str(pathlib.Path(__file__).resolve().parent)

def get_category_info(blogname) :
	tistoryPub_ctx = tistoryPub.tistoryPub(cur_working_dir)
	tistoryPub_ctx.update_category_info(blogname)

def publish_post(filename) :
	tistoryPub_ctx = tistoryPub.tistoryPub(cur_working_dir)

	if pathlib.Path(filename).is_dir() :
		tistoryPub_ctx.update_dir_recursive(filename)
	else :
		tistoryPub_ctx.publish_one_post(filename)

if __name__ == '__main__':
	# get_category_info('xenostudy')
	# publish_post('./test_sample/test_case-base-md.md')
	# publish_post('./test_sample/test_case-attach-img.md')
	# publish_post('./test_sample/test_case-link-other-md.md')
	publish_post('./test_sample')

