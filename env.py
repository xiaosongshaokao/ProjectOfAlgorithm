import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)  # 取消科学计数法


# def get_center_point(lis):  # get the center point of each room
#     area = 0.0
#     x, y = 0.0, 0.0
#
#     a = len(lis)
#     for i in range(a):
#         lat = lis[i][0]  # latitude
#         lng = lis[i][1]  # longitude
#
#         if i == 0:
#             lat1 = lis[-1][0]
#             lng1 = lis[-1][1]
#
#         else:
#             lat1 = lis[i - 1][0]
#             lng1 = lis[i - 1][1]
#
#         fg = (lat * lng1 - lng * lat1) / 2.0
#
#         area += fg
#         x += fg * (lat + lat1) / 3.0
#         y += fg * (lng + lng1) / 3.0
#
#     x = x / area
#     y = y / area
#
#     return [x, y]
def checkpoint(lis):  # 根据房间的拐点列表返回检测点列表,默认每一个纵坐标只有两个点
    check_point = []
    # 对于只有6个或4个顶点的，可以直接求解
    if len(lis) == 6:
        left1 = lis[0][0]
        right1 = lis[1][0]
        up1 = lis[0][1]
        down1 = lis[2][1]
        left2 = lis[4][0]
        right2 = lis[5][0]
        up2 = lis[2][1]
        down2 = lis[4][1]
        check_point.append(
            [[left1 + 1, up1 + 1], [right1 - 1, up1 + 1], [left1 + 1, down1 - 1], [right1 - 1, down1 - 1],
             [(left1 + right1) / 2, (up1 + down1) / 2]])
        check_point.append(
            [[left2 + 1, up2 + 1], [right2 - 1, up2 + 1], [left2 + 1, down2 - 1], [right2 - 1, down2 - 1],
             [(left2 + right2) / 2, (up2 + down2) / 2]])
        return check_point
    if len(lis) == 4:
        left = lis[0][0]
        right = lis[1][0]
        up = lis[0][1]
        down = lis[2][1]
        check_point.append([[left + 1, up + 1], [right - 1, up + 1], [left + 1, down - 1], [right - 1, down - 1],
                            [(left + right) / 2, (up + down) / 2]])
        return check_point

    else:
        left = lis[0][0]
        right = lis[1][0]
        up = lis[0][1]
        down = lis[2][1]
        check_point.append([[left + 1, up + 1], [right - 1, up + 1], [left + 1, down - 1], [right - 1, down - 1],
                            [(left + right) / 2, (up + down) / 2]])
        # 更新lis，删去顶层，递归
        if lis[2][0] < lis[0][0]:
            lis[3][0] = lis[1][0]
        elif lis[2][0] == lis[0][0]:
            lis[2][0] = lis[3][0]
            lis[3][0] = lis[1][0]
        elif lis[3][0] == lis[1][0]:
            lis[3][0] = lis[2][0]
            lis[2][0] = lis[0][0]
        elif lis[3][0] > lis[1][0]:
            lis[2][0] = lis[0][0]
        # print(lis)
        del lis[0]
        del lis[0]
        # print(lis)
        check_point.append(checkpoint(lis))
        return check_point


class Env:  # default size of environment : 5m*12m
    # the number of rooms, the dictionary of inflection point(x,y)
    def __init__(self, nroom=1, room=None):
        self.nroom = nroom
        structure = np.zeros([50, 120])  # get a 2-dimensional array of the environment
        check_point = {}
        hwall = []
        vwall = []
        if nroom == 1:
            check_point[1] = [[0, 0], [0, 119], [24, 59], [49, 0], [49, 119]]
            for i in range(120):
                structure[0][i] = 1
                structure[49][i] = 1
            for i in range(50):
                structure[i][0] = 1
                structure[i][119] = 1
            self.structure = structure
            self.checkpoint = check_point
            self.hwall = hwall
            self.vwall = vwall
        else:
            for i in range(1, nroom + 1):
                points = room[i]
                length = len(points)
                # 将有墙体的地方数组值设为1
                for j in range(length - 1):
                    for k in range(j + 1, length):
                        if points[j][0] == points[k][0]:
                            col = points[j][0]
                            vwall.append([col, points[j][1], points[k][1]])
                            for index in range(points[j][1], points[k][1] + 1):
                                structure[index][col] = 1
                        if points[j][1] == points[k][1]:
                            row = points[j][1]
                            hwall.append([row, points[j][0], points[k][0]])
                            for index in range(points[j][0], points[k][0] + 1):
                                structure[row][index] = 1
                check_point[i] = checkpoint(points)  # 得到每一个房间的检测点数组
            self.structure = structure
            self.checkpoint = check_point
            self.hwall = hwall
            self.vwall = vwall

    # def show(self):
    #     plt.scatter(self.structure)
    #     plt.show()


if __name__ == '__main__':
    # 手动输入各个房间的拐点
    room = {}
    room[1] = [[0, 0], [29, 0], [0, 9], [19, 9], [20, 24], [30, 24]]
    room[2] = [[29, 0], [59, 0], [29, 24], [59, 24]]
    room[3] = [[59, 0], [119, 0], [59, 9], [119, 9]]
    room[4] = [[0, 9], [19, 9], [0, 39], [19, 39]]
    room[5] = [[19, 24], [49, 24], [0, 39], [19, 39], [0, 49], [49, 49]]
    room[6] = [[59, 9], [94, 9], [49, 24], [59, 24], [49, 39], [74, 39], [74, 42], [94, 42]]
    room[7] = [[94, 9], [119, 9], [94, 42], [119, 42]]
    room[8] = [[49, 39], [74, 39], [49, 49], [74, 49]]
    room[9] = [[74, 42], [119, 42], [74, 49], [119, 49]]
    # room = {1: [[0, 0], [29, 0], [0, 9], [19, 9], [20, 24], [30, 24]], 2: [[29, 0], [59, 0], [29, 24], [59, 24]],
    #         3: [[59, 0], [119, 0], [59, 9], [119, 9]], 4: [[0, 9], [19, 9], [0, 39], [19, 39]],
    #         5: [[19, 24], [49, 24], [0, 39], [19, 39], [0, 49], [49, 49]],
    #         6: [[59, 9], [94, 9], [49, 24], [59, 24], [49, 39], [74, 39], [74, 42], [94, 42]],
    #         7: [[74, 42], [119, 42], [74, 49], [119, 49]], 8: [[49, 39], [74, 39], [49, 49], [74, 49]]}
    env = Env(len(room), room)
    print(env.structure)
    print(env.checkpoint)
