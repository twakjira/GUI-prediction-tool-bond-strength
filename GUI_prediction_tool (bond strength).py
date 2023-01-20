#!/usr/bin/env python
# coding: utf-8

# In[4]:


# www.tadessewakjira.com/Contact

import PySimpleGUI as sg
import numpy as np
import pandas as pd
from pickle import load

#import the dataset
dd1 = pd.read_excel('data.xlsx', sheet_name = 'data')
df=dd1.copy(deep=True)

t=32
td=35

# ADD TITLE COLOUR ,title_color='white'
sg.theme('DefaultNoMoreNagging')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Developed by Wakjira T., Abushanab A., Alam M., Alnahhal W., Plevris V.')],
            [sg.Text('University of British Columbia Okanagan, Qatar University')],
#             [sg.Text('Contact: tgwakjira@gmail.com, www.tadessewakjira.com/Contact')],
            #[sg.Text('Input parameters')],
          
            [sg.Frame(layout=[
            [sg.Text('Concrete compressive strength (fc)',size=(td, 1)), sg.Text('23 MPa ≤ fc ≤ 52.1 MPa')],
            [sg.Text('Reinforcement type (1:Smooth, 2:Deformed)',size=(td, 1)), sg.Text('1:Smooth,    2:Deformed')],
            [sg.Text('Steel yield strength (fy)',size=(td, 1)), sg.Text('290 MPa ≤ fy ≤ 606 MPa')],
            [sg.Text('Corrosion level',size=(td, 1)), sg.Text('0.10 ≤ CL ≤ 18.75')],
            [sg.Text('Concrete cover-to-bar diameter ratio (cc/db)',size=(td, 1)), sg.Text('0.78 ≤ cc/db ≤ 5.90')],
            [sg.Text('Bar diameter-to-bonded length ratio (db/lb)',size=(td, 1)), sg.Text('0.04 ≤ db/lb ≤ 0.28')],
            [sg.Text('Test type (0: Pull-out; 1:Beam)',size=(td, 1)), sg.Text('0:Pull-out,    1:Beam')]],
            title='Range of application of the models')],
            
            [sg.Frame(layout=[
            [sg.Text('Make sure the values are in the range of application listed above for all parameters.')],
            [sg.Text('Reinforcement type: Input values of 1 and 2 for smooth and deformed bars, respectively')],
            [sg.Text('Test type: Input values of 0 and 1 for pull-out and beam specimens, respectively')]],
            title='Important notes')],
          
            [sg.Frame(layout=[
            [sg.Text('Concrete compressive strength',size=(t, 1)),sg.InputText(key='-f1-'),sg.Text('MPa')],
            [sg.Text('Reinforcement type (1:Smooth, 2:Deformed)',size=(t, 1)), sg.InputText(key='-f2-'),sg.Text('--')],
            [sg.Text('Steel yield strength',size=(t, 1)), sg.InputText(key='-f3-'),sg.Text('MPa')],
            [sg.Text('Corrosion level',size=(t, 1)), sg.InputText(key='-f4-'),sg.Text('%')],
            [sg.Text('Concrete cover-to-bar diameter ratio',size=(t, 1)), sg.InputText(key='-f5-'),sg.Text('--')],
            [sg.Text('Bar diameter-to-bonded length ratio',size=(t, 1)), sg.InputText(key='-f6-'),sg.Text('--')],
            [sg.Text('Test type (0: Pull-out; 1:Beam)',size=(t, 1)), sg.InputText(key='-f7-'),sg.Text('--')]],
            title='Input parameters')],
          
            [sg.Frame(layout=[   
            [sg.Text('Bond strength',size=(t, 1)), sg.InputText(key='-OP-',size=(t+13, 1)),sg.Text('MPa')]],
                      title='Output')],
            [sg.Button('Predict'),sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Super learner ML-aided concrete/steel bond strenght prediction', layout)

filename = 'main1_model.pkl'
model = load(open(filename, 'rb'))
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    #window['-OP-'].update('Please fill all the input parameters')
    if event == 'Predict':
        #window['-OP-'].update(values[0])
        #break
        if values['-f1-'] == '' or values['-f2-'] == '' or values['-f3-'] == '' or values['-f4-'] == '' or values['-f5-'] == '' or values['-f6-'] == '' or values['-f7-'] == '':

            window['-OP-'].update('Please fill all the input parameters')

        else:

            df11=np.array([[float(values['-f1-']),float(values['-f2-']), float(values['-f3-']),float(values['-f4-']),float(values['-f5-']),
                            float(values['-f6-']),float(values['-f7-'])]])
#             df11=np.array([[values['-f1-'],values['-f2-'], values['-f3-'],values['-f4-'],values['-f5-'],values['-f6-'],values['-f7-']]])

            df1=pd.DataFrame(df11)
#             # normalize the user defined variables
            dfn=[]
            for i in range(0,df1.shape[1]):
#                 a = (df1.iloc[:,i]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                a = (df1.iloc[:,i][0]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                dfn.append(a)

            dfn = pd.DataFrame(np.array(dfn)).T.values
            
            y_pred = model.predict(dfn)[0]
            
            # Inverse normalization
            # observed responses
            yy1 = df['tmax (MPa)'].values

            # predicted responses
            y1=round(yy1.min()+(yy1.max()-yy1.min()) * y_pred, 2)
        
            
            window['-OP-'].update(np.round(y1,2))
            

window.close()


# In[ ]:





# In[ ]:




