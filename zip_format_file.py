
import os
import zipfile

from compress_file import CompressFile


class ZipFormatFile(CompressFile):
    def __init__(self, zip_file=None, unzip_path=None):
        super().__init__(zip_file, unzip_path)
        return

    def extract_all_file(self):
        if self.zip_file is None:
            return []

        # the unzip_path default value is the directory of the zip file
        if self.unzip_path is None:
            self.unzip_path, file_name = os.path.split(self.zip_file)

        zip_file = zipfile.ZipFile(self.zip_file, 'r')
        zip_file_list = zip_file.namelist()

        try:
            zip_file.extractall(self.unzip_path)
        except Exception as Error:
            print('Error occurs: %s.' % str(Error))

        zip_file.close()

        extract_file_list = []
        for file_item in zip_file_list:
            file_name = os.path.join(self.unzip_path, file_item)
            file_name = os.path.normpath(file_name)
            extract_file_list.append(file_name)

        return extract_file_list

    def extract_file_by_name(self, file_name):
        zip_file = zipfile.ZipFile(self.zip_file, 'r')
        zip_file_list = zip_file.namelist()
        extract_file_list = []

        for file_item in zip_file_list:
            if file_name not in file_item:
                continue

            # extract the specific file
            try:
                zip_file.extract(file_item, self.unzip_path)
            except Exception as Error:
                print('Error occurs: %s.' % str(Error))

            file_name = os.path.join(self.unzip_path, file_item)
            file_name = os.path.normpath(file_name)
            extract_file_list.append(file_name)

        zip_file.close()
        return extract_file_list


if __name__ == '__main__':
    zip_file = ZipFormatFile('C:/Users/Administrator/Desktop/testfile/log.zip', 'C:/Users/Administrator/Desktop/testfile/unzip_path')
    file_list = zip_file.extract_all_file()
    print(file_list)

    zip_file.set_zip_file('C:/Users/Administrator/Desktop/testfile/log (3).zip')
    file_list = zip_file.extract_file_by_name('GW')
    print(file_list)



