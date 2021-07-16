
### ---------------------------- Imports ---------------------------- ###
import os
import shutil
import numpy as np
import pandas as pd
import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session


# User Defined #
from app import app
from layouts import layout1
from adi_read import AdiParse
from create_user_table import dashtable
from tree import drawSankey
# import callbacks
### ----------------------------------------------------------------- ###


# init dash app with css style sheets
app = dash.Dash(__name__ , external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'] )
app.server.secret_key = os.urandom(24)

# Define main layout
app.layout = html.Div(children = [
    
    html.Div(children = layout1), 
])


### ---------- Update Colony Table--------- ###
@app.callback(
    [Output('user_table', "columns"), 
    Output('user_table', 'data'),
    Output('user_table', 'row_deletable'),
    Output('user_table', 'dropdown')
    ],

    [Input('add_row_button', 'n_clicks')],
    # [State("user_table","data")]
    )
def colony_update( n_clicks):

    # get data in dash table format
    # session.update({'df': pd.read_csv(temp_user_table)})
    dash_cols, df, drop_dict = dashtable(pd.read_csv(temp_user_table)) # get dashtable data

    print(n_clicks)
    if n_clicks > 0: # Add rows when button is clicked
        
        a = np.empty([1, len(df.columns)]) # create empty numpy array
        a[:] = np.nan # convert all to nans
        append_df = pd.DataFrame(a, columns = df.columns) # create dataframe
        df = df.append(append_df, ignore_index=True) # append dataframe

    # # get dataframe
    # dash_cols, df, drop_dict = dashtable(pd.DataFrame(table_data))  # get dashtable data

    return dash_cols, df.to_dict('records'), True, drop_dict


# Retrieve path and plot tree diagram
@app.callback(
    [Output('out_all_types', 'children'),
     Output('tree_plot_div', 'children')],
    [Input('generate_button', 'n_clicks')],
    [State('data_path_input', 'value')],
)
def update_output(n_clicks, folder_path):

    if folder_path is None:
        folder_path = 'empty'
    try:
        # initiate object        
        adi_read = AdiParse(folder_path)

        # get grouped dataframe
        df, unique_groups = adi_read.get_unique_conditions()

        # Get sankey plot as dcc graph
        graph = dcc.Graph(id = 'tree_structure', figure =  drawSankey(df))

    except Exception as err:
        return 'Got ' + str(folder_path) + ': ' + str(err)
    return str(folder_path), graph


if __name__ == '__main__':

    # get table
    # get csv path with user input
    file_ext = '.csv'
    user_table_path = 'example_data/default_table_data'

    # file that will be altered by user
    temp_user_table =  user_table_path + '_copy' + file_ext

    shutil.copy(user_table_path + file_ext, temp_user_table)

    app.run_server(debug = True,
                    port = 8050,
                    host = 'localhost',
                   )








