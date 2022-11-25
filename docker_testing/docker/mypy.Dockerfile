FROM python:3.10

RUN pip install tox
RUN pip install mypy
RUN useradd -ms /bin/bash unpriv

USER unpriv
ENV TOX_WORKDIR=.tox-docker
ENV TESTDIR=/usr/src/testdir
ENV PYTEST_ENV=mypy
COPY test.sh /test.sh
CMD [ "/test.sh" ]
