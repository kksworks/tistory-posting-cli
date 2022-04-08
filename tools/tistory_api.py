import os, sys

import requests
import json

import urllib3

# -----------------
# config setting
# -----------------
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DEFALT_TIMEOUT_SEC=15

def get_blog_category(blog_name, api_key_str) :
	data = {
		'access_token' : api_key_str,
		'blogName' : blog_name,
		'output' : 'json'
	}

	# api : POST https://www.tistory.com/apis/post/write?

	session = requests.Session()
	response = session.get('https://www.tistory.com/apis/category/list', timeout=DEFALT_TIMEOUT_SEC, params=data, verify=False)

	if response.status_code != 200 :
		return None

	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic['tistory']['item']['categories']
	except :
		return None

def get_blog_info(api_key_str) :
	data = {
		'access_token' : api_key_str,
		'output' : 'json'
	}

	# api : POST https://www.tistory.com/apis/post/write?

	session = requests.Session()
	response = session.get('https://www.tistory.com/apis/blog/info', timeout=DEFALT_TIMEOUT_SEC, params=data, verify=False)

	if response.status_code != 200 :
		return None
	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic
	except :
		None

def write_post(blog_name, api_key_str, title_str, content_html, category_id, tags, publish=True, post_id=None) :
	if post_id is None : 
		return _write_post(blog_name, api_key_str, title_str, content_html, category_id, tags, publish)
	else :
		return _edit_post(blog_name, api_key_str, post_id, title_str, content_html, category_id, tags, publish)

def _write_post(blog_name, api_key_str, title_str, content_html, category_id, tags, publish=True) :
	data = {
		'access_token' : api_key_str,
		'blogName' : blog_name,
		'title' : title_str,
		'output' : 'json',
		'content' : content_html,
		'visibility' : str((lambda x: 3 if x == True else 0)(publish)),
		'category' : str(category_id),
		'tag' : ','.join(tags)
	}

	# api : POST https://www.tistory.com/apis/post/write?

	session = requests.Session()
	response = session.post('https://www.tistory.com/apis/post/write', timeout=DEFALT_TIMEOUT_SEC, data=data, verify=False)

	if response.status_code != 200 :
		return None

	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic
	except :
		return None

def read_post(blog_name, api_key_str, post_id) :
	data = {
		'access_token' : api_key_str,
		'output' : 'json',
		'blogName' : blog_name,
		'postId' : post_id
	}

	# api : GET https://www.tistory.com/apis/post/read?

	session = requests.Session()
	response = session.get('https://www.tistory.com/apis/post/read', timeout=DEFALT_TIMEOUT_SEC, params=data, verify=False)

	if response.status_code != 200 :
		return None
	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic['tistory']['item']['id']
	except :
		return None

def _edit_post(blog_name, api_key_str, post_id, title_str, content_html, category_id, tags, publish=True) :
	data = {
		'access_token' : api_key_str,
		'postId' : post_id,
		'blogName' : blog_name,
		'title' : title_str,
		'output' : 'json',
		'content' : content_html,
		'visibility' : str((lambda x: 3 if x == True else 0)(publish)),
		'category' : str(category_id),
		'tag' : ','.join(tags)
	}

	# api : POST https://www.tistory.com/apis/post/write?

	session = requests.Session()
	response = session.post('https://www.tistory.com/apis/post/modify', timeout=DEFALT_TIMEOUT_SEC, data=data, verify=False)

	if response.status_code != 200 :
		return None

	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic
	except :
		return None

def attach_data(blog_name, api_key_str, target_file) :
	data = {'content-type': 'multipart/form-data',
		'access_token' : api_key_str,
		'blogName' : blog_name,
		'output' : 'json',
	}
	files = {'uploadedfile':open(target_file, 'rb')}

	# api : POST https://www.tistory.com/apis/post/write?

	session = requests.Session()
	response = session.post('https://www.tistory.com/apis/post/attach', timeout=DEFALT_TIMEOUT_SEC, files=files, params=data, verify=False)

	# return --
	# {'tistory': {'status': '200', 'url': 'https://blog.kakaocdn.net/dn/bRswZz/btrdlxc9yhr/vn3Zg7KHKUZHnWuAdIP9b1/img.png', 'replacer': '[##_Image|kage@bRswZz/btrdlxc9yhr/vn3Zg7KHKUZHnWuAdIP9b1/img.png|alignCenter|width="700" height="497" data-origin-width="700" data-origin-height="497" data-ke-mobilestyle="widthOrigin" filename="img.png" filemime="image/png"|||_##]'}}

	if response.status_code != 200 :
		return None

	try:
		content_str = response.content.decode('utf-8', 'ignore')
		content_dic = json.loads(content_str)
		return content_dic
	except :
		return None

if __name__ == "__main__":
	None