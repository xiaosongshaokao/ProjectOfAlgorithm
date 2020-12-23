#这个文件中需要写一个解类，此类需要包含一个解中所有的AP分布，并包含适应度函数
from env import *

location_set = [[0,0],[1,1],[2,2],[3,3]]
class solution:
    def __init__(self, location=None):
        if location is None:
            location = location_set
        self.location = location
        self.fit_number = 0
        self.emission_intensity = 100

    def ThroughTheWall(self, AP, TestPoint, background):#计算从信号发射点到信号检测点穿墙次数
        count = 0
        row = background.hwall
        column = background.vwall
        slope = (AP[1] - TestPoint[1]) / (AP[0] - TestPoint[0])
        cut_off = TestPoint[1] - AP[1] * slope
        for wall in row:
            cross = (wall[1] - cut_off) / slope
            if AP[1] < TestPoint[1]:
                if AP[1] < wall[0] and wall[0] < TestPoint[1] and wall[1] < cross and cross < wall[2]:
                    count += 1
            else:
                if TestPoint[1] < wall[0] and wall[0] < AP[1] and wall[1] < cross and cross < wall[2]:
                    count += 1
        for wall in column:
            cross = slope * wall[0] + cut_off
            if AP[0] < TestPoint[0]:
                if AP[0] < wall[0] and wall[0] < TestPoint[0] and wall[1] < cross and cross < wall[2]:
                    count += 1
                if TestPoint[0] < wall[0] and wall[0] < AP[0] and wall[1] < cross and cross < wall[2]:
                    count += 1
        return count

    # 计算从信号发射点到信号检测点的信号强度衰减
    #根据公式，我舍去了常数部分，PLE暂设为0.5， 每穿过一堵墙的损耗暂设为10dB，均为经验值
    def reduction(self, times, distance):
        reduce = 1
        loss = (distance) ** 0.5 * 10 ** times
        reduce = reduce / loss
        return reduce

    def fitness(self, background):#适应度函数，返回值为每个solution中的每个房间的所有监测点处信号强度
        results_in_background = []
        for i in range(0, background.nroom):#计算每个房间的每个信号检测点的信号强度
            TestPoint = background.checkpoint[i]
            results = []
            All_point = []
            for points in TestPoint:#points每个房间切分出的小矩形
                for j in points:
                    All_point.append(j)
            for point in All_point:
                result_at_the_point = 0
                for AP in location_set:
                    times = self.ThroughTheWall(AP, point, background)
                    distance = ((AP[0] - point[0])**2 + (AP[1] - point[1]))**0.5
                    reduction = self.reduction(times, distance)
                    result_at_the_point += self.emission_intensity * reduction
                results.append(result_at_the_point)
            results_in_background.append(results)
        return results_in_background

    def judgePopulation(self,results):#判断函数，用来决定特定种群这一组解的价值，后续可能会有调整

        def judgeAP(self, resultOfpoint):#加权函数
            value = resultOfpoint
            return value

        total_sum = 0
        for room_result in results:
            for point_result in room_result:
                total_sum += judgeAP(self,point_result)
        total_sum = total_sum // len(self.location)
        self.fit_number = total_sum
        return total_sum
