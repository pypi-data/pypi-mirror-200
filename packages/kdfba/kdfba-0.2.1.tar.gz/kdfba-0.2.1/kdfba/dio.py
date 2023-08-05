
### io
## 读取各种文件类型的模型，转化为cobra.Model的子类dModel
###

from pathlib import Path
from kdfba.model import dModel
from cobra.io import read_sbml_model
from cobra.io import load_json_model
from cobra.io import load_matlab_model
from cobra.io import load_yaml_model
from cobra import Model
from typing import IO, Match, Optional, Pattern, Tuple, Type, Union
import numpy as np

#  要不要做文件输出？但是dModel肯定和正常的sbml文件格式不一样
#  输出成什么形式呢？何况正常sbml文件里面是没有酶动力学模型的
#  如果要输出，只能做成dfba库自己能读取的格式，就作为拓展功能，后面有空再实现
class dio():

    # 将cobra里的Model类转换成dModel类
    # 真的可以直接这么转换吗？有点点不敢相信，后期测试多测一下
    def transfer_model2dModel(
        self,
        model: Model,
    ) -> dModel:
        return dModel(model)

    # 将读取的sbml文件转化为dModel
    def read_sbml_dModel(
        self,
        filename: Union[str, IO, Path],
        number: Type = float,
        **kwargs,
    ) -> dModel:
        return self.transfer_model2dModel(read_sbml_model(filename, number, **kwargs))

    # 将读取的json文件转化为dModel
    def load_json_dModel(self, filename: Union[str, Path, IO]) -> dModel:
        return self.transfer_model2dModel(load_json_model(filename))

    # 将读取的mat文件转化为dModel
    def load_matlab_dModel(
        self,
        infile_path: Union[str, Path, IO],
        variable_name: Optional[str] = None,
        inf: float = np.inf,
    ) -> dModel:
        return self.transfer_model2dModel(load_matlab_model(infile_path, variable_name, inf))

    def load_yaml_dModel(self, filename: Union[str, Path]) -> dModel:
        return self.transfer_model2dModel(load_yaml_model(filename))
