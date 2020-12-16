#这个文件中需要写一个解类，此类需要包含一个解中所有的AP分布，并包含适应度函数
location_set = [[0,0],[1,1],[2,2],[3,3]]
class solution:
    def __init__(self, location=None):
        if location is None:
            location = location_set
        self.location = location
