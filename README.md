
>>简介

大概步骤就是：

将源文件放入相应位置，

然后在工程目录下打开命令行窗口，

进入python虚拟环境来执行python命令。

命令行的意思是：python执行脚本文件，-s指英文文件名称，-t指中文文件名称。

执行完成后，去result目录获取对齐结果。


## 使用步骤

1.将中英docx文件放入 `/home/wande/文档/docx/source/`

2.进入工程目录 `cd /home/wande/align/alignProject`

3.若使用xshell远程登录模式，可直接输入`conda activate align_env`，进入python虚拟环境；

4.若直接登录linux操作系统模式：则需要 "右键-打开shell" 进入代码模式后再进入虚拟环境

5.执行命令 `python disposeOneMain.py -s "xxx-en.docx" -t "xxx-en-CN.docx"`，待命令执行完成

6.从 `/home/wande/文档/docx/result/` 中获取对齐结果


###备注：
######文档根目录：`/home/wande/文档/docx/`
######程序根目录：`/home/wande/align/alignProject`
######对齐工具champollion tool kit（CTK）使用说明: https://blog.csdn.net/hengwen1991/article/details/79025740