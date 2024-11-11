import os
import sys
import pathlib


def get_folder_size(folder_path):
    size = 0

    # get size
    for path, dirs, files in os.walk(folder_path):
        for f in files:
            fp = os.path.join(path, f)

            if os.path.exists(fp):  # for broken link sysm
                size += os.path.getsize(fp)

    # display size
    # print("Folder size: " + str(size))
    return size


if __name__ == '__main__':
    rootdir = '/mnt/XXXX/'

    path_lib = pathlib.Path(rootdir)

    # recursive

    # rec_items = path_lib.rglob("*_000")  # include folders only
    rec_items = path_lib.rglob("*_000*")  # include folders and files

    # folders and files
    # items = list(path_lib.iterdir())

    for item_000 in rec_items:

        if item_000.is_dir():
            # print(f'Folder path: ${item}')
            # print(f'Folder name: ${item.name}')
            f_path = f'{item_000.parent}/{item_000.name.removesuffix("_000")}'
            f_size = get_folder_size(f_path)

            print('Folder:')
            print(f'  - path: {f_path}')
            print(f'  - size: {f_size}')

            print('Folder _000:')
            print(f'  - path: {item_000.absolute()}')
            # print(f'  - size: {f_size}')

            if f_size == 0:
                if os.path.exists(f_path):
                    os.rmdir(f_path)
                    print('================ Action performed ================')
                else:
                    print(f"The file {f_path} does not exist.")

                item_000.rename(f_path)

            else:
                print('================ Folder size > 0 ================')

        else:
            print('File:')
            f_path = f'{item_000.parent}/{item_000.name.replace("_000", '')}'
            if not os.path.exists(f_path):
                continue

            f_size = os.path.getsize(f_path)
            print(f'  - path: {f_path}')
            print(f'  - size: {f_size}')

            print('File _000:')
            f_000_size = os.path.getsize(item_000)
            print(f'  - path: {item_000.absolute()}')
            print(f'  - size: {f_000_size}')
            #
            if f_size == f_000_size:
                os.remove(item_000)

    # print (item[0])
    # for root, subFolders, files in os.walk(rootdir):
    #     print(f'root ${root}')
    #     print(f'subFolders ${subFolders}')
    #     print(f'files ${files}')
    #
    #     for folder in subFolders:
    #         # outfileName = rootdir + "/" + folder + "/py-outfile.txt"  # hardcoded path
    #         # folderOut = open(outfileName, 'w')
    #         print("outfileName is " + folder)
    #
    #         for file in files:
    #             filePath = rootdir + '/' + file
    # print("file path: " + file)
    # f = open(filePath, 'r')
    # toWrite = f.read()
    # print
    # "Writing '" + toWrite + "' to" + filePath
    # folderOut.write(toWrite)
    # f.close()

    # folderOut.close()
