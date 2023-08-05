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


from cobra.flux_analysis import flux_variability_analysis
from cobra.exceptions import OptimizationError
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple, Union
from scipy.integrate import solve_ivp
from tqdm import tqdm
import numpy as np
import pandas as pd
import re


class solver():

    def __init__(self):
        self.models_dict = dict()
        self.states = dict()
        self.derivatives_description = dict()
        self.states_var = globals()
        self.loopless = False

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
        #  类属性赋值
        self.models_dict = models_dict
        self.states = states
        self.derivatives_description = derivatives_description
        self.loopless = loopless

        #  按传入的model变量名储存dModel类型数据   ？？其实可以直接用models_dict[model_name]表示变量名？？？
        # model_var = globals()
        # model_names = list(models_dict.keys())
        # for model_name in model_names:
        #     model_var['%s' % model_name] = models_dict[model_name]

        #  按传入的state键作为变量名，储存对应初始浓度数据
        model_names = list(models_dict.keys())
        states_names = list(states.keys())
        for state_name in states_names:
            if state_name in model_names:  # 处理输入的菌落初始浓度的变量命名与model变量命名相同的情况  浓度统一用x_(model名)表示
                self.states_var['x_%s' % state_name] = states[state_name]
            else:
                self.states_var['%s' % state_name] = states[state_name]

        #  调用ode求解微分方程
        sim_times = np.linspace(0, times, steps)
        states_values = list(states.values())
        sim_results = solve_ivp(fun=self.__calculate_derivatives,
                                t_span=(sim_times.min(),
                                        sim_times.max()),
                                y0=states_values,
                                t_eval=sim_times,
                                rtol=1.e-6,
                                atol=1.e-6,
                                method='BDF')

        return sim_results

    def __calculate_derivatives(self, t, states_value):  # 测试一下这个函数传入self会不会影响ode求解器求解，如果不会就好办了  12.15: 可以的

        #  按调用函数传入的state键作为变量名，储存这个函数传入的浓度数据
        states_names = list(self.states.keys())
        for i in range(0, len(states_value)):
            self.states_var['%s' % states_names[i]] = states_value[i]

        ##  接下来应该是写一个for循环，一个一个模型地结合酶动力学计算FVA优化结果，得到需要的flux值
        var = globals()

        model_names = list(self.models_dict.keys())
        for model_name in model_names:
            #  读取每个模型中修改后的酶动力学反应
            model_temp = self.models_dict[model_name]
            dreactions = model_temp.dReactions
            # flux_value = globals()

            #  根据酶动力学模型计算flux值
            for dreaction in dreactions:
                var['flux'] = 0
                if dreaction.is_volume:  # 以体积为单位，则计算flux时需要转化单位
                    exec(
                        "var['flux'] = (" + dreaction.equation + ') * (model_temp.volume / model_temp.weight)')  ## ？？测试一下state里没有eqution对应物质的情况
                else:
                    exec("var['flux'] = " + dreaction.equation)

                if dreaction.bound_direction.startswith("upper"):
                    dreaction.reaction.upper_bound = var['flux']
                elif (dreaction.bound_direction.startswith("lower")):
                    dreaction.reaction.lower_bound = var['flux']
                elif (dreaction.bound_direction.startswith("both")):
                    dreaction.reaction.upper_bound = 1000
                    dreaction.reaction.lower_bound = -1000  ## 避免上下限调整时出bug
                    dreaction.reaction.upper_bound = var['flux']
                    dreaction.reaction.lower_bound = var['flux']

            #  使用FVA计算得到优化后的flux值  ？？测试一下不可解的情况，该怎么处理？
            ##  03.08  直接在fva处计算obj，不在后面单独计算了  PS.objective取不到id，放弃

            sub_objectives = model_temp.sub_objectives
            if sub_objectives is not None:
                sub_objectives_str = [sub_objective.id for sub_objective in sub_objectives]
                sub_objective_directions = model_temp.sub_objective_directions
                try:
                    flux_values = flux_variability_analysis(model_temp, reaction_list=sub_objectives,
                                                            fraction_of_optimum=model_temp.fraction_of_optimum,
                                                            loopless=self.loopless)
                except OptimizationError:
                    rows = len(sub_objectives)
                    data = [[0] * 2] * rows
                    flux_values = pd.DataFrame(data, columns=['minimum', 'maximum'], index=sub_objectives_str,
                                               dtype=float)
                # print(flux_values)

                #  得到次级目的反应的flux值，变量名为model名+_+reaction_id
                # rxnsFluxValue = globals()
                for i in range(0, len(sub_objectives)):
                    ##  这里就表示如果要算某些反应的flux值(比如时间导数那里有这个反应的话)，就必须加入到sub_objectives中. 不过也可以优化，只不过到时候要在solution里面去找对应的
                    var[model_name + '_M_' + sub_objectives[i].id] = flux_values.at[
                        sub_objectives[i].id, sub_objective_directions[i]]
                    ##  加入一个环节  由于设定了几个次级目的反应的flux值，必将影响主要优化目标的flux值，所以把计算得到的次级目的反应flux值给赋值回去再计算objective
                    ##  好像没啥用，反正都是在这个线性空间里面去求解objective的最大最小值，除非把上下限设置得紧密一些
                    # sub_objectives[i].upper_bound = 1000
                    # sub_objectives[i].lower_bound = -1000  ## 避免上下限调整时出bug
                    # sub_objectives[i].upper_bound = flux_values.at[sub_objectives[i].id, "maximum"]
                    # sub_objectives[i].lower_bound = flux_values.at[sub_objectives[i].id, "minimum"]

            #  使用FBA计算得到objective优化后的flux值  变量名为model名+_+mu
            solution = model_temp.optimize()
            if solution.status == "infeasible":
                var[model_name + '_mu'] = 0
                solution.fluxes = solution.fluxes * 0
                var[model_name + '_solution'] = solution
            else:
                var[model_name + '_mu'] = solution.objective_value
                var[model_name + '_solution'] = solution

        ##  最后是根据输入的时间导数公式和优化后得到的flux，计算时间导数并得到外界物质浓度变化情况
        derivatives = []
        derivative = globals()
        rxnsFluxValue_keys = list(var.keys())
        derivatives_keys = list(self.derivatives_description.keys())
        for state_name in states_names:
            derivative['d'] = 0
            if state_name.startswith("x_"):  # 计算菌落生长率对应时间导数
                # derivative = 0
                model_name = state_name.split("_", 1)[1]  # 得到state中的model名
                model_mu = model_name + '_mu'  # 优化后的生长率flux值变量名
                if model_mu in rxnsFluxValue_keys:  # 计算了这个菌的生长率, derivatives就不为0
                    dilution_rate = self.models_dict[model_name].dilrate
                    derivative['d'] = self.states_var[state_name] * var[model_mu] - self.states_var[
                        state_name] * dilution_rate
            elif self.derivatives_description[state_name] == '0' or self.derivatives_description[state_name] == 0:
                pass
            elif state_name in derivatives_keys:  # 要求计算这种物质时间导数  3.28 添加功能，也可以识别没有修改过的反应->完成
                # derivative = 0
                derivative_description = self.derivatives_description[state_name]  # 得到该物质的计算公式
                items = re.split('[+-]', derivative_description)

                reactions = globals()
                for item in items:
                    if item != '':
                        item = item.strip()
                        model_name = (item.split("_", 1)[0])
                        flux_name = (item.split("_", 1)[1])

                        model_weight = 'x_' + model_name
                        item_temp = model_name + '_M_' + flux_name

                        if item_temp in reactions.keys():
                            exec('var[item] =' + model_weight + '*' + item_temp)
                        else:
                            print(model_name)
                            print(flux_name)
                            flux = var[model_name + '_solution'].fluxes['%s' % flux_name]
                            exec('var[item] =' + model_weight + '* flux')
                exec("derivative['d']=" + derivative_description)
            # print("%s导数: %f" % (state_name, derivative['d']))
            derivatives.append(derivative['d'])

        return np.array(derivatives)
