
DEFAULT_ACTION = 6
STEP_RULE_BEGIN_MATCH = 0
STEP_RULE_TOKEN_MATCH = 1
STEP_RULE_END_MATCH = 2


class FilterRule:
    def __init__(self, rule_type=None, rule_msg=None, action=DEFAULT_ACTION):
        self.filter_rule = []
        self.step_rule_match = []

        if rule_type is None or rule_msg is None:
            return

        if rule_type in ['AND', 'OR', 'STEP']:
            self.filter_rule.append({'type': rule_type, 'rule': rule_msg, 'action': action})
        return

    def add_new_rule(self, rule):
        for rule_item in self.filter_rule:
            if rule['type'] != rule_item['type']:
                continue

            if rule['rule'] != rule_item['rule']:
                continue

            rule_item['action'] = rule['action']
            return

        self.filter_rule.append(rule)
        return

    def delete_exist_rule(self, rule):
        for rule_item in self.filter_rule:
            if rule['type'] != rule_item['type']:
                continue

            if rule['rule'] != rule_item['rule']:
                continue

            # the type and rule of the new rule are matched with exist rule's
            self.filter_rule.remove(rule_item)
            return

        return

    def rule_add_process(self, rule_type, rule_msg, rule_action='6'):
        if rule_type not in ['AND', 'OR', 'STEP']:
            return 'Error rule type, please input one of \'AND\', \'OR\', \'STEP\''

        if type(rule_msg) is not list:
            return 'Wrong type of rule msg'

        for rule_item in rule_msg:
            if len(rule_item) == 0:
                return 'Empty rule content, please input.'

        try:
            action = int(rule_action)
        except Exception as Error:
            print(Error)
            action = DEFAULT_ACTION

        rule = {'type': rule_type, 'rule': rule_msg, 'action': action}
        self.add_new_rule(rule)

        return 'success'

    def rule_delete_process(self, rule_type, rule_msg):
        if rule_type not in ['AND', 'OR', 'STEP']:
            return 'Error rule type, please input one of \'AND\', \'OR\', \'STEP\''

        rule = {'type': rule_type, 'rule': rule_msg}
        self.delete_exist_rule(rule)

        return 'success'

    def rule_clear_process(self):
        self.filter_rule.clear()
        return

    def get_rule_info(self):
        rule_info = ''
        for rule_item in self.filter_rule:
            rule_item_str = '%s:%s\n' % (rule_item['type'], str(rule_item['rule']))
            rule_info += rule_item_str

        return rule_info

    def match_and_rule(self, line_msg, rule_list):
        for rule_item in rule_list:
            if rule_item not in line_msg:
                return False

        return True

    def match_or_rule(self, line_msg, rule_list):
        for rule_item in rule_list:
            if rule_item in line_msg:
                return True
        return False

    def match_step_rule(self, line_msg, rule_item):
        for match_item in self.step_rule_match:
            if rule_item == match_item:
                # get the rule item and match to line msg
                rule_list = match_item['rule']

                # delete the step rule from the list of step match info
                if len(rule_list) == STEP_RULE_END_MATCH + 1 and rule_list[STEP_RULE_END_MATCH] in line_msg:
                    self.step_rule_match.remove(match_item)
                    return False

                if rule_list[STEP_RULE_TOKEN_MATCH] not in line_msg:
                    return False

                return True

            continue
        # if the rule in not in step match info
        rule_list_item = rule_item['rule'][STEP_RULE_BEGIN_MATCH]
        if rule_list_item not in line_msg:
            return False

        self.step_rule_match.append(rule_item)

        return False

    def match_rule_by_line(self, line):
        # travel all the rules
        for rule_item in self.filter_rule:
            if rule_item['type'] == 'AND':
                is_match = self.match_and_rule(line, rule_item['rule'])
            elif rule_item['type'] == 'OR':
                is_match = self.match_or_rule(line, rule_item['rule'])
            else:
                is_match = self.match_step_rule(line, rule_item)

            if is_match is True:
                return True, rule_item['action']

        # end of travel, state not match any rules, so return false
        return False, None

    def match_rule_by_file(self, file):
        # clear step rule match info
        self.step_rule_match.clear()

        # begin to match rules to file
        file_fd = open(file, 'r', errors='ignore')
        line_msg = file_fd.readline()
        result_info = {'file': file, 'match_info': []}
        match_info = []
        index = 1
        while line_msg:
            is_match, action = self.match_rule_by_line(line_msg)
            if is_match is True:
                if type(action) is not int:
                    action = 1

                # do the filter rule action
                for id in range(action):
                    match_item = {'index': index, 'msg': line_msg}
                    match_info.append(match_item)

                    line_msg = file_fd.readline()
                    index += 1

            line_msg = file_fd.readline()
            index += 1

        if len(match_info) == 0:
            return None

        result_info['match_info'] = match_info

        return result_info


if __name__ == '__main__':
    filter_rule = FilterRule('STEP', ['wap.ssp.ps', 'kernelapp'])
    rule_info = filter_rule.get_rule_info()
    print(rule_info)

    match_info = filter_rule.match_rule_by_file('C:/Users/Administrator/Desktop/testfile/unzip_path/'
                                                '00E0FC015168_GW_collectDebugInfo_00E0FC015168_2000_07_08_21_18_480')
    print(match_info)

    filter_rule.rule_clear_process()
    rule_info = filter_rule.get_rule_info()
    print(rule_info)
