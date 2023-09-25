
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from mainwindow import Ui_MainWindow
from zip_file_filter import zipFileFilter
from my_thread_pool import MyThreadPool
from type_log.type_log import *


class QMyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.file_filter = zipFileFilter()
        self.run_thread = MyThreadPool(max_workers=2)
        self.run_thread.finished.connect(self.signal_call_back)

        self.set_connect_callback()
        self.log_handle = TypeLog(log_type=LOG_FILE_APPEND, log_file='operation_log')
        return

    def change_to_step_rule_label(self):
        self.ui.label_rule_item1.setText('Begin Token')
        self.ui.label_rule_item2.setText('Rule Item')
        self.ui.label_rule_item3.setText('End Token')

    def change_to_common_rule_label(self):
        self.ui.label_rule_item1.setText('Rule Item1')
        self.ui.label_rule_item2.setText('Rule Item2')
        self.ui.label_rule_item3.setText('Rule Item3')

    def set_connect_callback(self):
        # operator input container
        self.ui.pushButton_choose_file.clicked.connect(self.choose_unzip_file)
        self.ui.pushButton_choose_dir.clicked.connect(self.choose_dir)
        self.ui.pushButton_display_file_list.clicked.connect(self.show_file_list)
        self.ui.pushButton_find_message.clicked.connect(self.unzip_file_and_match)
        self.ui.pushButton_export_result.clicked.connect(self.export_result_info)

        # filter rule input container
        self.ui.pushButton_rule_add.clicked.connect(self.rule_add_process)
        self.ui.pushButton_rule_delete.clicked.connect(self.rule_delete_process)
        self.ui.pushButton_rule_clear.clicked.connect(self.rule_clear_process)
        self.ui.radioButton_rule_step.clicked.connect(self.change_to_step_rule_label)
        self.ui.radioButton_rule_and.clicked.connect(self.change_to_common_rule_label)
        self.ui.radioButton_rule_or.clicked.connect(self.change_to_common_rule_label)

        return

    def disable_all_button(self):
        self.ui.pushButton_choose_file.setDisabled(True)
        self.ui.pushButton_choose_dir.setDisabled(True)
        self.ui.pushButton_display_file_list.setDisabled(True)
        self.ui.pushButton_find_message.setDisabled(True)
        self.ui.pushButton_export_result.setDisabled(True)

        self.disable_rule_input_window()
        return

    def enable_all_button(self):
        self.ui.pushButton_choose_file.setEnabled(True)
        self.ui.pushButton_choose_dir.setEnabled(True)
        self.ui.pushButton_display_file_list.setEnabled(True)
        self.ui.pushButton_find_message.setEnabled(True)
        self.ui.pushButton_export_result.setEnabled(True)

        self.enable_rule_input_window()
        return

    def enable_rule_input_window(self):
        self.ui.pushButton_rule_add.setEnabled(True)
        self.ui.pushButton_rule_delete.setEnabled(True)
        self.ui.pushButton_rule_clear.setEnabled(True)

        self.ui.radioButton_rule_and.setEnabled(True)
        self.ui.radioButton_rule_or.setEnabled(True)
        self.ui.lineEdit_rule_item1.setEnabled(True)
        self.ui.lineEdit_rule_item2.setEnabled(True)
        self.ui.lineEdit_rule_item3.setEnabled(True)

    def disable_rule_input_window(self):
        self.ui.pushButton_rule_add.setDisabled(True)
        self.ui.pushButton_rule_delete.setDisabled(True)
        self.ui.pushButton_rule_clear.setDisabled(True)

        self.ui.radioButton_rule_and.setDisabled(True)
        self.ui.radioButton_rule_or.setDisabled(True)
        self.ui.lineEdit_rule_item1.setDisabled(True)
        self.ui.lineEdit_rule_item2.setDisabled(True)
        self.ui.lineEdit_rule_item3.setDisabled(True)
        return

    def clear_rule_input_window(self):
        self.ui.lineEdit_rule_item1.clear()
        self.ui.lineEdit_rule_item2.clear()
        self.ui.lineEdit_rule_item3.clear()

        return

    def choose_unzip_file(self):
        file_name, file_type = QFileDialog.getOpenFileName(None, 'choose parse file')
        if file_name == '':
            return

        self.file_filter.set_zip_file(file_name)
        self.ui.lineEdit_zip_file.setText(file_name)
        self.log_handle.logging('parse zip file', LOG_WARNING, 'choose unzip file :%s.' % file_name)
        return

    def choose_dir(self):
        path = QFileDialog.getExistingDirectory(None, "choose the unzip dir", "/")
        if path == '':
            return

        self.file_filter.set_unzip_path(path)
        self.ui.lineEdit_unzip_path.setText(path)

        self.log_handle.logging('parse zip file', LOG_WARNING, 'choose unzip dir :%s.' % path)
        return

    def signal_call_back(self, data):
        if data[0] == 'result_info' or data[0] == 'filter_list':
            self.ui.display_result_info.setPlainText(data[1])

        self.enable_all_button()
        return

    def match_file_of_filter_rule(self, msg):
        self.file_filter.extract_all_file()
        self.file_filter.match_file_by_filter_rule()
        if msg == 'match_file':
            result_data = self.file_filter.get_filter_result_info()
        elif msg == 'show_file_list':
            result_data = self.file_filter.get_filter_result_file_list()
        elif msg == 'export_result':
            self.log_handle.logging('parse zip file', LOG_ERROR, 'wrong msg.')
            return 'wrong msg'

        return result_data

    def unzip_file_and_match(self):
        self.disable_all_button()
        self.run_thread.submit(self.match_file_of_filter_rule, 'match_file')
        return

    def show_file_list(self):
        self.disable_all_button()
        self.run_thread.submit(self.match_file_of_filter_rule, 'show_file_list')
        return

    def export_result_info(self):
        self.disable_all_button()
        self.run_thread.submit(self.match_file_of_filter_rule, 'export_result')
        return

    def get_rule_content(self):
        # the default value of rule type is 'OR'
        rule_type = 'OR'
        if self.ui.radioButton_rule_and.isChecked():
            rule_type = 'AND'
        elif self.ui.radioButton_rule_step.isChecked():
            rule_type = 'STEP'

        rule_list = []
        item = self.ui.lineEdit_rule_item1.text()
        if item != '':
            rule_list.append(item)

        item = self.ui.lineEdit_rule_item2.text()
        if item != '':
            rule_list.append(item)

        item = self.ui.lineEdit_rule_item3.text()
        if item != '':
            rule_list.append(item)

        return rule_type, rule_list

    def get_rule_display_rows(self):
        display_rows = self.ui.lineEdit_display_rows.text()
        return display_rows

    def rule_add_process(self):
        rule_type, rule_msg = self.get_rule_content()
        if len(rule_msg) == 0:
            return

        rule_rows = self.get_rule_display_rows()

        result_info = self.file_filter.filter_rule_add(rule_type, rule_msg, rule_rows)

        rule_display = self.file_filter.filter_rule_get_display()
        self.ui.textEdit_rule_display.setText(rule_display)
        self.clear_rule_input_window()
        self.log_handle.logging('parse zip file', LOG_WARNING, 'add new rule: type %s, msg:%s, result:%s.' %
                                (rule_type, rule_msg, result_info))

        return

    def rule_delete_process(self):
        rule_type, rule_msg = self.get_rule_content()
        if len(rule_msg) == 0:
            return

        result_info = self.file_filter.filter_rule_delete(rule_type, rule_msg)

        rule_display = self.file_filter.filter_rule_get_display()
        self.ui.textEdit_rule_display.setText(rule_display)
        self.clear_rule_input_window()
        self.log_handle.logging('parse zip file', LOG_WARNING, 'delete rule: type %s, msg:%s, result:%s.' %
                                (rule_type, rule_msg, result_info))
        return

    def rule_clear_process(self):
        print('rule clear process')
        result_info = self.file_filter.filter_rule_clear()
        print(result_info)

        rule_display = self.file_filter.filter_rule_get_display()
        self.ui.textEdit_rule_display.setText(rule_display)
        self.clear_rule_input_window()

        self.log_handle.logging('parse zip file', LOG_WARNING, 'clear all the rule.')
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = QMyMainWindow()
    form.show()
    sys.exit(app.exec_())
