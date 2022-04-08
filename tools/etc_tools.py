#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys, os
import json

import pathlib

def save_to_json_file(attach_info_json_path, dic_data) :
    target_path = attach_info_json_path
    abpath_full = str(pathlib.PurePath(str(pathlib.Path(target_path).resolve())))
    abpath_folder = str(pathlib.PurePath(abpath_full).parent)

    pathlib.Path(abpath_folder).mkdir(exist_ok=True, parents=True)

    with open(target_path, 'wt', encoding='utf-8') as json_file:
        json.dump(dic_data, json_file, indent="\t", ensure_ascii=False)
    return True

def load_from_json_file(attach_info_json_path) :
    target_path = attach_info_json_path
    if pathlib.Path(target_path).exists() == True :
        with open(target_path, 'r', encoding='utf-8') as json_data:
            return json.load(json_data)
    else :
        return None

def load_from_dic(dic_str) :
    return json.loads(dic_str)



def join_path(*args) :
    path = ''
    for arg in args :
        path = pathlib.PurePath(path, arg)
    return str(path)

def get_file_info(target_path) :
	findinfo_dic = {}

	if pathlib.Path(target_path).exists() == False :
		return None

	findinfo_dic['file_name'] = str(pathlib.PurePath(target_path).stem)
	findinfo_dic['file_ext'] = str(pathlib.PurePath(target_path).suffix)
	findinfo_dic['file_full_name'] = findinfo_dic['file_name'] + findinfo_dic['file_ext']

	findinfo_dic['abpath_full'] = str(pathlib.PurePath(str(pathlib.Path(target_path).resolve())))
	findinfo_dic['abpath_dir'] = str(pathlib.PurePath(findinfo_dic['abpath_full']).parent)

	findinfo_dic['is_file'] = pathlib.Path(target_path).is_file()
	findinfo_dic['is_dir'] = pathlib.Path(target_path).is_dir()

	return findinfo_dic

def get_fileinfo_from_folder(path_folder, ext, exclude_paths=[]) :
	path = pathlib.Path(path_folder)

	fileinfo_dic_arr = []

	for target_path in path.glob('**/' + ext):
		exclude_path_flag = False
		findinfo_dic = get_file_info(target_path)

		# filter skip files
		for exclude_path in exclude_paths :
			if findinfo_dic['abpath_full'].find(exclude_path) >= 0:
				exclude_path_flag = True
				break

		if exclude_path_flag == False :
			fileinfo_dic_arr.append(findinfo_dic)

	return fileinfo_dic_arr