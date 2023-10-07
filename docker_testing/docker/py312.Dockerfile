FROM python:3.12

RUN useradd -ms /bin/bash unpriv

USER unpriv
ENV PATH="/home/unpriv/.local/bin:${PATH}"
RUN pip install --upgrade --user pip

RUN whoami
RUN pip install "tox>=4" --user

ENV TOX_WORKDIR=.tox-docker
ENV TESTDIR=/usr/src/testdir
# PYVER_FACTOR gets passed to:
# tox run -f $PYVER_FACTOR
# so e.g., all py311-{something,something-else} envs get run
ENV PYVER_FACTOR=py311
COPY test.sh /test.sh
CMD [ "/test.sh" ]
