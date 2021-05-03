# coding=utf-8
import os

import xlrd

# 打开文件
data = xlrd.open_workbook('C:/Users/Egqawkq/Desktop/快速握拳.xlsx')

# 通过文件名获得工作表,获取工作表1
table = data.sheet_by_name('Sheet1')

# 获取行数和列数
row, col = table.nrows, table.ncols

# 获取整行的值和整列的值，返回的结果为数组
col1 = table.col_values(1)
col5 = table.col_values(5)

print('下列标定存在问题：')
for i in range(1, len(col1)):
    if col5[i] == '':
        print('(line: ' + str(i + 1) + ')', col1[i])
    else:
        flag_judge = int(col5[i])
        flag_exist = 0
        if os.path.exists('Y:/Save_data/' + col1[i] + '/hand_movements.json') == False:
            flag_exist = 0
        else:
            flag_exist = 1
        if flag_exist != flag_judge:
            print('(line: ' + str(i + 1) + ')', col1[i])
