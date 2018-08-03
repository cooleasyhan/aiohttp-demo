 FROM python:3.6
 ENV PYTHONUNBUFFERED 1
 ENV PYTHONPATH .:$PYTHONPATH
 RUN mkdir -p /u01/report_server
 WORKDIR /u01/report_server
 ADD requirements.txt /u01/report_server/ 
 RUN pip install -r requirements.txt -i http://pypi.douban.com/simple/  --trusted-host pypi.douban.com
 RUN pip install gunicorn -i http://pypi.douban.com/simple/  --trusted-host pypi.douban.com
 ADD . /u01/report_server/
 ADD config/config_prod.yml config/config.yml
 RUN mkdir -p /data/logs
 EXPOSE 8080
 ENTRYPOINT [ "/usr/local/bin/gunicorn","main.main:gunicorn_app", "-k", "aiohttp.GunicornWebWorker"  ]
 CMD ["-b", "0.0.0.0:8080"  ,"-w" ,"2", "--log-config=config/log_info.conf" ]