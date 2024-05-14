# AI powered typing assistant with OpenAI

## 全新制作 / New Creation

(English version below)

此分支使用了 OpanAI 的 API 方案，以供在线使用。请先设置好 `.env` 配置文件。

换用了一套更可靠的全局热键监听模组，`Ctrl+F9` 在我的 PC 上工作良好。

改变了工作逻辑，不再模拟剪贴板操作。要处理的文本就是事先已经在剪贴板中复制好的，处理结束后也应手动粘贴。如此可以最大程度避免误操作。

提供一个 PySimpleGUI 界面，供临时编辑需处理的文本。极具扩展性，使用下拉选单以决定处理方案，所有提示词在源码中可供增减或修改，改正、优化、翻译均可在一处完成。

现在你需要：

```
pip install pyperclip global-hotkeys pysimplegui opanai python-dotenv
```

(English)

This branch uses OpenAI's API for online use. Please set up the `.env` configuration file first.

A reliable global hotkey module was used, with `Ctrl+F9` working well on my PC.

The working logic has been changed, no longer simulating clipboard operations. The text to be processed is the one that has been copied beforehand and placed in the clipboard, and after processing is completed, it should be manually pasted. This can avoid mistakes to the greatest extent.

A PySimpleGUI interface is provided for temporary editing of the text to be processed. It is highly extensible, using drop-down menus to determine the processing scheme, with all prompts available for modification or addition in the source code. All corrections, optimizations, and translations can be completed in one place.

Now you need:

```
pip install pyperclip global-hotkeys pysimplegui openai python-dotenv
```

## 原作自述 / Original README

A script that can run in the background and listen to hotkeys, then uses a Large Language Model to fix the text. Less than 100 lines of code.

Inspired by this tweet:

https://twitter.com/karpathy/status/1725553780878647482

> "GPT is surprisingly good at correcting minor typos, so you can write really really fast, ignore mistakes and keep going, and it comes out just fine." - Andrej Karpathy

You'll find a demo and step-by-step code explanations on my YouTube channel:

 [![Alt text](https://img.youtube.com/vi/IUTFrexghsQ/hqdefault.jpg)](https://youtu.be/IUTFrexghsQ)

### Get Started

#### 1. Set up Ollama

Ollama Installation: https://github.com/ollama/ollama

Run `ollama run mistral:7b-instruct-v0.2-q4_K_S`

Mistal 7B Instruct works well for this task, but feel free to try other models, too :)

#### 2. Install dependencies
```
pip install pynput pyperclip httpx
```

- pynput: https://pynput.readthedocs.io/en/latest/
- pyperclip: https://github.com/asweigart/pyperclip
- httpx: https://github.com/encode/httpx/

#### 3. Run it

Start the assistant:

```
python main.py
```

Hotkeys you can then press:

- F9: Fixes the current line (without having to select the text)
- F10: Fixes the current selection

**Note**: You may get an error the first time saying `This process is not trusted! Input event monitoring will not be possible until it is added to accessibility clients`. On Mac, you need to add the script (IDE/terminal) both on accessibility and input monitoring.

**Note**: The code works on macOS. The underlying shortcuts in the code like Cmd+Shift+Left, Cmd+C, Cmd+V might have to be changed for Linux & Windows (e.g. `Key.cmd` -> `Key.ctrl`).

### Customize

Hotkeys, prompt, and Ollama config can be easily customized and extended in the code.

For example, here are some prompt templates you can try:

```python
from string import Template

PROMPT_TEMPLATE_FIX_TEXT = Template(
    """Fix all typos and casing and punctuation in this text, but preserve all new line characters:

$text

Return only the corrected text."""
)

PROMPT_TEMPLATE_GENERATE_TEXT = Template(
    """Generate a snarky paragraph with 3 sentences about the following topic:

$text

Return only the corrected text."""
)

PROMPT_TEMPLATE_SUMMARIZE_TEXT = Template(
    """Summarize the following text in 3 sentences:

$text

Return only the corrected text."""
)
```
