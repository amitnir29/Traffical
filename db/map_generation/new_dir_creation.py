import os

DIRS_PATH = "db/databases/generated"


def create_new_dir() -> str:
    """
    create the dir of the new db
    :return: the full path of the new dir
    """
    name = __get_new_dir_name()
    path = DIRS_PATH + "/" + name
    os.mkdir(path)
    return path


def __get_new_dir_name() -> str:
    """
    :return: name of the new dir
    """
    try:
        dirs = os.listdir(DIRS_PATH)
    except FileNotFoundError as e:
        # no "generated" dir. create it
        os.mkdir(DIRS_PATH)
        return "0"
    # dir exists. check the inner dirs
    dirs_nums = [int(dir_name) for dir_name in dirs]
    # if no inner dirs:
    if len(dirs_nums) == 0:
        return "0"
    # return the next dir number
    new_name = max(dirs_nums) + 1
    return str(new_name)
