FROM python:3.9

RUN pip install tox

ENV TOX_WORKDIR=.tox-docker
ENV TESTDIR=/usr/src/testdir
COPY test.sh /test.sh
ENTRYPOINT [ "/test.sh" ]
