# -*- coding: utf-8 -*-
"""Visualization Project

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zvf1RSt_zN-zsXilstIoNHMWEWA3mAB5
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
# %matplotlib inline

#reading CSV, checking nulls, shape, columns and info

#link to dataset: https://www.kaggle.com/datasets/akshaydattatraykhare/diabetes-dataset/

path = "diabetes.csv"
df = pd.read_csv(path)
df.head()
df.isnull().sum()
df.columns
df.describe()
df.corr()
df.info()

df.shape #data set size

#initializing variables

mean_glucose_per_age = df[["Glucose", "Age"]].groupby(as_index=False, by = "Age").mean()
mean_glucose_per_age

X= mean_glucose_per_age["Age"]
Y = mean_glucose_per_age["Glucose"]
plot_title = "Average Glucose Level vs Age"
x_label = "Age"
y_label = "Average Glucose"

#MATPLOTLIB

ax = plt.scatter(X, Y, color="green", marker="o")
plt.ylim(0,)
plt.title(plot_title)
plt.xlabel(x_label)
plt.ylabel(y_label)

#SEABORN

sns.set_theme(style="whitegrid", palette="Spectral")
seaborn_plot = sns.scatterplot(x = X, y = Y)
seaborn_plot.set(title = plot_title, xlabel= x_label, ylabel=y_label, ylim=(0,180))

#PLOTLY

fig = px.scatter(mean_glucose_per_age, x="Age", y="Glucose", title = plot_title, labels={"Age":x_label, "Glucose":y_label}, color='Age')
fig.update_layout(plot_bgcolor="lightgray")
fig.update_yaxes(range=[0, 180], row=1, col=1)
fig.show()

df.describe()

bins=np.linspace(df['Age'].min(),df['Age'].max(),5)

bins

labels=['21-35','36-50','51-65','66-81']
df['Age-bins']=pd.cut(df['Age'],bins,labels=labels,include_lowest=True)

df[['Age','Age-bins','Outcome']]

df_dia=df[df['Outcome']==1]

!pip install pywaffle

df_dia1=df_dia.groupby(by=['Age-bins']).count() #number of patients with diabetes for different age categories

# import Waffle from pywaffle
from pywaffle import Waffle

#Set up the Waffle chart figure

fig = plt.figure(FigureClass = Waffle,
                 rows = 20, columns = 30, #pass the number of rows and columns for the waffle
                 values = df_dia1['Outcome'], #pass the data to be used for display
                 cmap_name = 'tab20', #color scheme
                 legend = {'labels': [f"{k} ({v})" for k, v in zip(df_dia1.index.values,df_dia1['Outcome'])],
                            'loc': 'lower left', 'bbox_to_anchor':(0,-0.1),'ncol': 4}
                 #notice the use of list comprehension for creating labels
                 #from index and total of the dataset
                )

#Display the waffle chart
plt.show()

sns.regplot(x="BMI",y="Glucose",data=df)

df[df['BMI']==0]

df=df[df['Glucose']!=0 ]

df=df[df['BMI']!=0 ]

df[df['Glucose']==0]

sns.regplot(x="Glucose",y="Insulin",data=df)

sns.regplot(x="BMI",y="Glucose",data=df)

sns.regplot(x="BloodPressure",y="Glucose",data=df)

df=df[df['BloodPressure']!=0]

sns.regplot(x="BloodPressure",y="Glucose",data=df)

sns.boxplot(x="Outcome",y="Glucose",data=df)

sns.boxplot(x="Outcome",y="BMI",data=df)

!pip install pyngrok

from pyngrok import ngrok
ngrok.kill()
NGROK_AUTH_TOKEN = "2Irwzpl15ewCiLLfkoTaiQN0YS3_mfT7Grs29VK5VZ1j14N4"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)
ngrok.connect(8050)

!pip install dash
!pip install plotly

import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Create a Dash application and give it a meaningful title
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div([
        html.H1('Diabetes Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 24}),

        # Plot 1: Average Glucose Level vs Age
        dcc.Graph(
            id='glucose_vs_age',
            figure=px.scatter(
                mean_glucose_per_age,
                x="Age",
                y="Glucose",
                labels={"Age": "Age", "Glucose": "Glucose (mg/dL)"},
                title="Average Glucose Level vs Age"
            )
        )]),
    html.Div([

        #Plot 2: Glucose Levels vs Blood Pressure
        dcc.Graph(
            id="glucose_vs_blood_pressure",
            figure=px.scatter(
                df,
                x="BloodPressure",
                y="Glucose",
                labels={"BloodPressure": "Blood Pressure (mm Hg)", "Glucose": "Glucose (mg/dL)"},
                trendline="ols",  # Ordinary Least Squares regression line -- used instead of sns.regplot because dash expects 2 plotly graphs. did not work with seaborn's regplot
                title="Glucose vs Blood Pressure"
            )
        )])
])

if __name__ == '__main__':
    app.run_server(debug=True)

