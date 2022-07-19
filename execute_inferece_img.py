import shutil
import subprocess
from os import listdir
from os.path import isfile, join

from tqdm import tqdm

img_dir_root = "/Users/larcuser/pc_folder/data/subset_of_data_for_interpolation_study/every_4th"
target_root = img_dir_root+"/interpolated"
exp=2

import os


def copy_files_to_final_dir(src_dir, out_dir, first_file_name):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    first_file_number = int(first_file_name.split("/")[-1].split(".")[0])
    original_files = get_sorted_file_list(src_dir)
    for original_file in original_files:
        file_name = original_file.split("/")[-1]
        new_file_path = join(out_dir, file_name)
        copy_file(original_file, new_file_path)
    interpolated_files = get_sorted_file_list("output")
    for i in range(len(interpolated_files)):
        file_name = "%04d.png"%(first_file_number+i+1)
        new_file_path = join(out_dir, file_name)
        copy_file(interpolated_files[i], new_file_path)


def copy_file(old_file, new_file):
    print(old_file, new_file)
    shutil.copyfile(old_file, new_file)


def get_sorted_file_list(a_dir):
    onlyfiles = [join(a_dir, f) for f in listdir(a_dir) if isfile(join(a_dir, f)) and f.lower().endswith("png")]
    return sorted(onlyfiles)


def get_sub_folder_list(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def get_png_files_in_dir(a_dir):
    return [name for name in os.listdir(a_dir)
            if name.lower().endswith('png')]


for src_sub_dir in tqdm(get_sub_folder_list(img_dir_root)):
    src_sub_dir_path = os.path.join(img_dir_root, src_sub_dir)
    target_sub_dir_path = os.path.join(target_root, src_sub_dir)
    file_list = get_sorted_file_list(src_sub_dir_path)
    for i in range(len(file_list) -1):
        command = ["python3", "inference_img.py", "--img", file_list[i], file_list[i+1], "--exp="+str(exp)]
        # print(command)
        # subprocess.run(command)
        copy_files_to_final_dir(src_sub_dir_path, target_sub_dir_path, file_list[i])
