To run this program, use Python 2.7.11 or above.
Can be executed in any Linux, unix or mac.

Summary of my approach (using database table concept here for easier description):
1. Read files, and convert it into multi-dimensional arrays (rows of records)
2.  Focus on relevant "columns" needed for output including group by key columns (CMTE_ID, 
ZIP_CODE, TRANSACTION_DT) , aggregate columns (TRANSACTION_AMT), and condition columns (OTHER_ID),
find out their index in the array of step 1.
3. For median by zip, it needs cumulative group by due to streaming so it needs to store accumulative values 
for sum/median of TRANSACTION_AMT. And we need to record one row for each original row including the 
required accumulative values. Count can be easily get from the length of the list in each group.
4. For median by date, it can be accomplished using groupby of itertools. The trick part is that one of group by key on
the zip code is on its first 5 characters. 
5. Once the lists of groupby and accumulative group by values are ready, just write the list into 
the required file name.

6. Can be improved on the following areas:
- space consideration since many columns are not used
- performance with different algorithms
- more generic on functions


To run:
1. from PROJECT_HOME/find-political-donors/insight_testsuite, execute ./run_tests.sh 
2. From PROJECT_HOME/find-political-donors, execut ./run.sh