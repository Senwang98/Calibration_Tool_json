import cv2

"""
    一些计算需要的常量
"""
fx = 364.304
fy = 364.304
cx = 258.891
cy = 209.32

red = (0, 255, 0)
green = (255, 0, 0)
white = (255, 255, 255)


def connect_point(x, y, img):
    """
        x,y中存放了对应的一帧帧骨架坐标，img为所需的图片
        函数功能：在img上将x,y的坐标画出
        return None
    """
    # 未读到骨架信息
    if len(x) == 0 or len(y) == 0:
        return

    # 关键点描绘
    for i in range(0, len(x)):
        for j in range(0, len(x[i])):
            if x[i][j] and y[i][j]:
                cv2.circle(img, (int(x[i][j]), int(y[i][j])), 4, green, -1)

    # 描绘边框
    for i in range(len(x)):
        # 因为可能会产生None而导致无法只用内置函数，所以此处手动求解极值
        maxx = -1e9
        minx = 1e9
        maxy = -1e9
        miny = 1e9
        for j in range(len(x[i])):
            if x[i][j]:
                maxx = max(maxx, x[i][j])
                minx = min(minx, x[i][j])
            if y[i][j]:
                maxy = max(maxy, y[i][j])
                miny = min(miny, y[i][j])

        # 画出矩形的四个点
        cv2.circle(img, (-1, int(maxy)), 3, green, -1)
        cv2.circle(img, (int(maxx), int(miny)), 3, green, -1)
        cv2.circle(img, (int(minx), int(maxy)), 3, green, -1)
        cv2.circle(img, (int(minx), int(miny)), 3, green, -1)

        # 将上述四个点进行连线
        cv2.line(img, (int(minx), int(miny)), (int(maxx), int(miny)), red, 1)
        cv2.line(img, (int(minx), int(miny)), (int(minx), int(maxy)), red, 1)
        cv2.line(img, (int(minx), int(maxy)), (int(maxx), int(maxy)), red, 1)
        cv2.line(img, (int(maxx), int(miny)), (int(maxx), int(maxy)), red, 1)

        # 设置索引
        image = cv2.putText(img, str(i), (round(minx), max(round(miny) - 5, 0)), cv2.FONT_HERSHEY_COMPLEX, 0.8, red, 1)

    # 将所有的骨架都进行描绘
    for i in range(len(x)):
        # 关键点连线
        if x[i][0] and y[i][0] and x[i][1] and y[i][1]:
            cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][1]), int(y[i][1])), red, 1)
        if x[i][1] and y[i][1] and x[i][20] and y[i][20]:
            cv2.line(img, (int(x[i][1]), int(y[i][1])), (int(x[i][20]), int(y[i][20])), red, 1)
        if x[i][20] and y[i][20] and x[i][2] and y[i][2]:
            cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][2]), int(y[i][2])), red, 1)
        if x[i][2] and y[i][2] and x[i][3] and y[i][3]:
            cv2.line(img, (int(x[i][2]), int(y[i][2])), (int(x[i][3]), int(y[i][3])), red, 1)

        if x[i][0] and y[i][0] and x[i][16] and y[i][16]:
            cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][16]), int(y[i][16])), red, 1)
        if x[i][16] and y[i][16] and x[i][17] and y[i][17]:
            cv2.line(img, (int(x[i][16]), int(y[i][16])), (int(x[i][17]), int(y[i][17])), red, 1)
        if x[i][17] and y[i][17] and x[i][18] and y[i][18]:
            cv2.line(img, (int(x[i][17]), int(y[i][17])), (int(x[i][18]), int(y[i][18])), red, 1)
        if x[i][18] and y[i][18] and x[i][19] and y[i][19]:
            cv2.line(img, (int(x[i][18]), int(y[i][18])), (int(x[i][19]), int(y[i][19])), red, 1)

        if x[i][0] and y[i][0] and x[i][12] and y[i][12]:
            cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][12]), int(y[i][12])), red, 1)
        if x[i][12] and y[i][12] and x[i][13] and y[i][13]:
            cv2.line(img, (int(x[i][12]), int(y[i][12])), (int(x[i][13]), int(y[i][13])), red, 1)
        if x[i][13] and y[i][13] and x[i][14] and y[i][14]:
            cv2.line(img, (int(x[i][13]), int(y[i][13])), (int(x[i][14]), int(y[i][14])), red, 1)
        if x[i][14] and y[i][14] and x[i][15] and y[i][15]:
            cv2.line(img, (int(x[i][14]), int(y[i][14])), (int(x[i][15]), int(y[i][15])), red, 1)

        if x[i][20] and y[i][20] and x[i][8] and y[i][8]:
            cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][8]), int(y[i][8])), red, 1)
        if x[i][8] and y[i][8] and x[i][9] and y[i][9]:
            cv2.line(img, (int(x[i][8]), int(y[i][8])), (int(x[i][9]), int(y[i][9])), red, 1)
        if x[i][9] and y[i][9] and x[i][10] and y[i][10]:
            cv2.line(img, (int(x[i][9]), int(y[i][9])), (int(x[i][10]), int(y[i][10])), red, 1)
        if x[i][10] and y[i][10] and x[i][11] and y[i][11]:
            cv2.line(img, (int(x[i][10]), int(y[i][10])), (int(x[i][11]), int(y[i][11])), red, 1)
        if x[i][10] and y[i][10] and x[i][24] and y[i][24]:
            cv2.line(img, (int(x[i][10]), int(y[i][10])), (int(x[i][24]), int(y[i][24])), red, 1)
        if x[i][11] and y[i][11] and x[i][23] and y[i][23]:
            cv2.line(img, (int(x[i][11]), int(y[i][11])), (int(x[i][23]), int(y[i][23])), red, 1)

        if x[i][20] and y[i][20] and x[i][4] and y[i][4]:
            cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][4]), int(y[i][4])), red, 1)
        if x[i][4] and y[i][4] and x[i][5] and y[i][5]:
            cv2.line(img, (int(x[i][4]), int(y[i][4])), (int(x[i][5]), int(y[i][5])), red, 1)
        if x[i][5] and y[i][5] and x[i][6] and y[i][6]:
            cv2.line(img, (int(x[i][5]), int(y[i][5])), (int(x[i][6]), int(y[i][6])), red, 1)
        if x[i][6] and y[i][6] and x[i][7] and y[i][7]:
            cv2.line(img, (int(x[i][6]), int(y[i][6])), (int(x[i][7]), int(y[i][7])), red, 1)
        if x[i][7] and y[i][7] and x[i][21] and y[i][21]:
            cv2.line(img, (int(x[i][7]), int(y[i][7])), (int(x[i][21]), int(y[i][21])), red, 1)
        if x[i][6] and y[i][6] and x[i][22] and y[i][22]:
            cv2.line(img, (int(x[i][6]), int(y[i][6])), (int(x[i][22]), int(y[i][22])), red, 1)


def connect_point_single(x, y, img, index):
    """
            x,y中存放了对应的一帧帧骨架坐标，img为所需的图片
            函数功能：在img上将x,y的坐标画出
            return None
        """
    # 未读到骨架信息
    if len(x) == 0 or len(y) == 0:
        return

    # 关键点描绘
    i = index
    for j in range(0, len(x[i])):
        if x[i][j] and y[i][j]:
            cv2.circle(img, (int(x[i][j]), int(y[i][j])), 4, green, -1)

    i = index
    # 因为可能会产生None而导致无法只用内置函数，所以此处手动求解极值
    maxx = -1e9
    minx = 1e9
    maxy = -1e9
    miny = 1e9
    for j in range(len(x[i])):
        if x[i][j]:
            maxx = max(maxx, x[i][j])
            minx = min(minx, x[i][j])
        if y[i][j]:
            maxy = max(maxy, y[i][j])
            miny = min(miny, y[i][j])

    # 画出矩形的四个点
    cv2.circle(img, (-1, int(maxy)), 3, green, -1)
    cv2.circle(img, (int(maxx), int(miny)), 3, green, -1)
    cv2.circle(img, (int(minx), int(maxy)), 3, green, -1)
    cv2.circle(img, (int(minx), int(miny)), 3, green, -1)

    # 将上述四个点进行连线
    cv2.line(img, (int(minx), int(miny)), (int(maxx), int(miny)), red, 1)
    cv2.line(img, (int(minx), int(miny)), (int(minx), int(maxy)), red, 1)
    cv2.line(img, (int(minx), int(maxy)), (int(maxx), int(maxy)), red, 1)
    cv2.line(img, (int(maxx), int(miny)), (int(maxx), int(maxy)), red, 1)

    #
    image = cv2.putText(img, str(i), (round(minx), max(round(miny) - 5, 0)), cv2.FONT_HERSHEY_COMPLEX, 0.8, red, 1)

    i = index
    # 关键点连线
    if x[i][0] and y[i][0] and x[i][1] and y[i][1]:
        cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][1]), int(y[i][1])), red, 1)
    if x[i][1] and y[i][1] and x[i][20] and y[i][20]:
        cv2.line(img, (int(x[i][1]), int(y[i][1])), (int(x[i][20]), int(y[i][20])), red, 1)
    if x[i][20] and y[i][20] and x[i][2] and y[i][2]:
        cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][2]), int(y[i][2])), red, 1)
    if x[i][2] and y[i][2] and x[i][3] and y[i][3]:
        cv2.line(img, (int(x[i][2]), int(y[i][2])), (int(x[i][3]), int(y[i][3])), red, 1)

    if x[i][0] and y[i][0] and x[i][16] and y[i][16]:
        cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][16]), int(y[i][16])), red, 1)
    if x[i][16] and y[i][16] and x[i][17] and y[i][17]:
        cv2.line(img, (int(x[i][16]), int(y[i][16])), (int(x[i][17]), int(y[i][17])), red, 1)
    if x[i][17] and y[i][17] and x[i][18] and y[i][18]:
        cv2.line(img, (int(x[i][17]), int(y[i][17])), (int(x[i][18]), int(y[i][18])), red, 1)
    if x[i][18] and y[i][18] and x[i][19] and y[i][19]:
        cv2.line(img, (int(x[i][18]), int(y[i][18])), (int(x[i][19]), int(y[i][19])), red, 1)

    if x[i][0] and y[i][0] and x[i][12] and y[i][12]:
        cv2.line(img, (int(x[i][0]), int(y[i][0])), (int(x[i][12]), int(y[i][12])), red, 1)
    if x[i][12] and y[i][12] and x[i][13] and y[i][13]:
        cv2.line(img, (int(x[i][12]), int(y[i][12])), (int(x[i][13]), int(y[i][13])), red, 1)
    if x[i][13] and y[i][13] and x[i][14] and y[i][14]:
        cv2.line(img, (int(x[i][13]), int(y[i][13])), (int(x[i][14]), int(y[i][14])), red, 1)
    if x[i][14] and y[i][14] and x[i][15] and y[i][15]:
        cv2.line(img, (int(x[i][14]), int(y[i][14])), (int(x[i][15]), int(y[i][15])), red, 1)

    if x[i][20] and y[i][20] and x[i][8] and y[i][8]:
        cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][8]), int(y[i][8])), red, 1)
    if x[i][8] and y[i][8] and x[i][9] and y[i][9]:
        cv2.line(img, (int(x[i][8]), int(y[i][8])), (int(x[i][9]), int(y[i][9])), red, 1)
    if x[i][9] and y[i][9] and x[i][10] and y[i][10]:
        cv2.line(img, (int(x[i][9]), int(y[i][9])), (int(x[i][10]), int(y[i][10])), red, 1)
    if x[i][10] and y[i][10] and x[i][11] and y[i][11]:
        cv2.line(img, (int(x[i][10]), int(y[i][10])), (int(x[i][11]), int(y[i][11])), red, 1)
    if x[i][10] and y[i][10] and x[i][24] and y[i][24]:
        cv2.line(img, (int(x[i][10]), int(y[i][10])), (int(x[i][24]), int(y[i][24])), red, 1)
    if x[i][11] and y[i][11] and x[i][23] and y[i][23]:
        cv2.line(img, (int(x[i][11]), int(y[i][11])), (int(x[i][23]), int(y[i][23])), red, 1)

    if x[i][20] and y[i][20] and x[i][4] and y[i][4]:
        cv2.line(img, (int(x[i][20]), int(y[i][20])), (int(x[i][4]), int(y[i][4])), red, 1)
    if x[i][4] and y[i][4] and x[i][5] and y[i][5]:
        cv2.line(img, (int(x[i][4]), int(y[i][4])), (int(x[i][5]), int(y[i][5])), red, 1)
    if x[i][5] and y[i][5] and x[i][6] and y[i][6]:
        cv2.line(img, (int(x[i][5]), int(y[i][5])), (int(x[i][6]), int(y[i][6])), red, 1)
    if x[i][6] and y[i][6] and x[i][7] and y[i][7]:
        cv2.line(img, (int(x[i][6]), int(y[i][6])), (int(x[i][7]), int(y[i][7])), red, 1)
    if x[i][7] and y[i][7] and x[i][21] and y[i][21]:
        cv2.line(img, (int(x[i][7]), int(y[i][7])), (int(x[i][21]), int(y[i][21])), red, 1)
    if x[i][6] and y[i][6] and x[i][22] and y[i][22]:
        cv2.line(img, (int(x[i][6]), int(y[i][6])), (int(x[i][22]), int(y[i][22])), red, 1)


def extract_sketelon_2(file_address, body_number, depth_number, body_index=None, need_skeleton=True):
    """
    Input:

        file_address : 存放图片以及骨架信息的上次目录
        body_number : .body的序号
        depth_number : 深度图的序号
        body_index : 某一帧中需要显示的那个目标骨架的序号，默认全部显示
        need_skeleton : 当前深度图是否需要叠加骨架信息

    Output:
        img : 返回最终处理后的图片
    """

    # 读取对应序号的深度图
    img = cv2.imread(file_address + '/kinect_depth/' + str(depth_number) + '.png')

    if not need_skeleton:
        return img
    else:
        # 读取对应序号的骨架信息
        fp = open(file_address + '/kinect_bodies/' + str(body_number) + '.body', 'r')
        text = fp.readlines()

        # 存放某一帧的所有骨架点信息的列表
        all_result = []

        # 暂存按照顺序读取的所有关键点坐标信息
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

        # index 表示一帧中有多少的骨架信息
        index = int((len(tmp_text)) / 25)

        for i in range(index):
            tmp = []
            start = i * 25
            for j in range(start, start + 25):
                tmp.append(tmp_text[j])
            all_result.append(tmp)
        fp.close()

        """
            对于读取的三维数据进行二维转化
        """
        coordinate_x, coordinate_y = [], []

        for i in range(len(all_result)):
            tmpx, tmpy = [], []
            for j in range(len(all_result[i])):
                x, y, z = all_result[i][j][0], all_result[i][j][1], all_result[i][j][2]
                # 此处需要处理好可能未找到关键点的问题
                if z == 0:
                    tmpx.append(None)
                    tmpy.append(None)
                else:
                    result_y = ((-y * fy) / z) + cy
                    result_x = ((-x * fx) / z) + cx
                    tmpx.append(result_x)
                    tmpy.append(result_y)

            coordinate_x.append(tmpx)
            coordinate_y.append(tmpy)

        # 按照具体显示需求分别处理
        if body_index is None:
            connect_point(coordinate_x, coordinate_y, img)
        elif body_index != -1:
            connect_point_single(coordinate_x, coordinate_y, img, body_index)
        else:
            pass

        return img


# test code
if __name__ == '__main__':
    file_address = 'Y:\\id_340321194604034063_20191014113044\\rapid_alternating_movements_of_hand'
    img = extract_sketelon_2(file_address, 321, 321, None)
    cv2.imshow('line', img)
    cv2.waitKey(0)
