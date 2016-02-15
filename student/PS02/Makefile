#
# This file makes your submission when you type 'make'


# Set MODE for running on local or on hadoop

MODE="-rlocal"

# Directory containing fwiki
FWIKI=fwiki

# Directory containing fwiki and geolite
FWIKIGEO=fwikigeo

REPORT_PY=report1.py report2.py report3.py report4.py
REPORT_TXT=report1.txt report2.txt report3.txt report4.txt
JOIN_PY=join1.py join2.py join3.py 
JOIN_TXT=join1.txt join2.txt join3.txt 

report1.txt: report1.py
	python report1.py $(MODE) $(FWIKI) > report1.txt

report2.txt: report2.py
	python report2.py $(MODE) $(FWIKI) > report2.txt

report3.txt: report3.py
	python report3.py $(MODE) $(FWIKI) > report3.txt

report4.txt: report4.py
	python report4.py $(MODE) $(FWIKI) > report4.txt

join1.txt: join1.py
	python join1.py $(MODE) $(FWIKI) > join1.txt

join2.txt: join2.py
	python join2.py $(MODE) $(FWIKI) > join2.txt

join3.txt: join3.py
	python join2.py $(MODE) $(FWIKI) > join3.txt

ps02.zip: $(REPORT_PY) $(REPORT_TXT) $(JOIN_PY) $(JOIN_TXT)
	zip ps02.zip -u answers.txt report?.py report?.txt join?.py join?.txt

clean: 
	/bin/rm -f $(REPORT_TXT) $(JOIN_TXT)