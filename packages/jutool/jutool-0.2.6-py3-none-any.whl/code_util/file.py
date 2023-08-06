import os, pickle
import time


def create_folder_if_not_exsited(*args):
    """
    如果路径下不存在则创建文件夹，返回路径
    :param args: 路径的分段信息，类似os.path.join
    :return: 路径
    """
    path = os.path.join(*args)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


class safe_pickle:
    def __init__(self, folder, filename):
        self._folder = folder
        self._filename = filename

        self._first_path = os.path.join(folder, filename)
        self._second_path = os.path.join(folder, "_" + filename)

        self._finfo_first = self._get_file_info(self._first_path)["time"]
        self._finfo_second = self._get_file_info(self._second_path)["time"]

        if self._finfo_first > self._finfo_second:
            self.read_path = self._first_path
            self.next_path = self._second_path
        else:
            self.read_path = self._second_path
            self.next_path = self._first_path

    def _get_file_info(self, path):
        try:
            with open(path, 'rb') as ff:
                return pickle.load(ff)
        except:
            return {
                'path': path,
                'time': 0,
                'obj': None
            }

    def exsite(self):
        if (not os.path.exists(self._first_path)) and (not os.path.exists(self._second_path)):
            return False
        return True

    def dump(self, obj):
        with open(self.next_path, 'wb') as ff:
            pickle.dump({'path': self.next_path,
                         'time': time.time(),
                         'obj': obj}, ff)

            if self.next_path == self._first_path:
                self.read_path = self._first_path
                self.next_path = self._second_path
            else:
                self.read_path = self._second_path
                self.next_path = self._first_path

    def load(self):
        if not os.path.exists(self.read_path):
            return None
        with open(self.read_path, 'rb') as ff:
            return pickle.load(ff)['obj']
