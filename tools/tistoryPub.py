import configparser
import pathlib
import importlib 
import json

from tools import logTool
from tools import etc_tools
from tools import markdownConv
from tools import tistory_api


# -------------------------
# prgram settings
# -------------------------
CONFIG_FILE_NAME = 'config.ini'  # config file path
META_FILE__DIR_PATH = 'meta' # front metter info
META_FILE__ATTACH = 'tistory-attach.json'
META_FILE__CATEGORY = 'tistory-category.json'
HTML_TMP__DIR_PATH = 'html_tmp'
AUTO_GEN_META_KEY = ['tistory', 'auto_gen'] # auto gen front metter key
DEFAULT_CATEGORY_ID = 0 # default post category id


class tistoryPub():
	_mdparser_plugin = []
	ctx_info = {}

	def __init__(self, base_dir, test_run=False) :
		self._base_dir = str(base_dir)
		self._config_parse(pathlib.PurePath(base_dir, CONFIG_FILE_NAME))
		self.ctx_info['is_test_run'] = test_run

	def _config_parse(self, config_file_path) :
		# load default config from ini file..
		config = configparser.ConfigParser()
		config.read(config_file_path, encoding='utf-8')

		self.ctx_info['ini_config'] = config._sections

		# [load from config file] : check valid config
		#  - TODO: valid config file....
		try:
			assert self.ctx_info['ini_config']['tistory']['tistory_api_key'] is not None

			assert self.ctx_info['ini_config']['markdown']['folder_chk_exclude_pattern'] is not None
			assert self.ctx_info['ini_config']['markdown']['attach_chk_include_pattern'] is not None
			assert self.ctx_info['ini_config']['markdown']['attach_chk_exclude_pattern'] is not None
			# assert self.ctx_info['ini_config']['markdown']['attach_retry_cnt'] is not None

			assert self.ctx_info['ini_config']['log']['log_to_file_path'] is not None
			assert self.ctx_info['ini_config']['log']['log_file_max_size_kb'] is not None
			assert self.ctx_info['ini_config']['log']['log_level'] is not None
			
			assert self.ctx_info['ini_config']['md_parser_plugin']is not None

		except Exception as e:
			print('invlid ini config : ' + e)
			exit(1)
		
		# [load from config file] : log setting 
		self.loger = logTool.logTool('tistoryPoting', self.ctx_info['ini_config']['log']['log_level'], self.ctx_info['ini_config']['log']['log_to_file_path'], int(self.ctx_info['ini_config']['log']['log_file_max_size_kb']))
		self.loger.dbg('logger setting success...')
		self.ctx_info['loger'] = self.loger

		# self.ctx_info['ini_config']['tistory']['auto_gen_meta_key'] = self.ctx_info['ini_config']['tistory']['auto_gen_meta_key'].replace(' ','').split(',')

		# [load from config file] : markdown parser setting 
		self.ctx_info['ini_config']['markdown']['folder_chk_exclude_pattern'] = self.ctx_info['ini_config']['markdown']['folder_chk_exclude_pattern'].replace(' ','').split(',')
		self.ctx_info['ini_config']['markdown']['attach_chk_include_pattern'] = self.ctx_info['ini_config']['markdown']['attach_chk_include_pattern'].replace(' ','').split(',')
		self.ctx_info['ini_config']['markdown']['attach_chk_exclude_pattern'] = self.ctx_info['ini_config']['markdown']['attach_chk_exclude_pattern'].replace(' ','').split(',')

		# [load from config file] : markdown parser plugin
		for md_parser_plugin_one in self.ctx_info['ini_config']['md_parser_plugin'].items() :
			if md_parser_plugin_one[1] == 'true' :
				self._mdparser_plugin.append(importlib.import_module('plugin.' + md_parser_plugin_one[0]))

		# [generate config] : generate config for running proc
		self.ctx_info['path_info'] = {}
		self.ctx_info['path_info']['base_dir'] = self._base_dir
		self.ctx_info['path_info']['meta_dir'] = str(pathlib.PurePath(self._base_dir, META_FILE__DIR_PATH))
		self.ctx_info['path_info']['html_tmp'] = str(pathlib.PurePath(self._base_dir, HTML_TMP__DIR_PATH))
		self.ctx_info['path_info']['attach_meta_file_path'] = str(pathlib.PurePath(self.ctx_info['path_info']['meta_dir'], META_FILE__ATTACH))
		self.ctx_info['path_info']['category_meta_file_path'] = str(pathlib.PurePath(self.ctx_info['path_info']['meta_dir'], META_FILE__CATEGORY))
		
		# make sub folder
		pathlib.Path(self.ctx_info['path_info']['meta_dir']).mkdir(exist_ok=True, parents=True)
		pathlib.Path(self.ctx_info['path_info']['html_tmp']).mkdir(exist_ok=True, parents=True)


	def _md_pre_proc(self, md_contents) :
		# ad-nomotion fix for obsidian plugin
		for pre_proc in self._mdparser_plugin :
			try :
				md_contents = pre_proc.pre_proc(self.ctx_info, md_contents)
			except Exception as e: 
				self.loger.err('plug-in {plugin_name} proc fail..'.format(plugin_name=str(pre_proc)))
				self.loger.err(e)
				continue
		return md_contents


	def _html_post_proc(self, html_contents) :
		# ad-nomotion fix for obsidian plugin
		for post_proc in self._mdparser_plugin :
			try :
				html_contents = post_proc.post_proc(self.ctx_info['ini_config'], html_contents)
			except :
				self.loger.err('plug-in {plugin_name} proc fail..'.format(plugin_name=str(post_proc)))
				continue
		return html_contents

	def publish_one_post(self, tareget_file) :
		self.loger.info('one post publish : [{tareget_file}]'.format(tareget_file=tareget_file))

		# make current edit file info.
		self.ctx_info['cur_working_info'] = {}
		self.ctx_info['cur_working_info']['cur_abpath_file'] = str(pathlib.PurePath(str(pathlib.Path(tareget_file).resolve())))
		self.ctx_info['cur_working_info']['cur_file_name'] = str(pathlib.PurePath(tareget_file).stem)
		self.ctx_info['cur_working_info']['cur_abpath_folder'] = str(pathlib.PurePath(self.ctx_info['cur_working_info']['cur_abpath_file']).parent)

		# load markdown with parser
		mdConv_ctx = markdownConv.markdownConv(md_file_path = self.ctx_info['cur_working_info']['cur_abpath_file'], md5_meta_dic_key = AUTO_GEN_META_KEY)
		md_contents = mdConv_ctx.get_md_contents()
		md_meta = mdConv_ctx.get_md_meta()

		# check essentail meta data..
		try :
			assert md_meta['tistory']['publish'] is not None
			assert md_meta['tistory']['blog_name'] is not None
			assert md_meta['tistory']['category'] is not None
			assert md_meta['tistory']['title'] is not None
			assert md_meta['tistory']['tags'] is not None
			# update curent file info
			self.ctx_info['cur_working_info']['blog_name'] = md_meta['tistory']['blog_name']
		except :
			self.loger.err('essentail meta info missing.. nothing TODO... bye bye..')
			return None

		# if no pub option

		if  md_meta['tistory']['publish'] == False:
			self.loger.dbg('skip publish : no publish target')
			return False

		# is file modified check
		try :
			if md_meta['tistory']['force_chk'] == False and mdConv_ctx.post_is_modified() is False :
				self.loger.info('skip publish : not modified - nothing TODO... bye bye..')
				return True
		except : 
			if mdConv_ctx.post_is_modified() is False :
				self.loger.info('skip publish : not modified - nothing TODO... bye bye..')
				return True

		self.loger.info('markdown convert start..')

		# load plug-in : pre processing for markdown contents
		md_contents = self._md_pre_proc(md_contents)

		# html convert ...
		md_conv_html = mdConv_ctx.convert_md_to_html(md_contents)['html']

		# load plug-in : post processing for html contents
		md_conv_html = self._html_post_proc(md_conv_html)

		# publish start...
		self.loger.dbg('publish start.. [{tareget_file}]'.format(tareget_file=tareget_file))

		# get post id (edit or new post)
		try :
			post_id = md_meta['tistory']['auto_gen']['post_id']
			assert tistory_api.read_post(md_meta['tistory']['blog_name'], 
										self.ctx_info['ini_config']['tistory']['tistory_api_key'],
										post_id ) is not None
			self.loger.info('exist post id : update post ')
		except :
			self.loger.info('not exist post id : new post')
			post_id = None

		# write post...
		try :
			category_id = self._category_convert_to_id(md_meta['tistory']['blog_name'], md_meta['tistory']['category'])
			write_ret = None
			if self.ctx_info['is_test_run'] == False :
				write_ret = tistory_api.write_post(	md_meta['tistory']['blog_name'],
													self.ctx_info['ini_config']['tistory']['tistory_api_key'],
													md_meta['tistory']['title'],
													md_conv_html,
													category_id,
													md_meta['tistory']['tags'],
													post_id=post_id)
			assert write_ret is not None 
		except Exception as e:
			self.loger.err('tistory publish fail.. : publish api')
			self.loger.err('  -> ' + e)
			return False

		# save html results.
		try : 
			html_save_option = int(md_meta['tistory']['save_conv_html'])
		except : 
			html_save_option = int(self.ctx_info['ini_config']['markdown']['save_conv_html'])

		try : 
			if html_save_option == 0 : # do nothing
				target_file_path = None
			elif html_save_option == 1 : # 1 : md same path
				save_path = self.ctx_info['cur_working_info']['cur_abpath_folder'] 
				html_name = self.ctx_info['cur_working_info']['cur_file_name'] + '.html'
				target_file_path = pathlib.PurePath(save_path, html_name)
			elif html_save_option == 2 : # 2 : html tmp path
				save_path = self.ctx_info['path_info']['html_tmp']
				html_name = self.ctx_info['cur_working_info']['cur_file_name'] + '.html'
				target_file_path = pathlib.PurePath(save_path, html_name)
			with open(target_file_path, 'w', encoding='utf-8') as html_file:
				self.loger.dbg('save to html : {target_file_path}'.format(target_file_path=target_file_path))
				html_file.write(md_conv_html)
		except :
			None

		try :
			md_meta['tistory']['auto_gen']['url'] = write_ret['tistory']['url']
			md_meta['tistory']['auto_gen']['post_id'] = write_ret['tistory']['postId']

			mdConv_ctx.set_md_meta(md_meta)
			mdConv_ctx.dump_md_file()
			self.loger.info('tistory publish success')
		except Exception as e:
			self.loger.err('tistory publish fail.. : save meta info')
			self.loger.err('  -> ' + e)
		None

	def update_dir_recursive(self, target_dir) :
		self.loger.info('search dir... [{target_dir}]'.format(target_dir=target_dir))

		target_files = etc_tools.get_fileinfo_from_folder(target_dir, '*.md', self.ctx_info['ini_config']['markdown']['folder_chk_exclude_pattern'])
		for target_file in target_files : 
			self.publish_one_post(target_file['abpath_full'])

	def update_category_info(self, blog_name) :
		self.loger.info('update category : [{blog_name}]'.format(blog_name=blog_name))
		attach_info = {}
		target_attach_file = self.ctx_info['path_info']['category_meta_file_path']

		try :
			with open(target_attach_file, 'r', encoding='utf-8') as json_data:
				attach_info = json.load(json_data)
			assert attach_info[blog_name] is not None
		except:
			attach_info[blog_name] = {}

		try	:
			# load from tistory category
			cur_category_dic = tistory_api.get_blog_category(blog_name, self.ctx_info['ini_config']['tistory']['tistory_api_key'])
			assert cur_category_dic is not None
			self.loger.dbg('get category success : get category count : [{length}]'.format(length=len(cur_category_dic)))
			with open(target_attach_file, 'w', encoding='utf-8') as json_file:
				self.loger.info('update category : save to file [{target_attach_file}]'.format(target_attach_file=target_attach_file))
				attach_info[blog_name] = cur_category_dic
				json.dump(attach_info, json_file, indent="\t", ensure_ascii=False, sort_keys=False)
			return attach_info
		except :
			self.loger.err('update category fail..')
			return None


	def _category_convert_to_id(self, blog_name, category_id) :
		category_info = {}
		category_info_file = self.ctx_info['path_info']['category_meta_file_path']
		
		try :
			with open(category_info_file, 'r', encoding='utf-8') as json_data:
				category_info = json.load(json_data)
			assert category_info[blog_name] is not None
		# load category info
		except :
			category_info = self.update_category_info(blog_name)
			
		try :
			# get from category name
			for category_dic in category_info[blog_name] : 
				if category_dic['name'] == category_id :
					return category_dic['id']

			# get from category id (number)
			for category_dic in category_info[blog_name] : 
				if category_dic['id'] == str(category_id) :
					return category_dic['id']
			return '0' # default category
		except:
			return '0' # default category

if __name__ == "__main__":
	None
