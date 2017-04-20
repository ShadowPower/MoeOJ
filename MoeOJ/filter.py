def difficulty_to_text(difficulty):
    DIFFICULTY_DESC = ['入门', '简单', '中等', '困难']
    return DIFFICULTY_DESC[difficulty]

def language_to_text(language):
    LANGUAGE_DESC = ['C', 'C++', 'Java', 'Python']
    return LANGUAGE_DESC[language]

def result_to_text(result):
    RESULT_DESC = ['答案正确', '编译错误', '答案错误', '程序崩溃', '运行超时', '无限输出', '内存超限', '函数受限', '格式错误']
    return RESULT_DESC[result]