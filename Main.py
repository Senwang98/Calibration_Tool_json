import datetime
import glob
import json
import math
import os
import sys

import matplotlib.pyplot as plt
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor, QBrush
from PyQt5.QtWidgets import *

from Extract_skeleton_2 import *
from GUI import Ui_MainWindow
from Extract_from_json import *

class myMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)

        # 设置所有的按钮触发事件
        self.btn_open.clicked.connect(self.Open_file)

        self.btn_display_pause.clicked.connect(self.display_pause)

        self.process_bar.valueChanged.connect(self.Slider_move)

        self.btn_change.clicked.connect(self.Mode_change)

        self.btn_start_record.clicked.connect(self.Record_start)

        self.btn_end_record.clicked.connect(self.Record_end)

        self.btn_verify.clicked.connect(self.Verify)

        self.btn_action.clicked.connect(self.Start_record_action)

        self.btn_save.clicked.connect(self.Save_event)

        self.btn_lock.clicked.connect(self.Lock_event)

        self.btn_skeleton.clicked.connect(self.Display_skeleton)

        # 设置一些全局的列表
        self.time_stamp_version2 = []
        self.show_queue_version2 = []
        self.skeleton_list = []
        self.action_list = []
        self.each_frame_input = []

        # 设置一些全局变量
        self.cnt = -1
        self.start = None
        self.end = None
        self.open_flag = False
        self.change_flag = False
        self.IsDisplay = False
        self.file_address = None
        self.video_address = None
        self.max_col = 1
        self.verify_timer = QTimer()
        self.table1_ok = False
        self.id_name = ""
        self.action_name = ""
        self.lock_flag = True
        self.version = -1
        self.need_skeleton = True

    ############## 弹窗事件触发函数定义区
    def btn_display_pause_warning(self):
        QMessageBox.warning(self, "警告", "请先完成时间标定！", QMessageBox.Cancel)

    def btn_change_warning(self):
        QMessageBox.warning(self, "警告", "请先打开文件！", QMessageBox.Cancel)

    def btn_action_warning(self):
        QMessageBox.warning(self, "警告", "请先完成验证！", QMessageBox.Cancel)

    def btn_open_error(self):
        QMessageBox.critical(self, "错误", "未打开文件,默认播放上一次！")

    def btn_open_error2(self):
        QMessageBox.critical(self, "错误", "路径错误！")

    def btn_lock_on(self):
        QMessageBox.information(self, "提示", "表格锁定！", QMessageBox.Yes)

    def btn_lock_off(self):
        QMessageBox.information(self, "提示", "表格解锁！", QMessageBox.Yes)

    def btn_save_information(self):
        QMessageBox.information(self, "提示", "保存成功！", QMessageBox.Yes)

    def btn_save_warning(self):
        QMessageBox.warning(self, "警告", "请先点击标定动作按钮！", QMessageBox.Cancel)

    def skeleton_error(self):
        QMessageBox.warning(self, "警告", "骨架表标定错误！", QMessageBox.Cancel)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '提示', '是否退出？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if os.path.exists('result.jpg'):
                os.remove('result.jpg')
            event.accept()
        else:
            event.ignore()

    ############## 结束

    def Display_skeleton(self):
        """
            函数功能：是否需要显示骨架,骨架按钮的触发函数
        """
        if self.open_flag:
            self.need_skeleton ^= 1
            # print(self.need_skeleton)
            self.Show_pic()

    def Lock_event(self):
        """
            函数功能：锁定按钮的触发函数，实现是否有权修改上一次的保存数据
        """
        if self.open_flag:
            if self.lock_flag:
                self.lock_flag = False
                self.btn_lock_off()
            else:
                self.lock_flag = True
                self.btn_lock_on()

    def Save_event(self):
        """
            函数功能：对标定结束的数据进行保存
        """
        if self.table1_ok and self.open_flag and self.start is not None and self.end is not None:
            # 读取动作标定数据并保存在action_list中
            self.action_list.clear()
            for i in range(self.file_number):
                tmp = []
                for j in range(self.max_col):
                    if self.table2.item(i, j) is None or self.table2.item(i, j).text() == '':
                        pass
                    else:
                        tmp.append(eval(self.table2.item(i, j).text()))
                if len(tmp) == 0:
                    tmp.append(0)
                self.action_list.append(tmp)

            # 设置json的格式
            data = {
                'start': self.start,
                'end': self.end,
                'body': self.skeleton_list,
                'action': self.action_list
            }

            # get_id = self.file_address.split('/')
            # 获取文件保存路径
            Save_path = self.save_data + '/Save_data/' + self.id_name + '/'

            # 如果不存在该文件夹就新建一个
            if not os.path.exists(Save_path):
                os.makedirs(Save_path)

            with open(Save_path + self.action_name + '.json', 'w') as f:
                json.dump(data, f)
            self.btn_save_information()
        else:
            self.btn_save_warning()

    def Start_record_action(self):
        """
            函数功能：在标定开始与结束之后绘制相关关键点变化图，开始对动作进行标定
        """
        if self.open_flag and self.start is not None and self.end is not None and self.start >= 0:
            # 读取骨架序号数据并保存在skeleton_list中
            self.skeleton_list = []
            for i in range(self.file_number):
                if self.table.item(i, 0).text() == '':
                    self.skeleton_list.append(-1)
                else:
                    # 此处理论上不需要特判，但标定时只考虑单人识别，所以此处添加上
                    if self.table.item(i, 0).text() != '0' and self.table.item(i, 0).text() != '9' and self.table.item(
                            i, 0).text() != '-1':
                        # print(i,'error!')
                        self.skeleton_error()
                        return
                    else:
                        self.skeleton_list.append(eval(self.table.item(i, 0).text()))

            # 取消用户对于骨架标定图的权限，此时只能操作动作表
            self.table1_ok = True
            self.cnt = -1
            for i in range(self.file_number):
                self.table.item(i, 0).setBackground(QBrush(QColor(255, 255, 255)))

            # print(self.skeleton_list)

            # x表示帧序号，y表示一条直线的对应值，yy表示另一条，具体的y的个数取决于需要画多少曲线
            x = []
            y = []
            # yy = []

            x.clear()
            y.clear()
            # yy.clear()

            for i in range(self.start, self.end + 1):
                x.append(i)
                # 脸部
                y.append(extract_point_from_json(self.file_address, i, self.skeleton_list[i]))

                # # 快速握拳
                # l7 = self.Read_skeleton(i, self.skeleton_list[i], 7, 1)
                # l22 = self.Read_skeleton(i, self.skeleton_list[i], 22, 1)
                #
                # r11 = self.Read_skeleton(i, self.skeleton_list[i], 11, 1)
                # r24 = self.Read_skeleton(i, self.skeleton_list[i], 24, 1)
                #
                # dis1 = math.sqrt(
                #     (l7[0] - l22[0]) * (l7[0] - l22[0]) + (l7[1] - l22[1]) * (l7[1] - l22[1]) + (l7[2] - l22[2]) * (
                #             l7[2] - l22[2]))
                # dis2 = math.sqrt((r11[0] - r24[0]) * (r11[0] - r24[0]) + (r11[1] - r24[1]) * (r11[1] - r24[1]) + (
                #         r11[2] - r24[2]) * (r11[2] - r24[2]))
                #
                # y.append(dis1)
                # yy.append(dis2)

                # # 手掌反转
                # l22 = self.Read_skeleton(i, self.skeleton_list[i], 22)
                # y.append(l22[0])
                # r24 = self.Read_skeleton(i, self.skeleton_list[i], 24)
                # yy.append(r24[0])

                # # stomp
                # l22 = self.Read_skeleton(i, self.skeleton_list[i], 14)
                # y.append(l22[1])
                # r24 = self.Read_skeleton(i, self.skeleton_list[i], 18)
                # yy.append(r24[1])

            # 设置y轴显示范围
            miny, maxy = 1e9, -1e9
            for i in y:
                if abs(i + 100) >= 1e-2:
                    miny = min(i, miny)
                    maxy = max(i, maxy)

            # for i in yy:
            #     if abs(i + 100) >= 1e-2:
            #         miny = min(i, miny)
            #         maxy = max(i, maxy)

            plt.ylim([miny - 0.02, maxy + 0.02])
            plt.xlim([self.start, self.end])

            plt.plot(x, y)
            # plt.plot(x, yy)

            # 暂存绘制出的图片
            plt.savefig('result.jpg')
            plt.close()

            # 读取该绘制图片，并将该图片显示在label中
            tmp = cv2.imread('result.jpg')
            # 只截取部分是为了尽可能最大显示有效信息，此处写死了绝对大小，具体优化此处未实现
            img_rgb = tmp[50:450, 40:600]
            height1, width1 = img_rgb.shape[:-1]
            img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
            qimage1 = QtGui.QImage(img_rgb, width1, height1, width1 * 3, QtGui.QImage.Format_RGB888)
            self.show_pic3.setPixmap(QtGui.QPixmap(qimage1))
            self.Next_frame()
        else:
            self.btn_action_warning()

    def Record_start(self):
        """
            函数功能：记录当前帧为开始帧
            tips：此处未设置在标定动作时取消用户修改开始帧的权限，可以根据要求进行修改
        """
        if self.open_flag:
            self.start = self.cnt
            self.start_information.setText(str(self.start))
            self.start_information.setAlignment(Qt.AlignCenter)

    def Record_end(self):
        """
            函数功能：记录当前帧为结束帧
            tips：此处未设置在标定动作时取消用户修改结束帧的权限，可以根据要求进行修改
        """
        if self.open_flag:
            self.end = self.cnt
            self.end_information.setText(str(self.end))
            self.end_information.setAlignment(Qt.AlignCenter)

    def Verify(self):
        """
            函数功能：用于预先设置验证播放的所需设置
        """
        if self.open_flag and self.start is not None and self.end is not None and self.start >= 0 and self.table1_ok is False:
            self.skeleton_list = []
            for i in range(self.file_number):
                if self.table.item(i, 0).text() == '':
                    self.skeleton_list.append(-1)
                else:
                    self.skeleton_list.append(eval(self.table.item(i, 0).text()))
            self.show_pic1.clear()
            self.show_pic2.clear()
            self.cnt = self.start
            self.verify_timer.start()
            self.IsDisplay = True
        else:
            self.btn_display_pause_warning()

    def Verify_display(self):
        # 读取当前时间，以便于计算出每一帧显示消耗的时间
        start = datetime.datetime.now()

        if self.cnt > self.end:
            self.IsDisplay = False
            self.verify_timer.stop()
            return

        img_rgb = cv2.imread(self.file_address + '/kinect_color/' + str(self.show_queue_version2[self.cnt][1]) + '.jpg')
        height1, width1 = img_rgb.shape[:-1]
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        qimage1 = QtGui.QImage(img_rgb, width1, height1, width1 * 3, QtGui.QImage.Format_RGB888)
        self.show_pic1.setPixmap(QtGui.QPixmap(qimage1))

        img_dep = extract_sketelon_2(self.file_address, self.show_queue_version2[self.cnt][0],
                                     self.show_queue_version2[self.cnt][2], self.skeleton_list[self.cnt])
        height2, width2 = img_dep.shape[:-1]
        if self.change_flag:
            img_convt = cv2.applyColorMap(cv2.convertScaleAbs(img_dep, alpha=15), cv2.COLORMAP_JET)
            qimage2 = QtGui.QImage(img_convt, width2, height2, width2 * 3, QtGui.QImage.Format_RGB888)
            self.show_pic2.setPixmap(QtGui.QPixmap(qimage2))
        else:
            qimage2 = QtGui.QImage(img_dep, width2, height2, width2 * 3, QtGui.QImage.Format_RGB888)
            self.show_pic2.setPixmap(QtGui.QPixmap(qimage2))

        self.label_process.setText(str(self.cnt + 1) + ' / ' + str(self.file_number))
        end = datetime.datetime.now()

        # 设置延时
        if self.cnt == self.end or abs(self.time_stamp_version2[self.cnt + 1] - self.time_stamp_version2[self.cnt] - (
                end - start).microseconds / 1000.0) <= 1e-2:
            self.verify_timer.setInterval(0)
        else:
            self.verify_timer.setInterval(abs(int(
                self.time_stamp_version2[self.cnt + 1] - self.time_stamp_version2[self.cnt] - (
                        end - start).microseconds / 1000.0)))
        self.cnt += 1

    def display_pause(self):
        """
            函数功能：为了验证播放的时候可以暂停做设置
        """
        if self.open_flag and self.start is not None and self.end is not None:
            if self.IsDisplay:
                self.verify_timer.stop()
                self.IsDisplay = False
            else:
                self.verify_timer.start()
                self.IsDisplay = True
        else:
            self.btn_display_pause_warning()

    def Open_file(self):
        """
            函数功能：打开按钮的触发函数，用于第一步打开文件获取相关信息以及预处理等相关操作
        """
        self.file_address = QFileDialog.getExistingDirectory()

        if self.file_address:
            # 算出保存文件的路径
            pos_id = -1
            pos_action = -1
            cnt = 0
            for i in range(len(self.file_address) - 1, -1, -1):
                if self.file_address[i] == '/':
                    cnt += 1
                if cnt == 1 and pos_action == -1:
                    pos_action = i
                if cnt == 2:
                    pos_id = i
                    break

            self.save_data = self.file_address[:pos_id]
            self.id_name = self.file_address[pos_id + 1:pos_action]
            self.action_name = self.file_address[pos_action + 1:]

            self.video_address = self.file_address + '/kinect_color'
            # self.id_name = self.file_address.split('/')[-2]

            # 如果读取的文件并不存在或者无效就给出一个错误提示
            if not os.path.exists(self.video_address):
                self.btn_open_error2()
                return
            self.file_number = len(glob.glob(self.file_address + '/kinect_bodies/*.body'))

            # 导入上一次的数据
            if os.path.exists(self.save_data + '/Save_data/' + self.id_name + '/' + self.action_name + '.json'):
                with open(self.save_data + '/Save_data/' + self.id_name + '/' + self.action_name + '.json', 'r') as f:
                    # 解析json文件，返回字典
                    dic = json.load(f)
                    self.start = dic['start']
                    self.end = dic['end']
                    body = dic['body']
                    action = dic['action']
                # print(self.start)
                # print(self.end)
                # print(body)
                # print(action)
                ############# 设置表格1
                self.table.clear()
                self.table.setRowCount(self.file_number)
                self.table.setColumnCount(1)

                for i in range(self.file_number):
                    item_tmp = QTableWidgetItem(str(body[i]))
                    item_tmp.setFont(QFont("Times", 12, QFont.Black))
                    item_tmp.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, 0, item_tmp)

                self.table.setHorizontalHeaderLabels(['Body'])
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
                self.table.verticalScrollBar().setValue(0)
                # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                ############# 设置表格2
                self.table2.clear()
                self.table2.setRowCount(self.file_number)
                self.max_col = -1
                for i in action:
                    if self.max_col < len(i):
                        self.max_col = len(i)
                self.table2.setColumnCount(self.max_col)
                # 初始时table2默认是全是 0，所以长度为 1
                self.each_frame_input = []

                for i in range(self.file_number):
                    self.each_frame_input.append(len(action[i]))
                    for j in range(len(action[i])):
                        item_tmp = QTableWidgetItem(str(action[i][j]))
                        item_tmp.setFont(QFont("Times", 12, QFont.Black))
                        item_tmp.setTextAlignment(Qt.AlignCenter)
                        self.table2.setItem(i, j, item_tmp)

                # self.table2.setHorizontalHeaderLabels(['M1'])
                self.table2.resizeColumnsToContents()
                self.table2.resizeRowsToContents()
                self.table2.verticalScrollBar().setValue(0)
                # self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)

                ############### table2设置完成

                self.cnt = -1
                self.open_flag = True
                self.IsDisplay = False
                self.table1_ok = False
                self.lock_flag = True
                self.need_skeleton = True
                self.Timestamp_version2()
                self.verify_timer.timeout.connect(self.Verify_display)
                self.label_process.setText('0 / ' + str(self.file_number))
                self.show_pic3.clear()
                # print('当前编号：' + id_name)
                self.setWindowTitle('当前编号：' + self.id_name + '  当前动作：' + self.action_name)
                self.start_information.setText(str(self.start))
                self.start_information.setAlignment(Qt.AlignCenter)
                self.end_information.setText(str(self.end))
                self.end_information.setAlignment(Qt.AlignCenter)

            # 第一次标定该数据
            else:
                ############# 设置表格1
                self.table.clear()
                self.table.setRowCount(self.file_number)
                self.table.setColumnCount(1)

                for i in range(self.file_number):
                    item_tmp = QTableWidgetItem('-1')
                    item_tmp.setFont(QFont("Times", 12, QFont.Black))
                    item_tmp.setTextAlignment(Qt.AlignCenter)
                    self.table.setItem(i, 0, item_tmp)

                self.table.setHorizontalHeaderLabels(['Body'])
                self.table.resizeColumnsToContents()
                self.table.resizeRowsToContents()
                self.table.verticalScrollBar().setValue(0)
                # self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

                ############# 设置表格2
                self.table2.clear()
                self.table2.setRowCount(self.file_number)
                self.table2.setColumnCount(1)

                for i in range(self.file_number):
                    item_tmp = QTableWidgetItem('0')
                    item_tmp.setFont(QFont("Times", 12, QFont.Black))
                    item_tmp.setTextAlignment(Qt.AlignCenter)
                    self.table2.setItem(i, 0, item_tmp)

                # self.table2.setHorizontalHeaderLabels(['M1'])
                self.table2.resizeColumnsToContents()
                self.table2.resizeRowsToContents()
                self.table2.verticalScrollBar().setValue(0)
                # 初始时table2默认是全是 0，所以长度为 1
                self.each_frame_input = [1] * self.file_number
                # self.table2.setEditTriggers(QAbstractItemView.NoEditTriggers)
                # self.table2.setSelectionBehavior(QAbstractItemView.SelectRows)
                ############### table2设置完成
                self.cnt = -1
                self.open_flag = True
                self.IsDisplay = False
                self.max_col = 1
                self.table1_ok = False
                self.lock_flag = False
                self.need_skeleton = True
                self.Timestamp_version2()
                self.verify_timer.timeout.connect(self.Verify_display)
                self.label_process.setText('0 / ' + str(self.file_number))
                self.show_pic3.clear()
                # print('当前编号：' + id_name)
                self.setWindowTitle('当前编号：' + self.id_name + '  当前动作：' + self.action_name)

        else:
            self.btn_open_error()
            if self.video_address:
                tmp = self.video_address.split('/')
                for i in range(0, len(tmp) - 1):
                    self.file_address += tmp[i] + '/'

    def Timestamp_version2(self):
        """
            函数功能：因为骨架、rgb、depth的时间戳可能会存在不对应的现象，所以该函数用于时间戳的最优对齐
            tips：考虑到 body、color、depth的时间戳个数不一致，
                  所以此处顺次读取文件
        """
        # 获取Body的时间戳
        self.show_queue_version2.clear()
        self.time_stamp_version2.clear()

        fp = open(self.file_address + '/kinect_bodies/time_index.txt', 'r')
        while True:
            content = fp.readline().strip('\n').split()
            if content:
                content = content[-1].split(':')
                hour = eval(content[0][1]) + 10 * eval(content[0][0])
                minute = eval(content[1][1]) + 10 * eval(content[1][0])
                second = eval(content[2][5]) + 10 * eval(content[2][4]) + 100 * eval(content[2][3]) + 1000 * eval(
                    content[2][1]) + 10000 * eval(content[2][0])
                self.time_stamp_version2.append(hour * 3600000 + minute * 60000 + second)
            else:
                break
        self.time_stamp_version2.sort()
        fp.close()

        # 获取RGB的时间戳
        tmp_color = []
        fp = open(self.file_address + '/kinect_color/time_index.txt', 'r')
        while True:
            content = fp.readline().strip('\n').split()
            if content:
                content = content[-1].split(':')
                hour = eval(content[0][1]) + 10 * eval(content[0][0])
                minute = eval(content[1][1]) + 10 * eval(content[1][0])
                second = eval(content[2][5]) + 10 * eval(content[2][4]) + 100 * eval(content[2][3]) + 1000 * eval(
                    content[2][1]) + 10000 * eval(content[2][0])
                tmp_color.append(hour * 3600000 + minute * 60000 + second)
            else:
                break
        tmp_color.sort()
        fp.close()

        # 获取Depth的时间戳
        tmp_depth = []
        fp = open(self.file_address + '/kinect_depth/time_index.txt', 'r')
        while True:
            content = fp.readline().strip('\n').split()
            if content:
                content = content[-1].split(':')
                hour = eval(content[0][1]) + 10 * eval(content[0][0])
                minute = eval(content[1][1]) + 10 * eval(content[1][0])
                second = eval(content[2][5]) + 10 * eval(content[2][4]) + 100 * eval(content[2][3]) + 1000 * eval(
                    content[2][1]) + 10000 * eval(content[2][0])
                tmp_depth.append(hour * 3600000 + minute * 60000 + second)
            else:
                break
        tmp_depth.sort()
        fp.close()

        # 至此我拿到了三类时间戳，以body的时间戳为base
        # two-points problem，类似合并两个有序序列
        i, j, k = 0, 0, 0
        tmp_body = self.time_stamp_version2
        len1, len2, len3 = len(tmp_body), len(tmp_color), len(tmp_depth)
        # print(len1, len2, len3)

        for i in range(len1):
            record = [i]
            while True:
                if j >= len2:
                    record.append(len2 - 1)
                    break
                if tmp_body[i] > tmp_color[j]:
                    j += 1
                else:
                    if j == 0:
                        record.append(j)
                        break
                    else:
                        if tmp_color[j] - tmp_body[i] < tmp_body[i] - tmp_color[j - 1]:
                            record.append(j)
                            break
                        else:
                            record.append(j - 1)
                            j = j - 1
                            break
            while True:
                if k >= len3:
                    record.append(len3 - 1)
                    break
                if tmp_body[i] > tmp_depth[k]:
                    k += 1
                else:
                    if k == 0:
                        record.append(k)
                        break
                    else:
                        if tmp_depth[k] - tmp_body[i] < tmp_body[i] - tmp_depth[k - 1]:
                            record.append(k)
                            break
                        else:
                            record.append(k - 1)
                            k = k - 1
                            break

            self.show_queue_version2.append(record)
        # print(self.show_queue_version2)

    def Mode_change(self):
        """
            函数功能：响应伪彩色按钮，对深度图进行伪彩色图转换
        """
        if self.open_flag:
            if self.change_flag:
                self.change_flag = False
            else:
                self.change_flag = True
            self.Show_pic()
        else:
            self.btn_change_warning()

    def Slider_move(self):
        """
            函数功能：根据进度条的移动切换至相应帧
        """
        if self.open_flag:
            value = self.process_bar.value() * 1.0
            self.cnt = int(round(value / 100.0, 2) * self.file_number)
            if self.cnt == self.file_number:
                self.cnt = self.file_number - 1
            self.label_process.setText(str(self.cnt + 1) + ' / ' + str(self.file_number))
            # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
            if self.cnt <= 25:
                self.table.verticalScrollBar().setValue(0)
                self.table2.verticalScrollBar().setValue(0)
            else:
                self.table.verticalScrollBar().setValue(self.cnt - 15)
                self.table2.verticalScrollBar().setValue(self.cnt - 15)

            self.Show_pic()

    def Pre_frame(self):
        """
            函数功能：右击鼠标返回上一帧
        """
        if self.open_flag:
            self.cnt -= 1
            if self.cnt < 0:
                self.cnt = self.file_number - 1

            self.label_process.setText(str(self.cnt + 1) + ' / ' + str(self.file_number))
            if not self.table1_ok:
                if self.cnt <= 25:
                    self.table.verticalScrollBar().setValue(0)
                else:
                    self.table.verticalScrollBar().setValue(self.cnt - 15)

                if self.cnt == self.file_number - 1:
                    if self.table.item(self.cnt, 0) and self.table.item(0, 0) is not None:
                        self.table.item(0, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
                else:
                    if self.table.item(self.cnt + 1, 0) is not None and self.table.item(self.cnt, 0) is not None:
                        self.table.item(self.cnt + 1, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
            else:
                if self.cnt <= 25:
                    self.table2.verticalScrollBar().setValue(0)
                    self.table.verticalScrollBar().setValue(0)
                else:
                    self.table2.verticalScrollBar().setValue(self.cnt - 15)
                    self.table.verticalScrollBar().setValue(self.cnt - 15)

                if self.cnt == self.file_number - 1:
                    if self.table2.item(self.cnt, 0) and self.table2.item(0, 0) is not None:
                        self.table2.item(0, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table2.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
                        self.table.item(0, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
                else:
                    if self.table2.item(self.cnt + 1, 0) is not None and self.table2.item(self.cnt, 0) is not None:
                        self.table2.item(self.cnt + 1, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table2.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
                        self.table.item(self.cnt + 1, 0).setBackground(QBrush(QColor(255, 255, 255)))
                        self.table.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
                # self.high_light(1)
            self.Show_pic()

    def Next_frame(self):
        """
            函数功能：左击鼠标跳转至下一帧
        """
        if self.open_flag:
            self.cnt += 1
            if self.cnt >= self.file_number or self.cnt >= len(self.show_queue_version2):
                self.cnt = 0

            self.label_process.setText(str(self.cnt + 1) + ' / ' + str(self.file_number))

            if not self.table1_ok:
                if not self.lock_flag:
                    if self.cnt == 0 and self.table.item(0, 0).text() == '':
                        # 设置标定区当前标签为上一帧的标签
                        item_tmp = QTableWidgetItem("-1")
                        item_tmp.setFont(QFont("Times", 12, QFont.Black))
                        item_tmp.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(self.cnt, 0, item_tmp)
                        self.table.verticalScrollBar().setValue(0)
                        self.table.resizeColumnsToContents()
                        self.table.resizeRowsToContents()
                    elif self.cnt == 0 and self.table.item(0, 0).text() != '':
                        pass
                    else:
                        # 设置标定区当前标签为上一帧的标签
                        pre_text = self.table.item(self.cnt - 1, 0).text()
                        item_tmp = QTableWidgetItem(str(pre_text))
                        item_tmp.setFont(QFont("Times", 12, QFont.Black))
                        item_tmp.setTextAlignment(Qt.AlignCenter)
                        self.table.setItem(self.cnt, 0, item_tmp)
                        self.table.resizeColumnsToContents()
                        self.table.resizeRowsToContents()

                    # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
                    if self.cnt <= 25:
                        self.table.verticalScrollBar().setValue(0)
                    else:
                        self.table.verticalScrollBar().setValue(self.cnt - 15)

                    self.high_light(1)
                    self.Show_pic()
                else:
                    # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
                    if self.cnt <= 25:
                        self.table.verticalScrollBar().setValue(0)
                    else:
                        self.table.verticalScrollBar().setValue(self.cnt - 15)

                    self.high_light(1)
                    self.Show_pic()

            else:
                if not self.lock_flag:
                    if self.cnt == 0 and self.table2.item(0, 0).text() != '':
                        pass
                    else:
                        # 设置标定区当前标签为上一帧的标签
                        self.Table2_clear()
                        number_cnt = 0
                        # print('input', self.input_cnt)
                        for i in range(self.max_col):
                            if self.table2.item(self.cnt - 1, i).text() != '':
                                number_cnt += 1
                                # print('now string:',)
                                pre_text = self.table2.item(self.cnt - 1, i).text()
                                item_tmp = QTableWidgetItem(str(pre_text))
                                item_tmp.setFont(QFont("Times", 12, QFont.Black))
                                item_tmp.setTextAlignment(Qt.AlignCenter)
                                self.table2.setItem(self.cnt, i, item_tmp)
                                self.table2.resizeColumnsToContents()
                                self.table2.resizeRowsToContents()
                            else:
                                break
                        self.each_frame_input[self.cnt] = number_cnt

                    # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
                    if self.cnt <= 25:
                        self.table2.verticalScrollBar().setValue(0)
                        self.table.verticalScrollBar().setValue(0)
                    else:
                        self.table2.verticalScrollBar().setValue(self.cnt - 15)
                        self.table.verticalScrollBar().setValue(self.cnt - 15)

                    self.high_light(2)
                    self.high_light(1)
                    self.Show_pic()
                else:
                    # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
                    if self.cnt <= 25:
                        self.table2.verticalScrollBar().setValue(0)
                        self.table.verticalScrollBar().setValue(0)
                    else:
                        self.table2.verticalScrollBar().setValue(self.cnt - 15)
                        self.table.verticalScrollBar().setValue(self.cnt - 15)

                    self.high_light(2)
                    self.high_light(1)
                    self.Show_pic()

    def Show_pic(self):
        """
            函数功能：在label中显示当前帧
        """
        # self.show_pic1.clear()
        # self.show_pic2.clear()
        # img_rgb = cv2.imread(self.file_address + '/kinect_color/' + str(self.show_queue_version2[self.cnt][1]) + '.jpg')
        # # height, width = img.shape[:-1]
        # # size = (int(width * 0.5), int(height * 0.5))
        # #
        # # img_rgb = cv2.resize(img, size, cv2.INTER_LINEAR)
        # height1, width1 = img_rgb.shape[:-1]
        # img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        # qimage1 = QtGui.QImage(img_rgb, width1, height1, width1 * 3, QtGui.QImage.Format_RGB888)
        # self.show_pic1.setPixmap(QtGui.QPixmap(qimage1))

        # img_dep = extract_sketelon_2(self.file_address, self.show_queue_version2[self.cnt][0],
        #                              self.show_queue_version2[self.cnt][2], None, self.need_skeleton)
        # # height, width = img.shape[:-1]
        # # size = (int(width * 0.5), int(height * 0.5))
        # # img_dep = cv2.resize(img, size, cv2.INTER_LINEAR)
        # height2, width2 = img_dep.shape[:-1]
        # if self.change_flag:
        #     img_convt = cv2.applyColorMap(cv2.convertScaleAbs(img_dep, alpha=15), cv2.COLORMAP_JET)
        #     qimage2 = QtGui.QImage(img_convt, width2, height2, width2 * 3, QtGui.QImage.Format_RGB888)
        #     self.show_pic2.setPixmap(QtGui.QPixmap(qimage2))
        # else:
        #     qimage2 = QtGui.QImage(img_dep, width2, height2, width2 * 3, QtGui.QImage.Format_RGB888)
        #     self.show_pic2.setPixmap(QtGui.QPixmap(qimage2))

        # 脸部
        self.show_pic1.clear()
        self.show_pic2.clear()
        img_rgb = extract_from_json(self.file_address, self.cnt)
        # height, width = img.shape[:-1]
        # size = (int(width * 0.5), int(height * 0.5))
        #
        # img_rgb = cv2.resize(img, size, cv2.INTER_LINEAR)
        height1, width1 = img_rgb.shape[:-1]
        img_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
        qimage1 = QtGui.QImage(img_rgb, width1, height1, width1 * 3, QtGui.QImage.Format_RGB888)
        self.show_pic1.setPixmap(QtGui.QPixmap(qimage1))

        img = cv2.imread(self.file_address + '/kinect_color/' + str(self.show_queue_version2[self.cnt][1]) + '.jpg')
        # height, width = img.shape[:-1]
        # size = (int(width * 0.5), int(height * 0.5))
        #
        # img_rgb = cv2.resize(img, size, cv2.INTER_LINEAR)
        height2, width2 = img.shape[:-1]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        qimage2 = QtGui.QImage(img, width2, height2, width1 * 3, QtGui.QImage.Format_RGB888)
        self.show_pic2.setPixmap(QtGui.QPixmap(qimage2))

    def Table_addItem(self, i, j, content):
        """
            函数功能：因为经常性地修改骨架表，所以这里代码复用，table[i][j] = content
        """
        # table[i][j] = content
        item_tmp = QTableWidgetItem(str(content))
        item_tmp.setFont(QFont("Times", 12, QFont.Black))
        item_tmp.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(i, j, item_tmp)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def Table2_addItem(self, i, j, content):
        """
            函数功能：因为经常性地修改动作表，所以这里代码复用，table2[i][j] = content
        """
        # table[i][j] = content
        item_tmp = QTableWidgetItem(str(content))
        item_tmp.setFont(QFont("Times", 12, QFont.Black))
        item_tmp.setTextAlignment(Qt.AlignCenter)
        self.table2.setItem(i, j, item_tmp)
        self.table2.resizeColumnsToContents()
        self.table2.resizeRowsToContents()
        self.each_frame_input[self.cnt] += 1

    def Table2_clear(self):
        """
            函数功能：对动作表当前帧所有动作进行清空
        """
        if self.open_flag and self.table1_ok:
            length = self.each_frame_input[self.cnt]
            # 先清空
            for i in range(length):
                item_tmp = QTableWidgetItem('')
                item_tmp.setFont(QFont("Times", 12, QFont.Black))
                item_tmp.setTextAlignment(Qt.AlignCenter)
                self.table2.setItem(self.cnt, i, item_tmp)

            for i in range(self.max_col - 1, 0, -1):
                other = False
                for j in range(self.file_number):
                    if self.table2.item(j, i).text() != '':
                        other = True
                        break
                if not other:
                    self.table2.setColumnCount(self.max_col - 1)
                    self.max_col -= 1
                else:
                    break

            self.each_frame_input[self.cnt] = 0

    def mousePressEvent(self, event):
        """
            函数功能：响应鼠标事件
        """
        # print(self.show_pic2.width())
        self.mouse_press_flag = True
        x, y = event.pos().x(), event.pos().y()
        # print(x,y)
        if 430 <= x <= 800 and 25 <= y <= 400:
            if event.button() == Qt.LeftButton:
                # print("鼠标左键点击")
                self.Next_frame()
            elif event.button() == Qt.RightButton:
                # print("鼠标右键点击")
                self.Pre_frame()
            elif event.button() == Qt.MidButton:
                if self.table1_ok:
                    # print(self.table2.item(self.cnt, 0).text())
                    if self.table2.item(self.cnt, 0).text() == '':
                        self.Table2_addItem(self.cnt, 0, '0')
                    else:
                        self.Table2_clear()
                    self.high_light(2)
                else:
                    if self.table.item(self.cnt, 0).text() == '-1':
                        self.Table_addItem(self.cnt, 0, '0')
                    else:
                        self.Table_addItem(self.cnt, 0, '-1')
                    self.high_light(1)

        if self.open_flag and self.table1_ok:
            if 83 <= x <= 767 and 434 <= y <= 776:
                if 83 <= x <= 767:
                    frame_num = round((1.0 * ((self.end - self.start + 1) * (x - 83)) / (684 * 1.0))) - 1 + self.start
                    if frame_num < 0:
                        frame_num = 0
                    if frame_num >= self.file_number - 1:
                        frame_num = self.file_number - 1
                    tmp = self.cnt
                    self.cnt = frame_num
                    self.Show_pic()

                    # 高亮
                    for i in range(self.file_number):
                        self.table2.item(i, 0).setBackground(QBrush(QColor(255, 255, 255)))
                    self.table2.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))

                    # 类似网页中的下拉条永远保持在底部，这里我让其保持底部大约10格
                    if self.cnt <= 30:
                        self.table2.verticalScrollBar().setValue(0)
                        self.table.verticalScrollBar().setValue(0)
                    else:
                        self.table2.verticalScrollBar().setValue(self.cnt - 10)
                        self.table.verticalScrollBar().setValue(self.cnt - 10)
                    self.label_process.setText(str(self.cnt + 1) + ' / ' + str(self.file_number))

    def high_light(self, table_num):
        """
            函数功能：因为经常性需要高亮当前帧，所以此处直接写一个函数代码复用
        """
        tmp = self.table
        if table_num == 2:
            tmp = self.table2

        if self.cnt == 0:
            tmp.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))
        else:
            tmp.item(self.cnt - 1, 0).setBackground(QBrush(QColor(255, 255, 255)))
            tmp.item(self.cnt, 0).setBackground(QBrush(QColor(0, 191, 255)))

    def keyReleaseEvent(self, event):
        """
            函数功能：响应键盘事件
        """
        if self.open_flag:
            if event.key() == Qt.Key_D:
                self.Next_frame()
            elif event.key() == Qt.Key_A:
                self.Pre_frame()

            Number = [48, 49, 50, 51, 52, 53, 54, 55, 56, 57]

            if not self.table1_ok:
                if self.lock_flag:
                    pass
                else:
                    if event.key() in Number:
                        self.Table_addItem(self.cnt, 0, chr(event.key()))
                    elif event.key() == Qt.Key_Backspace:
                        self.Table_addItem(self.cnt, 0, '')
                    # elif event.key() == Qt.Key_Minus:
                    #     self.Table_addItem(self.cnt, 0, -1)
                    elif event.key() == Qt.Key_Escape:
                        self.table.clearFocus()
                        self.table2.clearFocus()
                    else:
                        pass
                self.high_light(1)
            else:
                # if self.lock_flag:
                #     pass
                # else:
                if event.key() in Number:
                    length = self.each_frame_input[self.cnt]
                    length += 1
                    self.max_col = max(self.max_col, length)
                    self.table2.setColumnCount(self.max_col)

                    # 每次可以输入多个值
                    self.Table2_addItem(self.cnt, length - 1, chr(event.key()))
                    self.each_frame_input[self.cnt] = length

                    # 每次只能允许输入一个值，否则覆盖
                    # self.Table2_addItem(self.cnt, 0, chr(event.key()))
                    # self.each_frame_input[self.cnt] = 1

                    # print('当前长度为: ', self.each_frame_input[self.cnt])

                    # 始终保持表格中不存在None
                    for i in range(self.file_number):
                        for j in range(self.max_col):
                            if self.table2.item(i, j) is None:
                                item_tmp = QTableWidgetItem('')
                                item_tmp.setFont(QFont("Times", 12, QFont.Black))
                                item_tmp.setTextAlignment(Qt.AlignCenter)
                                self.table2.setItem(i, j, item_tmp)

                elif event.key() == Qt.Key_Backspace:
                    length = self.each_frame_input[self.cnt]
                    if length >= 1:
                        self.Table2_addItem(self.cnt, length - 1, '')
                        if length == self.max_col:
                            other = False
                            for i in range(self.file_number):
                                if self.table2.item(i, length - 1).text() != '':
                                    other = True
                                    break
                            if not other:
                                self.table2.setColumnCount(self.max_col - 1)
                                self.max_col -= 1

                        length -= 1
                        self.each_frame_input[self.cnt] = length
                    else:
                        pass
                elif event.key() == Qt.Key_Escape:
                    self.table2.clearFocus()
                    self.table.clearFocus()
                else:
                    pass
                self.high_light(2)

    def Read_skeleton(self, num, body_index, point_num, xyz_index=None):
        """
            函数功能：读取指定帧指定骨架指定关键点的坐标
            num : 骨架.body文件的序号
            body_index : 某一帧中骨架的序号
            point_num ： 某一帧某一骨架中的关键点序号

            函数返回：返回一个列表形如 [x,y,z]，根据索引读取具体坐标值
        """
        if body_index == -1:
            return [-100, -100, -100]
        else:
            fp = open(self.file_address + '/kinect_bodies/' + str(num) + '.body', 'r')
            all_result = []
            text = fp.readlines()
            tmp_text = []
            for i in text:
                if i[0].isdecimal():
                    s = i
                    s.strip('\n')
                    s = s.split()[1][:-1]
                    s = s.split(',')
                    tmp = []
                    for j in s:
                        tmp.append(eval(j[2:]))
                    tmp_text.append(tmp)

            index = int((len(tmp_text)) / 25)
            for i in range(index):
                tmp = []
                start = i * 25
                for j in range(start, start + 25):
                    tmp.append(tmp_text[j])
                all_result.append(tmp)
            fp.close()
            if len(all_result) == 0:
                return -100
            return all_result[body_index][point_num]


# main
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = myMainWindow()
    gui.show()
    sys.exit(app.exec_())
