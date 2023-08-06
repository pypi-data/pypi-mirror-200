'''
这个类是用来储存修改的reaction的具体情况的
三个属性: reaction, bound_direction和equation
分别代表修改反应, 修改的是反应上限还是下限, 以及酶动力学反应方程式
在dModel类中以DictList形式生成并储存
'''

from cobra import Reaction

class dReaction():
    def __init__(
        self,
        reaction: Reaction,
        bound_direction: str,
        equation: str,
        is_volume: bool
    ):
        self.reaction = reaction
        self.bound_direction = bound_direction
        self.equation = equation
        self.is_volume = is_volume
