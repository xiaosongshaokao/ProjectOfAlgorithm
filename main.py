import random
from solution import *
from  env import *
import numpy as np
# class Map():
#     '''
#     :param:地图类
#     :param:使用时需要传入行列两个参数 再实例化
#     '''
#
#     def __init__(self,row,col):
#         '''
#         :param:row::行
#         :param:col::列
#         '''
#         self.data = []
#         self.row = row
#         self.col = col
#     def map_init(self):
#         '''刘攀'''
#     def map_Obstacle(self,num):
#         '''
#         :param:num:地图障碍物数量
#         :return：返回包含障碍物的地图数据
#         '''

# step2 初始化种群 也是最难的一步
class Population:
    # 房间个数决定AP最大数目
        def __init__(self, number, N):  # number指AP数量，N是种群规模
        """
        初始化
        """
        entity = []
        self.number = number
        for k in range(N):
            gene = np.zeros(number * 13, dtype='int')  # 128 = 2^7, 64 = 2^6
            for i in range(number):
                while True:
                    row = random.randint(0, 49)
                    col = random.randint(0, 119)
                    if env.structure[row][col] and ([col, row] in pos):
                        continue
                    break
                cnt = 0
                start_index = i * 13
                while col != 0:
                    cnt += 1
                    gene[start_index + 7 - cnt] = col % 2
                    col = col // 2
                cnt = 0
                while row != 0:
                    cnt += 1
                    gene[start_index + 13 - cnt] = row % 2
                    row = row // 2
            self.gene = gene  # 各AP位置对应的基因型，先横坐标，后纵坐标
            entity.append(gene)
        self.entity = entity

    def Population_Init(self):
        '''
        种群初始化
        '''
        return None

    def Generate_Sample_AP(self):  # 生成可进行采样计算的各组AP
        '''
        '''
        return None


def gene2pos(gene):  # 将基因型解码至一个包含各AP位置的数组
    n = int(len(gene) / 13)
    pos = []
    for i in range(n):
        start_index = 13 * i
        col = 0
        row = 0
        for j in range(7):
            col += gene[start_index + j] * np.power(2, 6 - j)
        for j in range(6):
            row += gene[start_index + 7 + j] * np.power(2, 5 - j)
        pos.append([col, row])
    return pos

#step3 计算适应度函数
def calvalue(popu):
    '''
    :param popu: 传入种群信息
    :return: 返回的是每一组AP组成的列表
    '''

    return None

#step4 选择
def quick_sort(li, start, end):
    # 分治 一分为二
    # start=end ,证明要处理的数据只有一个
    # start>end ,证明右边没有数据
    if start >= end:
        return
    # 定义两个游标，分别指向0和末尾位置
    left = start
    right = end
    # 把0位置的数据，认为是中间值
    mid = li[left]
    while left < right:
        # 让右边游标往左移动，目的是找到小于mid的值，放到left游标位置
        while left < right and li[right].fit_number >= mid.fit_number:
            right -= 1
        li[left] = li[right]
        # 让左边游标往右移动，目的是找到大于mid的值，放到right游标位置
        while left < right and li[left].fit_number < mid.fit_number:
            left += 1
        li[right] = li[left]
    # while结束后，把mid放到中间位置，left=right
    li[left] = mid
    # 递归处理左边的数据
    quick_sort(li, start, left-1)
    # 递归处理右边的数据
    quick_sort(li, left+1, end)

def selection(pop,value):
    '''
    :param pop:种群
    :param value:适应度值列表
    :return:返回新的种群
    '''
    quick_sort(pop, 0, len(pop))
    ini_length = len(pop)#输入个体的总数
    remaining_number = ini_length // 2#确定保留的强者数量
    danger_number = ini_length - remaining_number#可能会被淘汰的弱者数量
    elimination_rate = []#弱者们各自可能被淘汰的概率
    random_deci = []#存放随机的小数
    inteval = 1 / danger_number
    #分别计算死亡淘汰概率和随机数
    for i in range(0, danger_number):
        elimination_rate.append(i * inteval)
    for i in range(0, danger_number):
        random_deci.append(random.random())
    new_popu = []       #选择后的个体
    for i in range(0, remaining_number):
        new_popu.append(pop[i])
    #如果随机数大于淘汰概率，则个体保留
    for i in range(0, danger_number):
        if elimination_rate[i] < random_deci[i]:
            new_popu.append(pop[remaining_number + i])
    return new_popu

#step5 交叉   拟采用单点交叉
def cross(parents_entity,pc):
    '''
    :param parents: 交叉的父类
    :param pc:   交叉概率
    :return:
    '''
    parents = []
    children = []  #首先创建一个子代 空列表 存放交叉后的种群基因型
    single_popu_index_list = []#存放重复内容的指针
    lenparents = len(parents_entity)  #先提取出父代的个数  因为要配对 奇数个的话会剩余一个
    for i in range(0, lenparents):
        parents.append(parents_entity[i].gene)
    parity = lenparents % 2 #计算出长度奇偶性  parity= 1 说明是奇数个  则需要把最后一条个体直接加上 不交叉
    for i in range(0,lenparents-1,2):       #每次取出两条个体 如果是奇数个则长度要减去 一  range函数不会取最后一个
        single_now_popu = parents[i]        #取出当前选中的两个父代中的第一个
        single_next_popu = parents[i+1]     #取出当前选中的两个父代中的第二个
        index_content = list(set(single_now_popu).intersection(set(single_next_popu))) #第一条路经与第二条路经重复的内容
        num_rep = len(index_content)          #重复内容的个数
        if random.random() < pc and num_rep>=3:
            content = index_content[random.randint(0,num_rep-1)]   #随机选取一个重复的内容
            now_index = single_now_popu.index(content)  #重复内容在第一个父代中的索引
            next_index = single_next_popu.index(content)#重复内容在第二个父代中的索引
            children.append(single_now_popu[0:now_index + 1] + single_next_popu[next_index + 1:])
            children.append(single_next_popu[0:next_index + 1] + single_now_popu[now_index + 1:])
            children.append(single_now_popu)
            children.append(single_next_popu)
        else:
            children.append(single_now_popu)
            children.append(single_next_popu)
    if parity == 1:     #如果是个奇数  为了保证种群规模不变 需要加上最后一条
        children.append(parents[lenparents - 1]) #子代在添加一行,直接遗传给下一代
    return children

#step6 变异
def mutation(children,pm):
    '''
    :param children: 子代种群
    :param pm: 变异概率
    :return: 返回变异后的新种群
    '''
    count = 0
    new_popu = []
    for i in children:
        new_popu.append([])
        for j in i:
            num = random.random()
            if num < pm:
                j = (j + 1) % 2
            new_popu[count].append(j)
        count += 1
    return new_popu

if __name__ == '__main__':
    env = Env()

    print("result is " )
