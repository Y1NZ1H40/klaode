# klaode

一个用于在终端中以美化界面展示文本内容的小工具，界面风格参考 Claude 对话窗口，
基于 [Textual](https://github.com/Textualize/textual) 构建。

支持在文本中插入本地代码文件内容，模拟"正在和一个会写代码的 AI 对话"的效果。

## 快速开始

```bash
git clone https://github.com/Y1NZ1H40/klaode.git
cd klaode
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

klaode
```

默认会打开 `texts/` 目录下的示例文件 `example.txt`。

## 添加你自己的文本

把 `.txt` 文件放进 `texts/` 目录，然后运行：

```bash
klaode 你的文件名.txt
```

如果 `texts/` 目录下只有一个 `.txt` 文件，直接运行 `klaode` 即可，不用带文件名。

## 模拟插入代码

在 txt 文件中使用 `{{code:文件名}}` 占位符，klaode 会读取 `snippets/` 目录下
对应的代码文件，并把它替换成带语法高亮的代码块，展示效果就像是 AI 在对话中
写出了这段代码。参考 `texts/example.txt` 和 `snippets/example.py`。

## 项目结构

```
klaode/
├── src/klaode/
│   ├── app.py              # Textual 应用主体
│   ├── __main__.py         # 命令行入口
│   ├── config.py           # 目录路径配置
│   ├── content/
│   │   ├── loader.py       # 加载 txt 文件
│   │   ├── code_injector.py # 将本地代码文件注入文本
│   │   └── blocks.py       # 将文本切分为多个显示块
│   └── ui/
│       ├── widgets.py      # 对话气泡组件
│       └── theme.tcss      # 界面样式
├── texts/                  # 放置你自己的 txt 文件
├── snippets/               # 会被注入到对话中的代码文件
└── tests/                  # 单元测试
```

## 开发

```bash
pip install -e ".[dev]"
pytest
```
