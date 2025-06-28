# Brute-force Dictionary Generator / 暴力破解字典生成器

## 项目简介 / Project Introduction

本项目是一个用于批量生成暴力破解密码字典的 Python 工具，支持多种字符组合和自定义密码长度，适合安全测试、密码学研究等场景。  
This project is a Python tool for generating password dictionaries for brute-force cracking, supporting various character combinations and custom password lengths. It is suitable for security testing, cryptography research, etc.

### 主要功能 / Features

- 支持生成仅数字、仅英文字母、仅大写、仅小写、数字和英文字母混合等多种字典类型  
  Supports numbers only, letters only, uppercase only, lowercase only, or mixed numbers and letters
- 可自定义密码长度，自动分批写入多个txt文件，适合大规模字典生成  
  Customizable password length, automatically splits output into multiple txt files for large-scale generation
- 多进程加速，充分利用多核CPU  
  Multiprocessing acceleration to fully utilize multi-core CPUs
- 兼容Windows命令行和pyinstaller打包为exe后直接双击运行  
  Compatible with Windows command line and can be packaged as an exe with pyinstaller for double-click execution
- 输入校验和异常处理，防止崩溃或死循环  
  Input validation and exception handling to prevent crashes or infinite loops

### 使用方法 / Usage

1. 运行 `generate a ictionary for brute force cracking.py`，或用 pyinstaller 打包为 exe 后双击运行  
   Run the script directly, or package it as an exe with pyinstaller and double-click to run
2. 按提示输入字典类型和密码长度  
   Follow the prompts to input dictionary type and password length
3. 程序会自动生成字典文件到当前目录  
   The program will automatically generate dictionary files in the current directory

### 注意事项 / Notes

- 大规模字典生成会占用大量磁盘空间和CPU资源，请根据实际需求设置合适的密码长度  
  Large-scale dictionary generation will consume a lot of disk space and CPU resources. Please set the password length appropriately.
- 仅供学习和安全测试用途，禁止用于非法用途  
  For learning and security testing purposes only. Do not use for illegal activities.
<p> |    </p>
<p> |    </p>                  
<p> |    </p>                    




<p><font size=2>这个项目十分简单，就一个文件。纯Python，谁都可以做出来。</font></p>
<p><font size=2>This project is very simple, just one file. Pure Python, anyone can do it.</font></p>
<p><font size=2>目前只可以在Windows上运行，如果要在其他操作系统上运行，只需要把源代码中的路径改为Linux、macOS的路径。</font></p>
<p><font size=2>Currently, it can only run on Windows, if you want to run it on other operating systems, you just need to change the path in the source code to, macOS path.</font></p>
<p><font size=2>这项目我只是草草地做了出来，所有可能会有大量的bug。</font></p>
<p><font size=2>I just threw this project together, so there might be a lot of bugs.</font></p>
<p><font size=2>如有改进意见请发邮件给:l846230@outlook.com</font></p>
<p><font size=2>If you have any suggestions for improvement, please send an email to: l846230@outlook.com</font></p>
