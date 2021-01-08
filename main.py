import random
from solution import *
from env import *
import numpy as np
import matplotlib.pyplot as plt

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
    if len(set([tuple(t) for t in pos])) == len(pos):
        return pos
    else:
        return None


def pos2gene(pos):  # 将一个包含各AP位置的数组解码至基因型
    number = len(pos)
    gene = np.zeros(number * 13, dtype='int')  # 128 = 2^7, 64 = 2^6 各AP位置对应的基因型，先横坐标，后纵坐标
    for i in range(number):
        col = pos[i][0]
        row = pos[i][1]
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
    return gene


# step2 初始化种群 也是最难的一步，房间个数决定AP最大数目
def init_population(number, N):  # number指AP数量，N是种群规模
    """
    初始化
    """
    solutions = []
    for k in range(N):
        pos = []
        for i in range(number):
            while True:
                row = random.randint(0, 49)
                col = random.randint(0, 119)
                if env.structure[row][col] and ([col, row] in pos):
                    continue
                break
            pos.append([col, row])
        solutions.append(solution(pos))
    return solutions


# step3 计算适应度函数
def calvalue(popu):
    '''
    :param popu: 传入种群信息
    :return: 返回的是每一组AP组成的列表
    '''

    return None


# step4 选择
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
    quick_sort(li, start, left - 1)
    # 递归处理右边的数据
    quick_sort(li, left + 1, end)


def selection(pop):
    '''
    :param pop:种群
    :param value:适应度值列表
    :return:返回新的种群
    '''
    quick_sort(pop, 0, len(pop) - 1)
    if len(pop) > 200:
        pop = pop[len(pop) - 201:]
    ini_length = len(pop)  # 输入个体的总数
    remaining_number = ini_length // 2  # 确定保留的强者数量
    danger_number = ini_length - remaining_number  # 可能会被淘汰的弱者数量
    elimination_rate = []  # 弱者们各自可能被淘汰的概率
    random_deci = []  # 存放随机的小数
    inteval = 1 / danger_number
    # 分别计算死亡淘汰概率和随机数
    for i in range(0, danger_number):
        elimination_rate.append(i * inteval)
    for i in range(0, danger_number):
        random_deci.append(random.random())
    new_popu = []  # 选择后的个体
    for i in range(0, remaining_number):
        new_popu.append(pop[len(pop) - 1 - i])
    # 如果随机数大于淘汰概率，则个体保留
    for i in range(0, danger_number):
        if elimination_rate[i] < random_deci[i]:
            new_popu.append(pop[len(pop) - 1 - remaining_number - i])
    return new_popu


# step5 交叉   拟采用单点交叉
def cross(parents_entity, pc):
    '''
    :param parents: 交叉的父类
    :param pc:   交叉概率
    :return:
    '''
    parents = []
    children = []  # 首先创建一个子代 空列表 存放交叉后的种群基因型
    single_popu_index_list = []  # 存放重复内容的指针
    lenparents = len(parents_entity)  # 先提取出父代的个数  因为要配对 奇数个的话会剩余一个
    for i in range(0, lenparents):
        parents.append(parents_entity[i].gene)
    parity = lenparents % 2  # 计算出长度奇偶性  parity= 1 说明是奇数个  则需要把最后一条个体直接加上 不交叉
    for i in range(0, lenparents - 1, 2):  # 每次取出两条个体 如果是奇数个则长度要减去 一  range函数不会取最后一个
        single_now_popu = parents[i].tolist()  # 取出当前选中的两个父代中的第一个
        single_next_popu = parents[i + 1].tolist()  # 取出当前选中的两个父代中的第二个
        index_content = []
        for j in range(len(single_next_popu)):
            if single_next_popu[j] == single_now_popu[j]:
                index_content.append(j)
        num_rep = len(index_content)  # 重复内容的个数
        if random.random() < pc and num_rep >= 1:
            index = index_content[random.randint(0, num_rep - 1)]  # 随机选取一个重复的内容
            children.append(single_now_popu[0:index + 1] + single_next_popu[index + 1:])
            children.append(single_next_popu[0:index + 1] + single_now_popu[index + 1:])
            children.append(single_now_popu)
            children.append(single_next_popu)
        else:
            children.append(single_now_popu)
            children.append(single_next_popu)
    if parity == 1:  # 如果是个奇数  为了保证种群规模不变 需要加上最后一条
        children.append(parents[lenparents - 1])  # 子代在添加一行,直接遗传给下一代
    return children


# step6 变异
def mutation(children, pm):
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
    env = Env(nroom=9, room=room)

    for i in range(0, 3):
        numOfAP = i+1
        for j in range (10,210,20):
            #需要根据图像做调整 对相对较密的地方把步长改小
            optimal_solutions = [0.01]
            count = 1
            init_sol = init_population(i + 1, j)
            for entity in init_sol:
                results_in_background = entity.fitness(env)
                entity.judgePopulation(results_in_background)
            while count <= 1000:
            #根据需要也可以改动
                average = 0
                population_After_selection = selection(init_sol)
            # print("1111", len(population_After_selection))
                population_After_cross = cross(population_After_selection, 0.8)
            # print("2222", len(population_After_cross))
                population_After_mutation = mutation(population_After_cross, 0.001)
                pos = []
                init_sol = []
                for gene in population_After_mutation:
                    pos = gene2pos(gene)
                    if pos is None:
                        continue
                    solution_new = solution(pos)
                    results_in_background_new = solution_new.fitness(env)
                    solution_new.judgePopulation(results_in_background_new)
                    init_sol.append(solution_new)
                quick_sort(init_sol, 0, len(init_sol) - 1)
                for k in range(0, 5):
                    average = average + init_sol[len(init_sol) - 1 - k].fit_number
                average = average // 5
                optimal_solutions.append(average)
                if -0.01 < (optimal_solutions[count] - optimal_solutions[count - 1]) / optimal_solutions[
                    count - 1] < 0.01 and count > 200:
                #print(optimal_solutions[count])
                #print(optimal_solutions[count - 1])
                    break
                count += 1
            print("AP",numOfAP,"Init pop",j)
            print("end epoch",count)
            print("result during evualtion",optimal_solutions)
            plt.plot(optimal_solutions)
            save_path = str(i + 1) + "-" + str(j)+".png"
            plt.savefig(save_path)
            plt.close()
