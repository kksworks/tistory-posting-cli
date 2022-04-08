import re
import pathlib
import hashlib

import markdown
import frontmatter
import traceback

# pip install markdown
# pip install python-frontmatter
# pip install markdown-captions


class markdownConv() :
	_md_contents_meta_loaded_hash = ''
	_md_contents_cur_hash = '-2'
	_is_modified = None

	def __init__(self, md_file_path=None, md5_meta_dic_key=None) :
		self._md_file_path = md_file_path

		try :
			# load md file
			with open(self._md_file_path, encoding='utf-8') as f:
				self._md_parser_ctx = frontmatter.load(f)
			
			# make metainfo key
			self._md5_meta_dic_key = self._md_parser_ctx.metadata
			if md5_meta_dic_key is not None :
				for key_name in md5_meta_dic_key :
					if key_name not in self._md5_meta_dic_key:
						self._md5_meta_dic_key[key_name] = {}
					self._md5_meta_dic_key = self._md5_meta_dic_key[key_name]

			self._first_chk_contents()
		except Exception as e: 
			print(e)
			raise Exception("cannot md file :{md_file_path}".format(md_file_path=md_file_path))

	def _first_chk_contents(self) :
		# check modified
		try :
			self._md_contents_meta_loaded_hash = self._md5_meta_dic_key['md_contents_hash']
		except :
			# not exist meta info. create hash
			self._md5_meta_dic_key['md_contents_hash'] = {}

		# md5sum get md5sum hash
		self._md_contents_cur_hash = self._get_file_md5_hash(self._md_parser_ctx.content)

		# is modfied chk
		if self._md_contents_meta_loaded_hash == self._md_contents_cur_hash :
			self._is_modified = False
		else :
			self._is_modified = True


	def _get_file_md5_hash(self, input_str) :
		return str(hashlib.md5(input_str.encode()).hexdigest())

	def _update_contents_md5(self) :
		self._md5_meta_dic_key['md_contents_hash'] = self._get_file_md5_hash(self._md_parser_ctx.content)

	def post_is_modified(self):
		return self._is_modified

	def get_md_contents(self) :
		return self._md_parser_ctx.content

	def set_md_contents(self, md_contents) :
		self._md_parser_ctx.content = md_contents

	def get_md_meta(self) :
		return self._md_parser_ctx.metadata

	def set_md_meta(self, md_meta) :
		self._md_parser_ctx.metadata = md_meta

	def convert_md_to_html(self, md_contents=None) :
		md = markdown.Markdown(extensions=['markdown.extensions.fenced_code', 'markdown.extensions.meta', 'markdown.extensions.attr_list', 'markdown_captions', 'tables', 'markdown.extensions.toc', 'markdown.extensions.admonition'], tab_length=2)

		md_conv_html = {}
		if md_contents is None :
			md_contents = self._md_parser_ctx.content

		md_conv_html['html'] = md.convert(md_contents)
		md_conv_html['meta'] = self._md_parser_ctx.metadata

		return md_conv_html

	def dump_md_file(self) :
		self._update_contents_md5()
		# post = frontmatter.load(self._md_file_path)
		# post.metadata = meta_info
		frontmatter.dump(self._md_parser_ctx, self._md_file_path)


if __name__ == "__main__":
	None