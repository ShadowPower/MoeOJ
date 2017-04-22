def difficulty_to_text(difficulty):
    DIFFICULTY_DESC = ['入门', '简单', '中等', '困难']
    return DIFFICULTY_DESC[difficulty]

def language_to_text(language):
    LANGUAGE_DESC = ['C', 'C++', 'Java', 'Python']
    return LANGUAGE_DESC[language]

def result_to_text(result):
    RESULT_DESC = ['正确答案', '编译错误', '错误答案', '运行错误', '时间超限', '输出超限', '内存超限', '函数受限', '格式错误']
    return RESULT_DESC[result]