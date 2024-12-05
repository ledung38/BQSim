# BSim-python

BSim-Python
This is the BlueQuant simulation tool for backtesting models.

# Requirements

- Python
- Numpy
  Download Python: https://www.python.org/downloads/
  To install the required libraries, from the BQSim root directory, Open CMD, run :
  > `pip install -r requirement.txt`

To install TA-Lib, follow the instructions on the page "https://pypi.org/project/TA-Lib/" and install it according to your operating system.

For example, on Windows, download the release file matching your version from https://github.com/cgohlke/talib-build/releases

In the folder containing the file you just downloaded, run:

> `py.exe -3.13 -m pip install ta_lib-0.5.1-cp313-cp313-win_amd64.whl`

1. # Run sample alphas

In the alphas/alpha1 folder contains the code and config files of the sample alpha. We can cp alpha2 or edit directly to alpha1.

Edit file alphas/alpha1.xml as follow:

- In the line: data_path="PATH_DATA_SOURCE", change PATH_DATA_SOURCE to the path of binance data path, for example: data_path="../bluequant/daily"
- Make sure all processor attributes are set with the correct paths, for example processor="../data_loader/binance_base_data_loader_v2.py"
- alphaId and path: id="alpha1" processor="alpha1/alpha1.py"

From the BQSim root directory, run the following command:

> `cd alphas`

> `python ../BSim.py alpha1/alpha1.xml`

# Data

The sample data source can be downloaded [Here](https://drive.google.com/file/d/163c0Gzzwthnc9EVlFtD22sCogODIdJ8w/view?usp=sharing)

2. # BlueQuant-alpha-tools

BlueQuant alpha tools

# Requirements

- Python
- Matplotlib

# PNL Summary

To print the summary of a PNL file (one alpha at a time), from the BQSim root directory, run:

> `cd alphas`

> `python ../alpha-tools/pnl_summary.py pnl/alpha1`

The output will be like

```
   START-     END    LONG  SHORT      PNL    TVR   RET     IR
20220101-20221231   500.0  500.0    513.2   36.6  50.1  0.084
20230101-20231231   500.0  500.0    394.3   34.8  38.5  0.055
20240101-20240720   500.0  500.0    599.3   33.6 105.6  0.080

20220101-20240720   500.0  500.0   1506.8   35.2  57.6  0.068
```

# Plot PNL

Plot pnl chart of alphas, can plot multiple alphas in one graph

> `python ../alpha-tools/pnl_plot.py pnl/alpha1`

The graph is like below
![Figure_1](https://github.com/user-attachments/assets/3450e777-a006-4dbb-a21c-ccd070049dad)
