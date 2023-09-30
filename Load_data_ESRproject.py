import os


# получает s01_ESR_211019_f064000n008p и возвращает (64.0, '008p')
def get_frequency_and_run_number(string):
    # ['f064000', '008p']
    frequency_and_run = string.split("_")[-1].split("n")
    frequency = float(frequency_and_run[0][1:])/1000
    run = frequency_and_run[1]
    # (64.0, '008p')
    return (frequency, run)


def get_up_dn_information(string):
    up_or_dn_information = string.split("_")[0][2:4]
    return up_or_dn_information

def get_name_of_file_from_path(path_of_file):
    list_of_full_path = path_of_file.split("/")
    file_name = list_of_full_path[-1]
    directory_name = "/".join(list_of_full_path[:-1])
    return file_name, directory_name


def split_name_of_file(name_of_file):

    left_splitted_name_of_file, right_splitted_name_of_file = name_of_file.split("+")

    frequency = get_frequency_and_run_number(left_splitted_name_of_file)[0]
    run = get_frequency_and_run_number(left_splitted_name_of_file)[1]
    up_dn_information = get_up_dn_information(right_splitted_name_of_file)

    return frequency, run, up_dn_information, name_of_file


def get_files_paths(folder_path) -> list:
    files_paths = [f.path for f in os.scandir(folder_path) if not f.is_dir()]
    return files_paths


def filter_files_by_size(list_of_files, min_size=51200):
    files_big_enough = []
    for path_file in list_of_files:
        if os.path.getsize(path_file) > min_size:
            files_big_enough.append(path_file)
    return files_big_enough


# эта функция сразу отфильтрует от папок и временно созданных файлов
def filter_files_by_up_dn(list_of_files):
    filtered_files_dn = [files for files in list_of_files if "+99dn" in files]
    filtered_files_up = [files for files in list_of_files if "+99up" in files]
    return filtered_files_dn, filtered_files_up


def get_list_for_plot(list_files_dn, list_files_up):

    list_for_plot = []
    filtered_files_dn_temp = list_files_dn[:]
    filtered_files_up_temp = list_files_up[:]

    for ind in range(len(list_files_dn)):
        file_name = list_files_dn[ind]
        temp_file_name = file_name.replace("+99dn", "+99up")
        if temp_file_name in list_files_up:
            list_for_plot.append((file_name, temp_file_name))
            filtered_files_dn_temp.remove(file_name)
            filtered_files_up_temp.remove(temp_file_name)

    if len(filtered_files_dn_temp):
        for ind in range(len(filtered_files_dn_temp)):
            file_name_dn = filtered_files_dn_temp[ind]
            list_for_plot.append(((file_name_dn, [])))

    if len(filtered_files_up_temp):
        for ind in range(len(filtered_files_up_temp)):
            file_name_up = filtered_files_up_temp[ind]
            list_for_plot.append((([], file_name_up)))

    return list_for_plot