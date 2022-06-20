HTML_COV_DIR=htmlcov

NPROCS=$(shell nproc)

HTML_COV_STAMP=.html_cov_stamp

PYONEPASSWORD_SRC_FILES=$(shell find ./pyonepassword -name \*py -print)
PYONEPASSWORD_TEST_FILES=$(shell find tests -name \*pyc -prune -o  -name reports -prune -o -type f -print)

all:
	@echo "make pytest-coverage for coverage report"

pytest-coverage: $(HTML_COV_STAMP)

$(HTML_COV_STAMP): $(PYONEPASSWORD_SRC_FILES) $(PYONEPASSWORD_TEST_FILES)
	pytest --cov=pyonepassword --cov-report html -n $(NPROCS)
	touch $@



clean-coverage:
	coverage erase
	-rm -r $(HTML_COV_DIR)
