
from cobra.flux_analysis import flux_variability_analysis
from cobra.exceptions import OptimizationError
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple, Union
from scipy.integrate import solve_ivp
from tqdm import tqdm
import numpy as np
import pandas as pd
import re


def solve(
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
    #  按传入的model变量名储存dModel类型数据   ？？其实可以直接用models_dict[model_name]表示变量名？？？
    # model_var = globals()
    # model_names = list(models_dict.keys())
    # for model_name in model_names:
    #     model_var['%s' % model_name] = models_dict[model_name]

    #  按传入的state键作为变量名，储存对应初始浓度数据
    states_var = globals()
    model_names = list(models_dict.keys())
    states_names = list(states.keys())
    for state_name in states_names:
        if state_name in model_names:  # 处理输入的菌落初始浓度的变量命名与model变量命名相同的情况  浓度统一用x_(model名)表示
            states_var['x_%s' % state_name] = states[state_name]
        else:
            states_var['%s' % state_name] = states[state_name]

    #  调用ode求解微分方程
    with tqdm() as pbar:
        calculate_derivatives.pbar = pbar

        params = (models_dict, states, derivatives_description, loopless)
        sim_times = np.linspace(0, times, steps)
        states_values = list(states.values())
        sim_results = solve_ivp(fun=calculate_derivatives,
                                t_span=(sim_times.min(),
                                        sim_times.max()),
                                y0=states_values,
                                t_eval=sim_times,
                                rtol=1.e-6,
                                atol=1.e-6,
                                events=infeasible_event,
                                method='BDF',
                                args=(params,))

    return sim_results

def calculate_derivatives(t, states_value, params):  # 测试一下这个函数传入self会不会影响ode求解器求解，如果不会就好办了  12.15: 可以的

    #  按调用函数传入的state键作为变量名，储存这个函数传入的浓度数据
    models_dict, states, derivatives_description, loopless = params[0], params[1], params[2], params[3]

    var = globals()
    states_names = list(states.keys())
    for i in range(0, len(states_value)):
        # if states_value[i] < 0:
        #     print('%s的值为%f' % (states_names[i], states_value[i]))
        #     states_value[i] = 0
        var['%s' % states_names[i]] = states_value[i]
        # print('%s的值为%f' % (states_names[i], states_value[i]))

    ##  接下来应该是写一个for循环，一个一个模型地结合酶动力学计算FVA优化结果，得到需要的flux值

    model_names = list(models_dict.keys())
    for model_name in model_names:
        #  读取每个模型中修改后的酶动力学反应
        model_temp = models_dict[model_name]
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
                # if dreaction.reaction.lower_bound > var['flux']:
                #     dreaction.reaction.lower_bound = var['flux']
                dreaction.reaction.upper_bound = var['flux']
            elif (dreaction.bound_direction.startswith("lower")):
                # if dreaction.reaction.upper_bound < var['flux']:
                #     dreaction.reaction.upper_bound = var['flux']
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
                                                        loopless=loopless)
                
                # if(model_name == 'cyano'):
                #     print(flux_values)

            except OptimizationError:
                rows = len(sub_objectives)
                data = [[0] * 2] * rows
                flux_values = pd.DataFrame(data, columns=['minimum', 'maximum'], index=sub_objectives_str,
                                            dtype=float)

            # 用于判断是否需要结束求解的变量
            global objective_value
            objective_value = flux_values.at[sub_objectives[0].id, sub_objective_directions[0]]
            # print('可行解%f' % objective_value)

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

        #  使用FBA计算得到objective优化后的flux值  变量名为model名+_+mu   3.31：那要是目标不是biomass呢？？？还是在fva里面加入objective算了
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
    derivatives_keys = list(derivatives_description.keys())
    for state_name in states_names:
        derivative['d'] = 0
        if state_name.startswith("x_"):  # 计算菌落生长率对应时间导数
            # derivative = 0
            model_name = state_name.split("_", 1)[1]  # 得到state中的model名
            model_mu = model_name + '_mu'  # 优化后的生长率flux值变量名
            if model_mu in rxnsFluxValue_keys:  # 计算了这个菌的生长率, derivatives就不为0
                dilution_rate = models_dict[model_name].dilrate
                derivative['d'] = var[state_name] * var[model_mu] - var[
                    state_name] * dilution_rate
        elif derivatives_description[state_name] == '0' or derivatives_description[state_name] == 0:
            pass
        elif state_name in derivatives_keys:  # 要求计算这种物质时间导数  3.28 添加功能，也可以识别没有修改过的反应->完成
            # derivative = 0
            derivative_description = derivatives_description[state_name]  # 得到该物质的计算公式
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

                        # if item.startswith('cyano'):
                        #     print('%s的值为%f' % (item_temp, var[item_temp]))

                        exec('var[item] =' + model_weight + '*' + item_temp)
                    else:
                        flux = var[model_name + '_solution'].fluxes['%s' % flux_name]

                        # if item.startswith('cyano'):
                        #     print('%s的值为%f' % (flux_name, flux))

                        exec('var[item] =' + model_weight + '* flux')
                    
                    # if item.startswith('cyano'):
                    #     print('%s的值为%f' % (item, var[item]))

            exec("derivative['d']=" + derivative_description)
        # print("%s导数: %f" % (state_name, derivative['d']))
        derivatives.append(derivative['d'])

        if calculate_derivatives.pbar is not None:
            calculate_derivatives.pbar.update(1)
            calculate_derivatives.pbar.set_description('t = {:.3f}'.format(t))

    return np.array(derivatives)


def infeasible_event(t, y, args):
    global objective_value
    # print('不可行解%f' % objective_value)
    return objective_value - infeasible_event.epsilon
