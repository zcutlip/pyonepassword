FROM python:3.8

RUN pip install tox
RUN useradd -ms /bin/bash unpriv

USER unpriv
ENV TOX_WORKDIR=.tox-docker
ENV TESTDIR=/usr/src/testdir
COPY test.sh /test.sh
CMD [ "/test.sh" ]
