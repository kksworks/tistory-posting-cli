def pre_proc(config_ctx, md_contents, **kwargs):
	md_contents += '\r\n\r\n'
	md_contents += '...'
	md_contents += '\r\n\r\n'
	md_contents += '- 해당 포스팅은 [tistory-posting-cli](https://github.com/kksworks/tistory-posting-cli) 를 이용해 발행되었습니다.'
	md_contents += '\r\n\r\n'
	return md_contents


def post_proc(config_ctx, html_contents, **kwargs):
	return html_contents
