# ToDo

# 11-15
## 1. 在笔记本环境中安装allure
## 2. 修改一下modified 文件，ignore一部分，push 一部分
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   main.py
        modified:   try.py
        modified:   ../CaseList/Runner.py
        modified:   ../ReportBat/GenerateReport.bat
        modified:   ../Todo.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        ../.idea/
        ../CaseList/__pycache__/
        ../PrivateLib/__pycache__/ADB.cpython-310.pyc
        ../testoutput/

no changes added to commit (use "git add" and/or "git commit -a")
---


 1. 修改unzip的代码，无参数化，固定src_zip，从ini文件中读取
 2. 在笔记本上试运行
 3. 挂载到服务器上试运行， 添加出发时间的机制
 4. 完善另外2个BT的case，
 5. 3个case都挂载到Jenkins上，试运行完整的集成测试
 6. 尝试在另外一台电脑上抓取最新的代码
 7. 建立另外一个project，专门放Mylog这些lib库
 8. change on 05/11

11-14
 1. 在download前，先看看full_web是否存在，不存在的话，就不用下了
 2. 如果1不存在，尝试看看倒数第二个版本是否存在，如果存在下载这个版本


former
1. 把report和result的位置放到ini里
2. 尝试调出history和trend
3. ~~重写upgrade，在PrivateLib.Serial的基础上~~
4. ~~尝试自寻找COM口，放弃，不利于代码稳定性~~
5. ~~serial的com口要么用4的方法解决，要么写进ini文件里，done~~