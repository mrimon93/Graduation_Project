import os


def make_directory_tree(dir_path):
    CURR_DIR_PATH = os.path.dirname(os.path.realpath(__file__))

    dir_list = [
        os.path.join(dir_path, 'data_w'),
        os.path.join(dir_path, 'data_el'),

        os.path.join(dir_path, 'data_w', 'raw'),
        os.path.join(dir_path, 'data_el', 'raw'),

        os.path.join(dir_path, 'data_w', 'target'),
        os.path.join(dir_path, 'data_el', 'harmonized'),

        # os.path.join(dir_path, 'data_w', 'merged'),
        os.path.join(dir_path, 'data_el', 'merged'),
        
        os.path.join(dir_path, 'data_w', 'clean'),
        os.path.join(dir_path, 'data_w', 'final_avg'),
    ]


    for dir in dir_list:
        if not os.path.exists(dir):
            print(dir)
            os.mkdir(dir)
