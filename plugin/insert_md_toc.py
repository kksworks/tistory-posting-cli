

def pre_proc(config_ctx, md_contents, **kwargs):
	## python markdown TOC insert
	if md_contents.find('[TOC]') < 0 :
		md_contents = '\r\n[TOC]\r\n\r\n' + md_contents
	
	return md_contents


def post_proc(config_ctx, html_contents, **kwargs):
	return html_contents
