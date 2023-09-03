
import os
import sys


class CompressFile:
    def __init__(self, zip_file=None, unzip_path=None):
        self.zip_file = None
        self.unzip_path = None

        if zip_file is None or unzip_path is None:
            return 'Please input zip_file and unzip_path.'

        if os.path.exists(zip_file) is False:
            return 'the file [%s] is not exist.' % zip_file

        if os.path.exists(unzip_path) is False:
            return 'the unzip path [%s] is not exist.' % unzip_path

        self.zip_file = zip_file
        self.unzip_path = unzip_path
        return 'Success'

    def set_zip_file(self, zip_file):
        if os.path.exists(zip_file) is False:
            return 'the file [%s] is not exist.' % zip_file

        self.zip_file = zip_file
        return 'Success'

    def set_unzip_path(self, unzip_path):
        if os.path.exists(unzip_path) is False:
            return 'the unzip path [%s] is not exist.' % unzip_path

        self.unzip_path = unzip_path
        return 'Success'

    def extract_all_file(self):
        return

    def extract_file(self):
        return


if __name__ == '__main__':
    zipfile = CompressFile()
    zipfile.unzip_file()

