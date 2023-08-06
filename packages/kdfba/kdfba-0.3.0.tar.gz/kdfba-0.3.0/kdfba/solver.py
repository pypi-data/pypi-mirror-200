# 使用odint求解fba递进循环过程
''''''  # 总体思路
###
# 1.首先读取模型列表，需要修改的reaction列表，初始状态列表
## 怎么对应list中每个元素的model？（可变变量？外界传入字典？）
## (需不需要用字典，让用户从外界输入reaction方程和对应的reation在model中的名称，或者在输入之前就在model中改好？)
## 怎么对应list中每个元素的物质初始浓度？
## 怎么对应list中每个元素和传入众多model中的metabolite id(可能不需要)
# 2.根据反应修改的参考，对对应的reaction上下限进行重设（怎么对应？）
# 3.修改fba优化目标
### 以上，我觉得提前在各个model中改好再传进来最好。 缺点：每个simulate只能对应一种特定情况，不过也还行
# 4.计算时间导数

###
''''''

''''''  # 其他类的设计
### io
## 读取各种文件类型的模型，转化为cobra.Model的子类
###

### cobra.Model的子类model
## 读取字符串形式的酶动力学模型并修改对应reaction上下限的方法
## 修改优化目标的方法
###
''''''

### solver
## simulate方法：读取需要模拟的model列表，模拟时长，初始物质浓度状态，（时间导数对应关系？），返回odeint求解高维列表
###


import dfba.tool as tool


class solver():

    def simulate(
        self,
        ## 12.11补充: 要不也用dict来表示，键为自己取名的变量名，值为对应dModel类型数据
        models_dict: dict,  # 暂时是一个model，后面应该会做成队列的model
        states: dict,  # 各种物质的初始状态，用字典来表示吧，键是物质名(菌浓度用x_(model名)表示), 值是浓度(或flux)值
        ##  还需要一个参数，来表示导数关系，即计算多种菌同时影响的一种物质的变化情况
        ###  每一个通过FVA计算出来的flux值变量命名按照  model名+_+reaction_id命名  例如 iAF1260_phe_Ec4_upd
        ###  所以时间导数可以大概写成  iAF1260菌干重值*iAF1260_(reaction_id) ± iND1260菌干重值*iND1260_(reaction_id)
        ###  传入参数以字典形式  键是物质名词，值是 (model1)_(reaction_id1) ± (model2)_(reaction_id2)...
        derivatives_description: dict,
        times: float,  # 模拟时长, 单位h
        steps=100,  # 模拟步数, 步数越多越精确, 后期可以再测试一下最佳范围
        ##  或许还可以加一个dilution rate参数(加在这里还是加在dModel里面？？)  02.21 加在dModel里面了
        loopless=False  ##  还可以再加入一个loopless参数，在FVA计算时使用loopless算法会更精确但运算量更大
    ):
        tool.infeasible_event.epsilon = 1e-6
        tool.infeasible_event.direction = -1
        tool.infeasible_event.terminal = True

        tool.calculate_derivatives.pbar = None

        result = tool.solve(models_dict, states, derivatives_description, times, steps, loopless)
        return result
