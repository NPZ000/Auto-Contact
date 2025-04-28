# BOSS直聘网站自动打招呼

## 声明
本项目仅供学习交流使用，勿作商业或非法用途。

所有用户个人行为与本项目无关。

## 环境准备
1. 安装 python3
2. 更新 Google 浏览器到最新版本
3. 安装 Selenium
   ```shell script
   $ pip3 install selenium
   ```
4. 安装 Google 的 Driver
    https://googlechromelabs.github.io/chrome-for-testing/
    - 点击 Stable
    - 找到对应你电脑对应版本的chromedriver，复制后面的 url，另外打开一个页面复制到地址栏，按回车
    - 下载下来之后解压打开，双击里面的exe文件，mac系统如果报错有风险，问一下deepseek怎么解决
    - 移动到系统路径（看不懂就问问deepseek怎么安装chromedriver）
        1. 打开终端，执行： sudo mv /path/to/chromedriver /usr/local/bin/
        （需输入密码，/path/to/chromedriver 替换为实际路径，如 ~/Downloads/chromedriver-mac-x64/chromedriver）
        2. 赋予执行权限
            sudo chmod +x /usr/local/bin/chromedriver
        3. 验证安装
            chromedriver --version
5. 在BOSS手机端设置点击立即沟通就自动发送打招呼语
    - 在设置 -> 打招呼语里面，进去就能看到了
6. 登录 BOSS的 PC 端网站拿 cookie
    - 打开控制台，点击Application，找到cookie，找到里面有个key=wt2的，复制他的value，粘贴到代码中对应的位置（搜‘wt2的值粘贴到这里’）
7. 运行程序
   ```shell script
   $ python3 main.py
   ``` 
8. 正常流程
    - 自动打开网站boss
    - 会刷新一下登录到自己的账号上
    - 会点击职位按钮，跳转到职业页面上
    - 然后就会点击下面的职位卡片
    - 会出现一个弹窗，提示已自动打招呼，
    - 然后弹窗会消失，继续点击下一个，重复