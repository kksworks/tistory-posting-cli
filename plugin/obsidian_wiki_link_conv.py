
# def _conv_wiki_syntax_to_md(self, md_contents) :
# 	# [[파일네임|링크네임]]
# 	attach_pattern = re.findall('\[\[(.+)\|(.+)\]\]', md_contents)
# 	for md_attach_info in attach_pattern :
# 		real_file_name = md_attach_info[0]
# 		desc = md_attach_info[1]
# 		# log_tool.dbg(md_attach_info[0]) # real_file_name
# 		# log_tool.dbg(md_attach_info[1]) # desc
# 		find_str = '[[{real_file_name}|{desc}]]'.format(real_file_name=real_file_name, desc=desc)
# 		replace_str = '[{desc}]({real_file_name})'.format(real_file_name=real_file_name, desc=desc)
# 		md_contents = md_contents.replace(find_str,replace_str)
#
# 	# [[파일네임]]
# 	attach_pattern = re.findall('\[\[(.+)\]\]', md_contents)
# 	for md_attach_info in attach_pattern :
# 		# log_tool.dbg(md_attach_info[0]) # real_file_name
# 		real_file_name = md_attach_info
# 		desc = ' '
# 		find_str = '[[{real_file_name}]]'.format(real_file_name=real_file_name)
# 		replace_str = '[{desc}]({real_file_name})'.format(real_file_name=real_file_name, desc=desc)
# 		md_contents = md_contents.replace(find_str,replace_str)
#
# 	return md_contents

def pre_proc(config, md_contents, **kwargs):
	return md_contents

def post_proc(config, html_contents, **kwargs):
	return html_contents