
import re

def pre_proc(config, md_contents, **kwargs):
	chk_pattern = {}
	while chk_pattern is not None:
		chk_pattern = re.search('```ad-.*([^`]*)```', md_contents)
		if chk_pattern is None :
			continue
		replace_str = original_str = chk_pattern.group(0)

		replace_str = replace_str.replace('```ad-note','!!! note')
		replace_str = replace_str.replace('```ad-info','!!! note')
		replace_str = replace_str.replace('```ad-tip','!!! important')
		replace_str = replace_str.replace('```ad-danger','!!! danger')
		replace_str = replace_str.replace('```','')
		# insert indent space..
		replace_str = replace_str.replace('\n','\n    ')
		replace_str = replace_str.replace('\r\n','\n    ')
		
		md_contents = md_contents.replace(original_str, replace_str)

	return md_contents

def post_proc(config, html_contents, **kwargs):
	return html_contents
