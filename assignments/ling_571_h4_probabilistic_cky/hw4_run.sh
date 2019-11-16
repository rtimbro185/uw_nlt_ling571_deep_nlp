#!/bin/bash
##### Constants
TITLE="LING 571 Homework 4 Execution script"
RIGHT_NOW=$(date +"%x %r %Z")
TIME_STAMP="Updated on $RIGHT_NOW by $USER"
PY_ENV="/opt/python-3.4.1/bin/python3.4"
##################### Functions
echo ${TITLE}
echo ${RIGHT_NOW} 
function pcfgGrammarInduction()
{ 
${PY_ENV} ./hw4_topcfg.py parses.train hw4_trained.pcfg
}
pcfgGrammarInduction
function pckyParserBaseLine()
{ 
${PY_ENV} ./hw4_parser.py hw4_trained.pcfg sentences.txt parses_base.out
}
pckyParserBaseLine
function evalbBaseLine()
{ 
./tools/evalb -p ./tools/COLLINS.prm ./tools/parses.gold ./parses_base.out > ./parses_base.eval
}
evalbBaseLine
function pcfgGrammarInductionImprove()
{
${PY_ENV} ./hw4_topcfg_improved.py parses.train hw4_trained_improved.pcfg
}
pcfgGrammarInductionImprove
function pckyParserImprove()
{ 
${PY_ENV} ./hw4_parser.py hw4_trained.pcfg sentences.txt parses_improved.out
}
pckyParserImprove
evalbImprove()
{ 
./tools/evalb -p ./tools/COLLINS.prm ./tools/parses.gold ./parses_improved.out > ./parses_improved.eval
}