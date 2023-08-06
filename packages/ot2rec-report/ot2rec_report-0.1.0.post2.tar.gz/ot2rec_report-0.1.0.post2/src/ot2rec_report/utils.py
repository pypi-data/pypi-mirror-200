from glob import glob
import os


def get_processes(plist):
    node_list = []
    for curr_proc in plist:
        # Find relevant log files
        file_lookfor = f"{os.getcwd()}/o2r_{curr_proc}.log"
        file_found = len(glob(file_lookfor)) == 1

        try:
            assert file_found
        except:
            print(f"File {file_lookfor} not found. Process {curr_proc} not performed?")

        if file_found:
            node_list.append(curr_proc)

    return node_list


# def get_process_from_dir(directory):
#     node_list = []
#     for file in os.listdir(directory):
#         if file.endswith(".log"):
#             node_list.append(file)
#     return node_list
