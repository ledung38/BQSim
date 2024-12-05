# BSim-python
This is BlueQuant simulation tool to backtest model

# Requirements
+ Python
+ Numpy

# Run sample alphas
Edit file sample/config.xml as follow:
+ In the line: data_path="PATH_DATA_SOURCE", change PATH_DATA_SOURCE to the path of binance data path, for example: data_path="/home/joe/binance/data"
+ Make sure all processor attributes are set with the correct paths, for example processor="../data_loader/binance_base_data_loader.py" 

In the Params tag at the beginning, there is data_dir="./data", that tells where BSim will store working data, so make sures the directory, in this case ./data, has been created.

Command to run: 
```
python3 ../BSim.py config.xml
```
# Run combo alpha
## Save alpha position to file
See sample config file sample/config_save_alpha_pos.xml for how to save alpha position to file 

## Run combo
After we save individual alpha positions to files, we can make combo alpha from those alphas. See sample config sample/config_combo.xml 

# Data
The sample data source can be downloaded [Here](https://drive.google.com/file/d/163c0Gzzwthnc9EVlFtD22sCogODIdJ8w/view?usp=sharing)

