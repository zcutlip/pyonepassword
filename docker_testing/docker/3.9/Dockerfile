FROM python:3.10

RUN pip install tox

ENV TOX_WORKDIR=.tox-docker
ENV TESTDIR=/usr/src/testdir
COPY test.sh /test.sh
CMD [ "/test.sh" ]
