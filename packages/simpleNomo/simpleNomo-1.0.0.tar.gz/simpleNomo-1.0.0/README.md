### Project Description

simpleNomo is a python package for generating nomograms of logistic regression models with only model coefficients and variables ranges.  

#### Backgroud
Nomogram, a graphical calculator, has adequately solved the problem of inconvenient calculation. Nomogram is a chart consisting of several arranged lines for visualization of logistic regression model. With the development of the electronic calculators and computers, nomograms become less popular these days. However, they are still very prevalent in the condition without the computation sources. There are several tools for generating nomograms. They are available in SAS, Stata, as well as **rms** and **hdnom** packages in R language.

However, these tools either lack an integrated toolbox such as SAS or take input only from model trained within the programming language like hdnom and rms. In this case, it is difficult for converting existing works that established logistic regression models but not published the training data or developed nomograms. Therefore, plenty of works will stagnate into logistic regression models with good performance rather than meaningful clinical applications.  

simpleNomo is a straightforward framework for creating nomograms for logistic regression models. PyNG can accepts only the coefficients
and range of predictors in a logistic regression model as inputs.

#### Requirements
```txt
pandas==1.2.4
numpy==1.21.5
matplotlib==3.5.1
```

#### To install
```terminal
pip install simpleNomo
```
Or more specifically at <https://github.com/Hhy096/nomogram>.

#### Function Introduction
```python
nomogram(path, result_title="Positive Risk", fig_width=10, single_height=0.45, dpi=300,
         ax_para = {"c":"black", "linewidth":1.3, "linestyle": "-"},
         tick_para = {"direction": 'in', "length": 3, "width": 1.5,},
         xtick_para = {"fontsize": 10, "fontfamily": "Songti Sc", "fontweight": "bold"},
         ylabel_para = {"fontsize": 12, "fontname": "Songti Sc", "labelpad":100, 
                        "loc": "center", "color": "black", "rotation":"horizontal"},
         total_point=100)
```
- **path:** Path of the excel that reserves the model coefficients and variabels range. The template of excel can be downloade at https://github.com/Hhy096/nomogram/blob/main/template.xlsx.
- **result_title:** Title for the predictive name. Default "Positive Risk".
- **fig_width:** Width for the figure. Default 10.
- **single_height:** Hight for each axis of the nomogram. Default 0.45.
- **dpi:** The resolution in dots per inch. Default 300.
- **ax_para:** The parameters for axises in the nomogram. You can find more from *Other Parameters* part in https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.axhline.html.
- **tick_para:** The parameters for probability matching axis. You can find more in https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.tick_params.html.
- **xtick_para:** The parameters for x-ticklables of axises. You can find more paramters in https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text.
- **ytick_para:** The parameters for y-ticklabels of axises. You can find more paramters in https://matplotlib.org/stable/api/text_api.html#matplotlib.text.Text.
- **total_point:** The maximum point for aixes. Default 100.


#### Example
Check https://github.com/Hhy096/nomogram for more examples.