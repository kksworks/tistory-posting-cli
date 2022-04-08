import re
import sys
import pathlib
import json

from tools import tistory_api

def pre_proc(ctx_info, md_contents, **kwargs):
	if ctx_info['is_test_run'] == True :
		return md_contents

	# find pattern : [link_desc](link_name)
	chk_pattern = re.findall('\[(.+)\]\((.+)\)', md_contents)

	attach_info = {}
	try :
		with open(ctx_info['path_info']['attach_meta_file_path'], 'r', encoding='utf-8') as json_data:
			attach_info = json.load(json_data)
	except:
		None

	# for each pattern fix
	for md_link_info in chk_pattern :
		# local variable
		need_to_upload_attach_flag = False
		conv_md_syntax_file_name = ''
		attach_file_url_link = ''

		# save original pattern
		md_syntax_file_name = md_link_info[1]
		md_syntax_file_desc = md_link_info[0]
		original_attach_str = '[{md_syntax_file_desc}]({md_syntax_file_name})'.format(md_syntax_file_name=md_syntax_file_name, md_syntax_file_desc=md_syntax_file_desc)

		# for markdown caption plugin (picture caption setting)
		if len(md_syntax_file_desc) == 0 :
			md_syntax_file_desc = ' '

		# check exclude pattern... (url link skip...)
		for _chk_exclude_pattern in ctx_info['ini_config']['markdown']['attach_chk_exclude_pattern'] :
			need_to_upload_attach_flag = True
			if md_syntax_file_name.find(_chk_exclude_pattern) >= 0 :
				need_to_upload_attach_flag = False
				break
		if need_to_upload_attach_flag == False:
			continue

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
		if not str(real_file_path.suffix) in ctx_info['ini_config']['markdown']['attach_chk_include_pattern']:
			continue # not valid file extention ... skip attach 

		# load attach meta file and check info
		try : 
			attach_file_url_link = attach_info[md_syntax_file_name]['url']
		except : 
			attach_file_url_link = None

		# upload attach file to tistory server..
		if attach_file_url_link is None:
			try : 
				upload_ret = tistory_api.attach_data(ctx_info['cur_working_info']['blog_name'], ctx_info['ini_config']['tistory']['tistory_api_key'], real_file_path)
				assert upload_ret['tistory']['url'] is not None
				attach_file_url_link = upload_ret['tistory']['url']
				# upload success...
				attach_info[md_syntax_file_name] = {}
				attach_info[md_syntax_file_name]['url'] = attach_file_url_link
				# TODO: each file check md5sum (same file skip upload)
				with open(ctx_info['path_info']['attach_meta_file_path'], 'wt', encoding='utf-8') as json_file:
					json.dump(attach_info, json_file, indent="\t", ensure_ascii=False)
				ctx_info['loger'].dbg('tistory-file-attach plugin - upload success : {md_syntax_file_name}'.format(md_syntax_file_name=md_syntax_file_name))
			except Exception as e:
				# TODO: need to upload fail exception scenario
				# continue
				ctx_info['loger'].err('tistory-file-attach plugin - file upload fail.. :: ' + str(e))
				None

		if attach_file_url_link is not None:
			replace_attach_str = '[{md_syntax_file_desc}]({attach_file_url_link})'.format(attach_file_url_link=attach_file_url_link, md_syntax_file_desc=md_syntax_file_desc)
		else :
			replace_attach_str = '[ERROR] !!! auto upload fail - check markdown'

		md_contents = md_contents.replace(original_attach_str, replace_attach_str)
		# log_tool.dbg(self.md_contents)
	return md_contents

def post_proc(ctx_info, html_contents, **kwargs):
	return html_contents

