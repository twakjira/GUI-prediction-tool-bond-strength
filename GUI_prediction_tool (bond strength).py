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
td2=8

# define the range of values for each parameter
reinforcement_type_range = [1, 2]
test_type_range = [0, 1]

fc_range = [23, 52.1]
fy_range = [290, 606]
cl_range = [0.1, 18.75]
ccdb_range = [0.78, 5.9]
db_lb_range = [0.04, 0.28]


sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Text('Developed by Wakjira T., Abushanab A., Alam MS., Alnahhal W., Plevris V.')],
            [sg.Text('University of British Columbia Okanagan, Qatar University')],
#             [sg.Text('Contact: tgwakjira@gmail.com, www.tadessewakjira.com/Contact')],
            #[sg.Text('Input parameters')],
    [
      sg.Column(layout=[
            [sg.Frame(layout=[
            [sg.Text('Concrete compressive strength',size=(t, 1)),sg.InputText(key='-f1-', size=(td2,1)),sg.Text('MPa')],
            [sg.Text('Reinforcement type (1:Smooth, 2:Deformed)',size=(t, 1)), sg.InputCombo(reinforcement_type_range, key='-f2-', 
                                                                                 default_value = 2,size=(td2, 1)),sg.Text('--')],
            [sg.Text('Steel yield strength',size=(t, 1)), sg.InputText(key='-f3-', size=(td2,1)),sg.Text('MPa')],
            [sg.Text('Corrosion level',size=(t, 1)), sg.InputText(key='-f4-', size=(td2,1)),sg.Text('%')],
            [sg.Text('Concrete cover-to-bar diameter ratio',size=(t, 1)), sg.InputText(key='-f5-', size=(td2,1)),sg.Text('--')],
            [sg.Text('Bar diameter-to-bonded length ratio',size=(t, 1)), sg.InputText(key='-f6-', size=(td2,1)),sg.Text('--')],
            [sg.Text('Test type (0: Pull-out; 1:Beam)',size=(t, 1)), sg.InputCombo(test_type_range, key='-f7-', 
                                                                       default_value = 0,size=(td2, 1)),sg.Text('--')]],
            title='Input parameters')],
        ], justification='left'),
        
            
            
            sg.Column(layout=[
            [sg.Frame(layout=[
            [sg.Text('23 MPa ≤ fc ≤ 52.1 MPa')],
            [sg.Text('1:Smooth,    2:Deformed')],
            [sg.Text('290 MPa ≤ fy ≤ 606 MPa')],
            [sg.Text('0.10 ≤ CL ≤ 18.75')],
            [sg.Text('0.78 ≤ cc/db ≤ 5.90')],
            [sg.Text('0.04 ≤ db/lb ≤ 0.28')],
            [sg.Text('0:Pull-out,    1:Beam')]],
            title='Range of application of the models')],
            
            
            
        ], justification='center') 
  ],
[sg.Frame(layout=[   
            [sg.Text('Bond strength',size=(32, 1)), sg.InputText(key='-OP-', size=(td2,1)),sg.Text('MPa')]],
                      title='Output')],
            [sg.Button('Predict'),sg.Button('Cancel')]
]


# layout = [    
    
#             [sg.Frame(layout=[   
#             [sg.Text('Bond strength',size=(32, 1)), sg.InputText(key='-OP-',size=(32+13, 1)),sg.Text('MPa')]],
#                       title='Output')],
#             [sg.Button('Predict'),sg.Button('Cancel')] ]


# Open the images
img1 = Image.open('image1.png')
img2 = Image.open('image2.png')

# Get the original size of the images
width, height = img1.size
width2, height2 = img2.size

# Define the scale factor
scale_factor = 0.43

# Resize the images
img1 = img1.resize((int(width * scale_factor), int(height * scale_factor)))
img2 = img2.resize((int(width2 * scale_factor), int(height2 * scale_factor)))

# Save the resized images
img1.save('image11.png')
img2.save('image22.png')


# To add figures in two columns
fig1 = sg.Image(filename='image11.png', key='-fig1-', size=(width * scale_factor,height * scale_factor))
fig2 = sg.Image(filename='image22.png', key='-fig2-', size=(width2 * scale_factor,height2 * scale_factor))

# # To add description of the image
# fig1_desc = sg.Text('Image 1')
# fig2_desc = sg.Text('Image 2')

# To layout the figures and descriptions in two columns
layout += [[sg.Text(' ')],
           [sg.Text('Summary plot and global importance of the input features')],
    [fig1, fig2], 
#            [fig1_desc, fig2_desc]
          ]
# layout += [
#     sg.Column(
#         layout=[
#             [fig1],
#             [fig1_desc]
#         ],
#         justification='center'
#     ),
#     sg.VerticalSeparator(),
#     sg.Column(
#         layout=[
#             [fig2],
#             [fig2_desc]
#         ],
#         justification='center'
#     )
# ]


# Create the Window
window = sg.Window('Super learner ML-aided concrete/steel bond strenght prediction', layout)

filename = 'main1_model.pkl'
model = load(open(filename, 'rb'))

while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    elif event == 'Predict':
        try:
            # get the input values
            fc = float(values['-f1-'])
            reinforcement_type = int(values['-f2-'])
            fy = float(values['-f3-'])
            cl = float(values['-f4-'])
            ccdb = float(values['-f5-'])
            db_lb = float(values['-f6-'])
            test_type = int(values['-f7-'])
            
            # check if the input values are within the defined range
            if fc < fc_range[0] or fc > fc_range[1]:
                sg.popup("Concrete compressive strength (fc) must be between 23 MPa and 52.1 MPa.")
                continue
            if reinforcement_type not in reinforcement_type_range:
                sg.popup("Reinforcement type must be 1 for smooth bars or 2 for deformed bars.")
                continue
            if fy < fy_range[0] or fy > fy_range[1]:
                sg.popup("Steel yield strength (fy) must be between 290 MPa and 606 MPa.")
                continue
            if cl < cl_range[0] or cl > cl_range[1]:
                sg.popup("Corrosion level must be between 0.1% and 18.75%.")
                continue
            if ccdb < ccdb_range[0] or ccdb > ccdb_range[1]:
                sg.popup("Concrete cover-to-bar diameter ratio (cc/db) must be between 0.78 and 5.9.")
                continue
            if db_lb < db_lb_range[0] or db_lb > db_lb_range[1]:
                sg.popup("Bar diameter-to-bonded length ratio (db/lb) must be between 0.04 and 0.28.")
                continue
            if test_type not in test_type_range:
                sg.popup("Test type must be 0 for pull-out specimens or 1 for beam specimens.")
                continue
            
            df11=np.array([[fc, reinforcement_type, fy, cl, ccdb, db_lb, test_type]])
            df1=pd.DataFrame(df11)
#           # normalize the user defined variables
            dfn=[]
            for i in range(0,df1.shape[1]):
#                 a = (df1.iloc[:,i]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                a = (df1.iloc[:,i][0]-df.iloc[:,i].min())/(df.iloc[:,i].max()-df.iloc[:,i].min())
                dfn.append(a)

            dfn = pd.DataFrame(np.array(dfn)).T.values           
            
            # make the prediction
            prediction = model.predict(dfn)[0]
            y_pred = prediction
            
            # Inverse normalization
            # observed responses
            yy1 = df['tmax (MPa)'].values

            # predicted responses
            y1=round(yy1.min()+(yy1.max()-yy1.min()) * y_pred, 2)
            
            window['-OP-'].update(np.round(y1,2))
  
        except:
            sg.popup("Invalid input. Please make sure to enter numeric values and make sure the input values are within the defined range.")
            continue         
                    
            
window.close()
