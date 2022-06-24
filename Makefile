HTML_COV_DIR=htmlcov
COV_REPORT_FILE=coverage-report.txt
NPROCS=$(shell nproc)

COV_STAMP=.cov_stamp
HTML_REPORT_STAMP=".html_report_stamp"

PYONEPASSWORD_SRC_FILES=$(shell find ./pyonepassword -name \*py -print)
PYONEPASSWORD_TEST_FILES=$(shell find tests -name \*pyc -prune -o  -name reports -prune -o -type f -print)

all:
	@echo "make pytest-coverage for coverage report"

pytest-coverage: $(HTML_REPORT_STAMP)

$(HTML_REPORT_STAMP): $(COV_STAMP)
	coverage html
	touch $@

coverage-report: $(COV_STAMP)
	coverage report > $(COV_REPORT_FILE)

$(COV_STAMP): $(PYONEPASSWORD_SRC_FILES) $(PYONEPASSWORD_TEST_FILES)
	pytest --cov=pyonepassword --cov-report= -n $(NPROCS)
	touch $@




clean-coverage:
	coverage erase
	-rm -r $(HTML_COV_DIR)
	-rm $(COV_STAMP)
	-rm $(HTML_REPORT_STAMP)
	-rm $(COV_REPORT_FILE)
