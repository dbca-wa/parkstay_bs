# Prepare the base environment.
FROM ubuntu:22.04 as builder_base_container
MAINTAINER asi@dbca.wa.gov.au
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Australia/Perth
ENV PRODUCTION_EMAIL=True
ENV SECRET_KEY="ThisisNotRealKey"
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install --no-install-recommends -y wget git libmagic-dev gcc binutils libproj-dev gdal-bin python3 python3-setuptools python3-dev python3-pip tzdata cron nginx
RUN apt-get install --no-install-recommends -y libpq-dev patch
RUN apt-get install --no-install-recommends -y postgresql-client mtr htop vim ssh 
RUN ln -s /usr/bin/python3 /usr/bin/python 
#RUN ln -s /usr/bin/pip3 /usr/bin/pip
RUN pip install --upgrade pip
# Install Python libs from requirements.txt.

WORKDIR /app

# Install the project (ensure that frontend projects have been built prior to this step).
COPY timezone /etc/timezone
ENV TZ=Australia/Perth
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN touch /app/.env
COPY cron /etc/cron.d/container
COPY startup.sh /
COPY reporting_database_rebuild.sh /
COPY open_reporting_db /
COPY nginx-default.conf /etc/nginx/sites-enabled/default
# RUN service rsyslog start
RUN chmod 0644 /etc/cron.d/container
RUN crontab /etc/cron.d/container
RUN service cron start
RUN touch /var/log/cron.log
RUN service cron start
RUN chmod 755 /open_reporting_db
RUN chmod 755 /reporting_database_rebuild.sh
RUN chmod 755 /startup.sh
EXPOSE 80
HEALTHCHECK CMD service cron status | grep "cron is running" || exit 1
CMD ["/startup.sh"]
