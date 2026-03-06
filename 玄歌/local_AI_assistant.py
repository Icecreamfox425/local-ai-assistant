import ollama
import json
import time
history_user = []
# identify time to greeting


def time_greeting():
    now_time = time.strftime('%H')
    now_time_num = float(now_time)
    greet = 'hello'
    if 4 <= now_time_num <= 6:
        greet = '这么早过来，真是让我惊讶。需要帮忙么'
    if 7 <= now_time_num <= 8:
        greet = '这个时间段你应该去吃饭或者上课什么的...为什么来这里？有什么需要做的么'
    if 9 <= now_time_num <= 10:
        greet = '上午好，打起精神来。需要我做什么？'
    if 11 <= now_time_num <= 12:
        greet = '记得吃饭哦。'
    if 13 <= now_time_num <= 17:
        greet = "需要做什么？"
    if 18 <= now_time_num <= 23:
        greet = '加油，WangBenRen'
    if 0 <= now_time_num <= 3:
        greet = '你该睡觉了哦，速战速决。'
    return greet


# 存储和加载历史使用的是接送文件，是比起txt更能让电脑读懂的表格
# memory past chats
def save_history():
    # with用于管理资源，确保资源被正常打开关闭。with有关闭文件的作用
    with open('history_user.json', 'w', encoding='utf-8') as f:
        json.dump(history_user, f, ensure_ascii=False, indent=2)


# read past chats
def load_history():
    global history_user
    try:
        with open('history_user.json', 'r', encoding='utf-8') as f:
            history_user = json.load(f)
    except FileNotFoundError:
        history_user = []


# content
def code_assistant(prompt):
    #
    history_user.append(
                        {'role': 'user',
                         'content': f'你是一个专业的Python代码助手，请帮我解决以下问题：{prompt}'
                         }
                        )
    response = ollama.chat(
        model='deepseek-r1:1.5b',
        messages=history_user
                           )
    # message是整条回复包裹，包含角色和content，content是Ai回复内容
    ai_history = response['message']['content']
    history_user.append(
                        {'role': 'assistant',
                         'content': ai_history
                         }
                        )
    # 执行一次对话后会触发‘save’函数，进行保存
    save_history()
    return response['message']['content']


if __name__ == "__main__":
    greeting = time_greeting()
    print("%s，WangBenRen" % greeting)
    load_history()
    while True:
        user_input = input("WangBenRen：")
        if user_input.lower() == 'over':
            break
        result = code_assistant(user_input)
        print("玄歌：", result)
