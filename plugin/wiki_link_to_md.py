
# wikilink -> mdlink -> html convert
def pre_proc(ctx_info, md_contents, **kwargs):
	if ctx_info['is_test_run'] == True :
		return md_contents

def post_proc(ctx_info, html_contents, **kwargs):
	return html_contents
