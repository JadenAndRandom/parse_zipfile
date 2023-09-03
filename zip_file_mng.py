import os

from zip_format_file import ZipFormatFile
from gz_format_file import GzipFormatFile

FILE_STATE_INIT = 0
FILE_STATE_ZIP = 1
FILE_STATE_UNZIP = 2


class ZipFileMng:
    def __init__(self, zip_file=None, unzip_path=None):
        self.zip_file = zip_file
        self.unzip_path = unzip_path

        self.zip_object = None
        self.file_list = []
        self.extract_process_list = []

        self.state = FILE_STATE_ZIP
        if zip_file is None:
            self.state = FILE_STATE_INIT
        elif os.path.exists(zip_file) is False:
            return

        if unzip_path is not None and os.path.exists(unzip_path) is False:
            os.mkdir(unzip_path)
        return

    def set_zip_file(self, zip_file):
        if os.path.exists(zip_file) is False:
            return 'the file [%s] is not exist.' % zip_file

        self.zip_file = zip_file
        self.state = FILE_STATE_ZIP
        return ''

    def set_unzip_path(self, unzip_path):
        if os.path.exists(unzip_path) is False:
            return 'the unzip path [%s] is not exist.' % unzip_path

        self.unzip_path = unzip_path
        return ''

    # if the file_name is not None, then extract the specify file,
    # otherwise extract all the file from the zip file
    def extract_all_file(self, file_name=None):
        # if the file is unzip, return the file list directly
        if self.state == FILE_STATE_UNZIP:
            return self.file_list

        # init the mng module state
        self.file_list.clear()
        # init the process list
        self.extract_process_list.clear()
        self.extract_process_list.append(self.zip_file)

        # begin to extract file
        self.extract_process(file_name)
        self.state = FILE_STATE_UNZIP

        return self.file_list

    def extract_process(self, extract_file_name):

        for file_item in self.extract_process_list:
            file_path, file_name = os.path.split(file_item)
            file_type = str(file_name).split('.')[-1]

            # if the file type is not in the list, it is not need to unzip
            if file_type not in ['zip', 'gz', 'rar']:
                self.file_list.append(file_item)
                continue

            if file_type == 'zip':
                self.zip_object = ZipFormatFile(file_item, self.unzip_path)
            elif file_type == 'gz':
                self.zip_object = GzipFormatFile(file_item, self.unzip_path)
            else:
                continue

            if extract_file_name is None:
                extract_list = self.zip_object.extract_all_file()
            else:
                extract_list = self.zip_object.extract_file_by_name(extract_file_name)

            if type(extract_list) is list:
                for list_item in extract_list:
                    self.extract_process_list.append(list_item)
            else:
                self.extract_process_list.append(extract_list)

        return


if __name__ == '__main__':
    zip_file = ZipFileMng('C:/Users/Administrator/Desktop/testfile/log (3).zip',
                          'C:/Users/Administrator/Desktop/testfile/unzip_path')
    file_list = zip_file.extract_all_file()
    print(file_list)

    zip_file.set_zip_file('C:/Users/Administrator/Desktop/testfile/log (4).zip')
    file_list = zip_file.extract_all_file('GW')
    print(file_list)
