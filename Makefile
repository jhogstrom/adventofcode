year=$(shell date +%Y)
day?=$(shell date +%d)

foo:
	@echo $(year) $(day)

$(year):
	mkdir -p $@

$(year)/dec$(day).py:
	python newday.py --year=$(year) --day=$(day)
# 	cp templates/decXX.py $@

$(year)/dec$(day)_test.txt:
	cp templates/decXX_test.txt $@

today: $(year) $(year)/dec$(day).py $(year)/dec$(day)_test.txt
	code $(year)/dec$(day).py $(year)/dec$(day)_test.txt
	@echo "Today's file is $(year)/dec$(day).py"
