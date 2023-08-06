@echo off
REM
REM  Dave Skura, 2023
REM
REM  pip install zetl

echo  Restoring tables in MySQL

call py -m zetl.mysql_import sample7.csv restored_1s

REM call py -m zetl.mysql_import sample8.csv restored_sample8

REM call py -m zetl.mysql_import thistbl.csv restored_thistbl

pause



