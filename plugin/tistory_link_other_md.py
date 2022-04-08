import re
import sys
import pathlib
import json

from tools import markdownConv

def pre_proc(ctx_info, md_contents, **kwargs):
	if ctx_info['is_test_run'] == True :
		return md_contents

	# find pattern : [link_desc](link_name)
	chk_pattern = re.findall('\[(.+)\]\((.+)\)', md_contents)

	for md_link_info in chk_pattern :

		# save original pattern
		md_syntax_file_name = md_link_info[1]
		md_syntax_file_desc = md_link_info[0]
		original_attach_str = '[{md_syntax_file_desc}]({md_syntax_file_name})'.format(md_syntax_file_name=md_syntax_file_name, md_syntax_file_desc=md_syntax_file_desc)

		# file path fix for each platform
		if sys.platform == 'win32':
			conv_md_syntax_file_name = md_syntax_file_name.replace('/','\\')
		else :
			conv_md_syntax_file_name = md_syntax_file_name.replace('\\','/')

		# make real file path and valid file extention
		# - TODO: support specific attach folder (ctx_info)
		real_file_path = pathlib.Path(pathlib.PurePath(ctx_info['cur_working_info']['cur_abpath_folder'], conv_md_syntax_file_name))
		if not real_file_path.exists() and real_file_path.is_file() :
			continue # not file ... skip attach 
		if not str(real_file_path.suffix) in '.md':
			continue # not valid file extention ... skip attach 

		ctx_info['loger'].dbg('tistory-link-other-md plugin - link file..')

		try : 
			mdConv_ctx = markdownConv.markdownConv(md_file_path = real_file_path)
			md_meta = mdConv_ctx.get_md_meta()
		
			post_url_link = md_meta['tistory']['auto_gen']['url']
			post_title = md_meta['tistory']['title']
			
			replace_attach_str = '[{post_title}]({post_url_link})'.format(post_url_link=post_url_link, post_title=post_title)
		except :
			replace_attach_str = '해당 포스팅 작성중 입니다.'

		md_contents = md_contents.replace(original_attach_str, replace_attach_str)

	# find pattern : [link_desc](link_name)
	# chk_pattern = re.findall('\[(.+)\]\((.+)\)', md_contents)\
	return md_contents

def post_proc(config, html_contents, **kwargs):
	return html_contents
