FROM centos:7

LABEL MAINTAINER="Matthijs Risselada"

RUN rpm -Uhv https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm 
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y python-pip python36u python36u-libs python36u-devel python36u-pip

# RUN sudo yum install python-pip
#RUN yum install -y python36-setuptools && easy_install-3.6 pip

RUN yum install -y wget libXt gtk3 centos-indexhtml hunspell gtk2 liberation-fonts-common hunspell-en-US mozilla-filesystem xcb-util startup-notification liberation-sans-fonts wget bzip2 && yum clean all && rm -rf /var/cache/yum /usr/{games,src,tmp}

RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-linux64.tar.gz" -O /usr/bin/geckodriver.tgz && tar xvzf /usr/bin/geckodriver.tgz -C /usr/bin && rm -f /usr/bin/geckodriver.tgz

RUN wget -q "https://ftp.mozilla.org/pub/firefox/releases/61.0/linux-x86_64/en-US/firefox-61.0.tar.bz2" -O /usr/local/ff.bz2 && tar xvjf /usr/local/ff.bz2 -C /usr/local/ && rm -f /usr/local/ff.bz2

RUN wget -q "https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm" -O /usr/bin/google-chrome-stable_current_x86_64.rpm

RUN yum install -y /usr/bin/google-chrome-stable_current_x86_64.rpm

RUN wget -q "https://chromedriver.storage.googleapis.com/2.44/chromedriver_linux64.zip" -O /usr/local/chromedriver_linux64.zip

RUN yum install -y unzip

RUN unzip /usr/local/chromedriver_linux64.zip -d /usr/local/bin/ 

RUN pip3.6 install --upgrade pip && pip3.6 install selenium && pip3.6 install configparser && pip3.6 install untangle

RUN mkdir /var/ini /var/logs

WORKDIR /var/dumps

RUN wget -q "https://github.com/mkhage/IVS_Next/TC_01.py" -O /var/dumps/TC_01.py

RUN wget -q "https://github.com/mkhage/IVS_Next/page.py" -O /var/dumps/page.py

RUN wget -q "https://github.com/mkhage/IVS_Next/uitvoering_UI_BP_1.py" -O /var/dumps/uitvoering_UI_BP_1.py

RUN wget -q "https://github.com/mkhage/IVS_Next/voorbereiding_UI_BP_1.py" -O /var/dumps/voorbereiding_UI_BP_1.py

RUN wget -q "https://github.com/mkhage/IVS_Next/master/init.ini" -O /var/ini/init.ini

ENTRYPOINT ["python3.6", "/var/dumps/TC_01.py"]