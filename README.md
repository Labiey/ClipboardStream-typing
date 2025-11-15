# Clipboard Stream-typing 剪贴板流式输出 
做这个项目的原因是因为某些网站或应用的对话框中不允许直接粘贴内容（说你呢批改网学习通，在其他编辑器里写好的内容不能直接粘贴）。且以往的修改html的方法已经部分失效，故本项目采用模拟键盘输入的方法将你剪贴板的内容逐字输出进行粘贴（支持UFT-8字符）
## 使用库
- *pyperclip* 用于读取剪贴板
- *time* 用于控制输出速度
- *random* 用于随机延迟
- *pynput keyboard* 用于键盘监听、热键和输入模拟
- *json* 用于读取config.json
- *os* 用于定位config.json位置
## 使用方法 
直接打开`ClipboardStream-typing_0.1_.exe`或者使用`python ClipboardStream-typing_0.1_.py`运行代码。命令框提示以下内容。其中快捷键和等待时间可以在config.json中修改
```
配置文件加载成功：C:\Users\Labie\Desktop\mkdir\VScode\python\dist\config.json
脚本已启动。按 ctrl+s 开始输入（确保焦点在目标窗口）。
输入过程中，按 esc 退出。
按 ctrl+alt+r 重新读取剪贴板。
剪贴板内容已读取：'example_text'
```
然后按照提示进行操作即可
# 未来计划
- [ ] 增加对英文的支持 
- [ ] 运行读取同目录下的text.txt作为输出内容 