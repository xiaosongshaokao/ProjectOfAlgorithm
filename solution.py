#这个文件中需要写一个解类，此类需要包含一个解中所有的AP分布，并包含适应度函数
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

        return count

    def reduction(self, times, distance):#计算从信号发射点到信号检测点的信号强度衰减
        reduce = 1

        return reduce

    def fitness(self, background):#适应度函数，返回值为修改过的fit_number
        results_in_background = []
        for room in background.rooms:#计算每个房间的每个信号检测点的信号强度
            results = []
            TestPoint = room.points
            for point in TestPoint:
                result_at_the_point = 0
                for AP in location_set:
                    times = self.ThroughTheWall(AP, point, background)
                    distance = ((AP[0] - point[0])**2 + (AP[1] - point[1]))**0.5
                    reduction = self.reduction(times, distance)
                    result_at_the_point += self.emission_intensity * reduction
                results.append(result_at_the_point)
            results_in_background.append(results)

