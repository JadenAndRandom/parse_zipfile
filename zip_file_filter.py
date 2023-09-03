
from filter_rule import FilterRule
from zip_file_mng import ZipFileMng

FILE_INIT_STATE = 1
FILE_ZIP_STATE = 2
FILE_UNZIP_STATE = 3
FILE_FILTER_STATE = 4


class zipFileFilter():
    def __init__(self, zip_file=None, unzip_dir=None):
        self.zip_file = zip_file
        self.unzip_dir = unzip_dir
        self.state = FILE_INIT_STATE

        self.filter_result = []
        self.filter_rule = FilterRule()
        self.file_mng = ZipFileMng()

        return

    def unzip_file_init(self):
        # clear the wait unzip file list, before the unzip process
        self.unzip_file_list.clear()

        self.unzip_file_list.append(self.zip_file)
        return

    def filter_rule_add(self, rule_type, rule_msg, rule_action):
        return self.filter_rule.rule_add_process(rule_type, rule_msg, rule_action)

    def filter_rule_delete(self, rule_type, rule_msg):
        return self.filter_rule.rule_delete_process(rule_type, rule_msg)

    def filter_rule_clear(self):
        return self.filter_rule.rule_clear_process()

    def filter_rule_get_display(self):
        return self.filter_rule.get_rule_info()

    def set_unzip_path(self, unzip_path):
        return self.file_mng.set_unzip_path(unzip_path)

    def set_zip_file(self, zip_file):
        return self.file_mng.set_zip_file(zip_file)

    def extract_all_file(self, file_name=None):
        return self.file_mng.extract_all_file(file_name)

    def match_file_by_filter_rule(self):
        # if the filter rule is empty, not travel the unzip file
        if len(self.filter_rule.filter_rule) == 0:
            return

        self.filter_result.clear()
        for file in self.file_mng.file_list:
            match_info = self.filter_rule.match_rule_by_file(file)
            # if the match info is None, not need to append
            if match_info is None:
                continue

            self.filter_result.append(match_info)
        return

    def get_filter_result_info(self):
        filter_result_str = ''
        for filter_item in self.filter_result:
            item_str = '%s:\n' % filter_item['file']
            for line_item in filter_item['match_info']:
                item_str += '\t%d: %s' % (line_item['index'], line_item['msg'])
            filter_result_str += item_str

        return 'result_info', filter_result_str

    def get_filter_result_file_list(self):
        filter_result_str = ''
        for filter_item in self.filter_result:
            item_str = '%s:\n' % filter_item['file']
            filter_result_str += item_str

        return 'filter_list', filter_result_str


if __name__ == '__main__':
    zipFileFilter = zipFileFilter()
