import pyperclip  # 读取剪贴板
import time        # 控制输出速度
import random      # 随机延迟
from pynput import keyboard  # 键盘监听、热键和输入模拟
import json
import os
import sys

# 读取配置文件
def resource_path(relative_path: str) -> str:
    """返回资源的绝对路径：冻结时使用 exe 同目录，未冻结时使用脚本目录。"""
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

try:
    config_path = resource_path('config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    hotkey_config = config['hotkeys']
    delay_config = config['delay']
    start_delay_s = config.get('start_delay_s', 0.5)
    print(f"配置文件加载成功：{config_path}")
except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
    print(f"警告: 配置文件加载失败 ({e})，路径：{config_path}。将使用默认设置。")
    # 如果配置文件有问题，使用默认值
    hotkey_config = {
        "start": "ctrl+s",
        "exit": "esc",
        "reload": "ctrl+alt+r"
    }
    delay_config = {
        "min_s": 0.007,
        "max_s": 0.02
    }
    start_delay_s = 0.5  # 默认启动延迟

# 全局标志，用于控制输入过程
is_running = False
should_exit = False

# 读取剪贴板内容（在脚本启动时读取）
text = pyperclip.paste()

# 创建键盘控制器（用于模拟输入，支持Unicode如中文）
controller = keyboard.Controller()

# 定义启动热键的回调函数
def on_start():
    global is_running
    if not is_running:
        is_running = True
        print("程序启动，请将焦点放置在在目标窗口")

# 定义退出热键的回调函数
def on_exit():
    global should_exit
    should_exit = True
    print("收到退出信号，停止输入...")

# 定义重新读取剪贴板函数
def on_reload():
    global text
    text = pyperclip.paste()  # 重新从剪贴板读取内容，更新用于输入的变量
    print("已重新读取剪贴板内容。剪贴板预览：", text[:50] + "...ace back" if len(text) > 50 else text)

# --- 从配置中设置热键 ---
def parse_hotkey(key_string):
    """将 'ctrl+alt+s' 格式的字符串转换为 pynput 可接受的 '<ctrl>+<alt>+s' 格式"""
    # 定义需要用尖括号包围的特殊键
    special_keys = {'esc', 'space', 'enter', 'tab', 'shift', 'ctrl', 'alt', 'cmd'}
    # 动态添加 F1-F12
    for i in range(1, 13):
        special_keys.add(f'f{i}')

    parts = key_string.lower().split('+')
    
    parsed_parts = []
    for part in parts:
        part = part.strip()  # 去除可能存在的空格
        if part in special_keys:
            # 如果是特殊键，用尖括号包围
            parsed_parts.append(f'<{part}>')
        else:
            # 普通按键直接使用
            parsed_parts.append(part)
            
    # 用 '+' 重新组合
    return '+'.join(parsed_parts)

hotkey_start = keyboard.HotKey(keyboard.HotKey.parse(parse_hotkey(hotkey_config['start'])), on_start)
hotkey_exit = keyboard.HotKey(keyboard.HotKey.parse(parse_hotkey(hotkey_config['exit'])), on_exit)
hotkey_reload = keyboard.HotKey(keyboard.HotKey.parse(parse_hotkey(hotkey_config['reload'])), on_reload)


# 键盘监听器（用于检测热键）
def on_press(key):
    hotkey_start.press(listener.canonical(key))
    hotkey_exit.press(listener.canonical(key))
    hotkey_reload.press(listener.canonical(key))

def on_release(key):
    hotkey_start.release(listener.canonical(key))
    hotkey_exit.release(listener.canonical(key))
    hotkey_reload.release(listener.canonical(key))

# 主函数：启动监听并处理输入
print(f"脚本已启动。按 {hotkey_config['start']} 开始输入（确保焦点在目标窗口）。")
print(f"输入过程中，按 {hotkey_config['exit']} 退出。")
print(f"按 {hotkey_config['reload']} 重新读取剪贴板。")
print("剪贴板内容已读取：", text[:50] + "..." if len(text) > 50 else text)  # 显示前50字符预览

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    while True:
        if is_running:
            time.sleep(start_delay_s)  # 在启动后延迟
            # 开始输入循环
            for char in text:
                if should_exit:
                    break  # 如果收到退出信号，立即停止
                
                controller.type(char)  # 使用 pynput 输出单个字符（支持中文等Unicode）
                # 使用配置文件中的随机延迟
                delay_s = random.uniform(delay_config['min_s'], delay_config['max_s'])
                time.sleep(delay_s)
            
            # 输入完成后或退出时，重置标志
            is_running = False
            should_exit = False
            print("输入完成或已停止！")
        
        time.sleep(0.1)  # 小延迟，减少CPU占用，等待下一次启动

# 注意：脚本会一直运行，直到手动停止
