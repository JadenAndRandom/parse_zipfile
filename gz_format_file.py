
import os
import gzip
from compress_file import CompressFile


class GzipFormatFile(CompressFile):
    def __init__(self, zip_file=None, unzip_path=None):
        super().__init__(zip_file, unzip_path)
        return

    def extract_all_file(self):
        if self.zip_file is None:
            return []

        # the unzip_path default value is the directory of the zip file
        if self.unzip_path is None:
            self.unzip_path, file_name = os.path.split(self.zip_file)

        unzip_file_list = []
        file_path, file_name = os.path.split(self.zip_file)
        unzip_file_name = file_name.replace('.gz', '')
        unzip_file_path = os.path.join(self.unzip_path, unzip_file_name)

        with open(unzip_file_path, 'wb') as pw:
            gzip_file = gzip.GzipFile(self.zip_file, mode='rb')
            pw.write(gzip_file.read())
            gzip_file.close()

        unzip_file_list.append(os.path.normpath(unzip_file_path))
        return unzip_file_list

    def extract_file_by_name(self, file_name):
        return self.extract_all_file()


if __name__ == '__main__':
    zip_file = GzipFormatFile('C:\\Users\\Administrator\\Desktop\\testfile\\unzip_path\\20658EDE6074_AP_collectDebugInfo_20658EDE6074_2000_07_08_13_16_400.gz',
                              'C:/Users/Administrator/Desktop/testfile/unzip_path')
    file_list = zip_file.extract_all_file()
    print(file_list)
