FROM zhaoliu09/tensorflow-gpu
MAINTAINER liulianjushi@126.com
RUN mkdir /root/tea_weeds_server
WORKDIR /root/tea_weeds_server
ADD  ./ /root/tea_weeds_server
RUN pip3 --no-cache-dir install -r requirements.txt;\
    apt-get autoremove && apt-get autoclean ;\
    rm -rf /var/lib/apt/lists/*
CMD ["python3", "tea_weed_server.py"]
