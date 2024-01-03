#!/usr/bin/env python3
import json
def count_table(table):
    num_rows = len(table)
    num_cols = len(table[0])  

    column_sums = [0] * num_cols
    for col in range(num_cols):
        for row in range(num_rows):
            column_sums[col] += table[row][col]

    row_sums = []
    
    for row in range(num_rows):
        print(table[row])
        row_sum = sum(table[row])
        row_sums.append(row_sum)
    return column_sums, row_sums


with open("bugs.json", 'r') as of:
    d = json.load(of)


d_status = {
   'postgis':   {'fixed': [], 'verified': [], 'reported': [], 'duplicate': []}, 
   'libgeos':   {'fixed': [], 'verified': [], 'reported': [], 'duplicate': []}, 
   'duckdb':    {'fixed': [], 'verified': [], 'reported': [], 'duplicate': []}, 
   'mysql':     {'fixed': [], 'verified': [], 'reported': [], 'duplicate': []}, 
   'sqlserver': {'fixed': [], 'verified': [], 'reported': [], 'duplicate': []}, 
}

d_type = {
    'postgis':   {'logic': {'fixed': [], 'verified': [],}, 'crash': {'fixed': [], 'verified': []}}, 
    'libgeos':   {'logic': {'fixed': [], 'verified': [],}, 'crash': {'fixed': [], 'verified': []}}, 
    'duckdb':    {'logic': {'fixed': [], 'verified': [],}, 'crash': {'fixed': [], 'verified': []}}, 
    'mysql':     {'logic': {'fixed': [], 'verified': [],}, 'crash': {'fixed': [], 'verified': []}}, 
    'sqlserver': {'logic': {'fixed': [], 'verified': [],}, 'crash': {'fixed': [], 'verified': []}}, 
}


for bug in d:
    d_status[bug['dbms']][bug['status']].append(bug['number'])
    if bug['status'] in ['fixed', 'verified']:
        d_type[bug['dbms']][bug['type']][bug['status']].append(bug['number'])

table_status = [[0 for _ in range(0,4)] for _ in range(0, 4)]
table_status[0][0] = len(d_status['postgis']['fixed']) + len(d_status['libgeos']['fixed'])
table_status[0][1] = len(d_status['postgis']['verified']) + len(d_status['libgeos']['verified'])
table_status[0][2] = len(d_status['postgis']['reported']) + len(d_status['libgeos']['reported'])
table_status[0][3] = len(d_status['postgis']['duplicate']) + len(d_status['libgeos']['duplicate'])
table_status[1][0] = len(d_status['duckdb']['fixed'])
table_status[1][1] = len(d_status['duckdb']['verified'])
table_status[1][2] = len(d_status['duckdb']['reported'])
table_status[1][3] = len(d_status['duckdb']['duplicate'])
table_status[2][0] = len(d_status['mysql']['fixed'])
table_status[2][1] = len(d_status['mysql']['verified'])
table_status[2][2] = len(d_status['mysql']['reported'])
table_status[2][3] = len(d_status['mysql']['duplicate'])
table_status[3][0] = len(d_status['sqlserver']['fixed'])
table_status[3][1] = len(d_status['sqlserver']['verified'])
table_status[3][2] = len(d_status['sqlserver']['reported'])
table_status[3][3] = len(d_status['sqlserver']['duplicate'])

column_sums, row_sums = count_table(table_status)
sum_status = sum(row_sums)
status = f'''
    PostGIS     & {table_status[0][0]} & {table_status[0][1]} & {table_status[0][2]} & {table_status[0][3]} & {row_sums[0]} \\\\
    MySQL       & {table_status[2][0]} & {table_status[2][1]} & {table_status[2][2]} & {table_status[2][3]} & {row_sums[2]} \\\\
    DuckDB      & {table_status[1][0]} & {table_status[1][1]} & {table_status[1][2]} & {table_status[1][3]} & {row_sums[1]} \\\\
    SQL Server  & {table_status[3][0]} & {table_status[3][1]} & {table_status[3][2]} & {table_status[3][3]} & {row_sums[3]} \\\\
    \midrule
    Sum & \\textbf{'{' + str(column_sums[0]) + '}'} & \\textbf{'{' + str(column_sums[1]) + '}'} & \\textbf{'{' + str(column_sums[2]) + '}'}  & \\textbf{'{' + str(column_sums[3]) + '}'} & \\textbf{'{' + str(sum_status) + '}'}\\\\
'''
print(status)

table_type = [[0 for _ in range(0,4)] for _ in range(0, 4)]

table_type[0][0] = len(d_type['postgis']['logic']['fixed']) + len(d_type['libgeos']['logic']['fixed'])
table_type[0][1] = len(d_type['postgis']['logic']['verified']) + len(d_type['libgeos']['logic']['verified'])  
table_type[0][2] = len(d_type['postgis']['crash']['fixed']) + len(d_type['libgeos']['crash']['fixed'])    
table_type[0][3] = len(d_type['postgis']['crash']['verified']) + len(d_type['libgeos']['crash']['verified']) 
table_type[1][0] = len(d_type['duckdb']['logic']['fixed'])
table_type[1][1] = len(d_type['duckdb']['logic']['verified'])
table_type[1][2] = len(d_type['duckdb']['crash']['fixed'])
table_type[1][3] = len(d_type['duckdb']['crash']['verified'])
table_type[2][0] = len(d_type['mysql']['logic']['fixed'])
table_type[2][1] = len(d_type['mysql']['logic']['verified'])
table_type[2][2] = len(d_type['mysql']['crash']['fixed'])
table_type[2][3] = len(d_type['mysql']['crash']['verified'])

column_sums, row_sums = count_table(table_type)
sum_type = sum(row_sums)

type = f'''
    PostGIS     & {table_type[0][0]} & {table_type[0][1]} & {table_type[0][2]} & {table_type[0][3]} & {row_sums[0]} \\\\
    MySQL       & {table_type[2][0]} & {table_type[2][1]} & {table_type[2][2]} & {table_type[2][3]} & {row_sums[2]} \\\\
    DuckDB      & {table_type[1][0]} & {table_type[1][1]} & {table_type[1][2]} & {table_type[1][3]} & {row_sums[1]} \\\\
    \midrule
    Sum & \\textbf{'{' + str(column_sums[0]) + '}'} & \\textbf{'{' + str(column_sums[1]) + '}'} & \\textbf{'{' + str(column_sums[2]) + '}'}  & \\textbf{'{' + str(column_sums[3]) + '}'} & \\textbf{'{' + str(sum_type) + '}'}\\\\
'''
print(type)