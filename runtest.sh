#!/bin/bash
find . -name "*-cmat*" -exec rm -Rf {} \;
python main.py /home/accts/img22/Desktop/cmat-in/ /home/accts/img22/Desktop/cmat-out/
