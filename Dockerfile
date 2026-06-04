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


# Default scripts
RUN wget https://raw.githubusercontent.com/dbca-wa/wagov_utils/main/wagov_utils/bin/default_script_installer.sh -O /tmp/default_script_installer.sh
RUN chmod 755 /tmp/default_script_installer.sh
RUN /tmp/default_script_installer.sh
# Install Python libs from requirements.txt.
COPY timezone /etc/timezone
ENV TZ=Australia/Perth
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
COPY nginx-default.conf /etc/nginx/sites-enabled/default

# Create local user
RUN groupadd -g 5000 oim
RUN useradd -g 5000 -u 5000 oim -s /bin/bash -d /app
RUN mkdir /app
RUN chown -R oim.oim /app

COPY startup.sh /

WORKDIR /app
USER oim
# Install the project (ensure that frontend projects have been built prior to this step).
COPY python-cron ./
RUN touch /app/.env

COPY --chown=oim:oim reporting_database_rebuild.sh /
COPY --chown=oim:oim open_reporting_db /

COPY --chown=oim:oim startup.sh /
COPY --chown=oim:oim reporting_database_rebuild.sh /
COPY --chown=oim:oim open_reporting_db /

# RUN service rsyslog start
RUN chmod 755 /open_reporting_db
RUN chmod 755 /reporting_database_rebuild.sh
RUN chmod 755 /startup.sh
EXPOSE 80
HEALTHCHECK CMD service cron status | grep "cron is running" || exit 1
CMD ["/startup.sh"]
                                                      

COPY --chown=oim:oim startup.sh /
COPY --chown=oim:oim reporting_database_rebuild.sh /
COPY --chown=oim:oim open_reporting_db /
