python版本：3.4.0

python需要组件：
chromedriver (2.24.1)
selenium (3.11.0)
redis (2.10.6)
pillow

python安装组件：
pip install selenium
pip install chromedriver
pip install redis
pip install pyvirtualdisplay
pip install pillow


机器上需要的软件：
一、chrome安装：
1、增加google源
在/etc/yum.repos.d目录下，创建文件google-chrome.repo，并增加以下内容：
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
2、安装
yum -y install google-chrome-stable

二、chrome driver下载：
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
% unzip chromedriver_linux64.zip

三、
yum update
yum install Xvfb
yum install libXfont
yum install xorg-x11-fonts*


机器需要安装字体：
yum install freetype*
yum install cjkuni-ukai-fonts
不行就Google查一下别的字体库安装一下

