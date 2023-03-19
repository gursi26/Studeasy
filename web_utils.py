def count_indentation(line):
    return len(line) - len(line.lstrip())

def indented_string_to_dict(indented_string):
    lines = indented_string.strip().split('\n')
    current_indent = 0
    result = {}
    parent_keys = []
    for line in lines:
        temp_indent = count_indentation(line)

        if temp_indent > current_indent:
            if parent_keys[-1] not in result:
                result[parent_keys[-1]] = []
            
            result[parent_keys[-1]].append(line.lstrip())
        else:
            parent_keys.append(line)
            result[line] = []
    return result
