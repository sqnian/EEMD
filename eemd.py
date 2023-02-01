import pandas as pd
import numpy as np
from PyEMD import EEMD 
from Visualisation  import Visualisation  # 可视化
"""
pip3 install EMD-signal
"""

##载入时间序列数据
def get_data(path,i):
    data = pd.read_csv(path,usecols=[i])
    data = data.values
    return data


def get_eemd(data):
    """
    信号参数：
    N:采样频率500Hz
    tMin:采样开始时间
    tMax:采样结束时间 2*np.pi
    """
    data_value = data[:,0]
    T = np.arange(0,len(data_value),1)  # t 表示横轴的取值范围

    eemd = EEMD(trials=50)
    eemd.noise_seed(12345)

    # 获得分量
    E_IMFs = eemd.eemd(data_value, T)
    return E_IMFs 

def plot_imf(data_value,E_IMFs):
    t = np.arange(0,len(data_value),1)  # t 表示横轴的取值范围
    vis = Visualisation()
    # 分量可视化
    vis.plot_imfs(imfs=E_IMFs,  t=t , include_residue=False)
    path = "./eemd_imf.png"
    vis.save(path)

    # 频率可视化
    vis.plot_instant_freq(t=t ,imfs=E_IMFs)
    vis.show()
    path = "./eemd_instant_freq.png"
    vis.save(path)
    

# 保存分量
def save_imf(E_IMFs):
    for i  in range(len(E_IMFs)):
        a = E_IMFs[i]
        dataframe = pd.DataFrame({'E_IMFs{}'.format(i+1):a})
        dataframe.to_csv(r"E_IMFs-%d.csv"%(i+1),index=False,sep=',')
    
  

def test():
    path = "sample.csv"
    data = get_data(path,0)

    E_IMFs  = get_eemd(data)

    plot_imf(data,E_IMFs)

    save_imf(E_IMFs)

if  __name__ =="__main__":
    test()
