# Code source: https://dash-bootstrap-components.opensource.faculty.ai/examples/simple-sidebar/
import os
import glob
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

# Some important definitions --------------------------------------------------
dir_input_fields = os.path.join('assets', 'img', 'input_fields')
dir_img_clusters = os.path.join('assets', 'img', 'clusters')
fnames_input_fields = ["TEMP_MED.jpg", "PREC_MED.jpg", "NDVI_MED.jpg", "RH_MED.jpg", "TOPO.jpg", "VEG.jpg"]
var_input_fields = [x.split("_")[0].split('.')[0] for x in fnames_input_fields]
var_input_aux = ["LON", "LAT"]
var_input_all = var_input_aux + var_input_fields
dic_options = [{"label": "Yes", "value": True}, {"label": "No", "value": False}]
dic_options2 = [{"label": 4, "value": 4}, {"label": 5, "value": 5}]
sty_fields = {'max-height':'100%', 'max-width':'100%', 'margin':'auto'}
sty_radio = {'text-align':'center', 'padding':'0px', 'border':'1px solid'}
sty_radio2 = {'text-align':'center', 'border':'1px solid', 'display':'inline-block'}

sty_col_fields = {'border':'0.5px solid', 'padding':'0px', 'margin':'0px'}

# Captura todos os nomes dos arquivos (clusteres em jpg)
fnames_all = sorted(glob.glob(f"{dir_img_clusters}/[G|K]*.jpg"))

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflowY": "scroll"
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "overflowY": "auto"
}

# Building the table to choose which field/var to show

tab_rows = []
for i, var in enumerate(var_input_all):
   tab_rows += [html.Tr([html.Td(var, style={'padding':'0px', 'width':'25%'}), 
                dbc.RadioItems(id=f"show_{var}", options=dic_options, value=True, inline=True, style=sty_radio)])]
table_body = [html.Tbody(tab_rows)]
table = dbc.Table(table_body, bordered=True)

sidebar = html.Div([
        html.H2("SAZones", className="display-4", style={'background-image':'-webkit-gradient(linear, left top, left bottom, from(lightgreen), to(blue))', 'color':'white', "text-align":'center', 'padding':'1px', 'margin':'1px'}),
        html.Div(id='qtd_files', style={'padding-bottom':'20px'}),
        table,
        html.P(),
        html.Div(id="input_fields", children={})
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    dbc.Row(id="results", children={}, style=CONTENT_STYLE)
)

app.layout = html.Div([
    dcc.Location(id="url"),  # hidden
    sidebar,
    content
])
@app.callback([Output(component_id="results", component_property="children"),
              Output(component_id="qtd_files", component_property="children"),
              Output(component_id="input_fields", component_property="children")],
              [Input(component_id='show_LON', component_property='value'),
                Input(component_id='show_LAT', component_property='value'),
                Input(component_id='show_TEMP', component_property='value'),
                Input(component_id='show_PREC', component_property='value'),
                Input(component_id='show_NDVI', component_property='value'),
                Input(component_id='show_RH', component_property='value'),
                Input(component_id='show_TOPO', component_property='value'),
                Input(component_id='show_VEG', component_property='value')])

def update_fields(show_lon, show_lat, show_fld_00, show_fld_01, show_fld_02, show_fld_03, show_fld_04, show_fld_05):
    '''
    show_fld_00=show_fld_01=show_fld_02=True
    show_lon=show_lat=show_fld_03=show_fld_04=show_fld_05=False
    '''
    
    input_show = [show_lon, show_lat, show_fld_00, show_fld_01, show_fld_02, show_fld_03, show_fld_04, show_fld_05]
    
    opts = np.array((["LON", "LAT"] + var_input_fields))
    #variablesYes = list(opts[input_show])
    variablesNo = list(opts[np.logical_not(input_show)])
   
    # Retira os aqruivos que não devem ser mostrados
    fnames = [fname for fname in fnames_all if not any(var in fname for var in variablesNo)]
    #print(fnames)

    # Separa os arquivos entre os métodos e qtd de clusteres
    keys=["KMeans", "4"]
    list1 = [fname for fname in fnames if all(item in fname for item in keys)]

    keys=["GaussianMixture", "4"]
    list2 = [fname for fname in fnames if all(item in fname for item in keys)]

    keys=["KMeans", "5"]
    list3 = [fname for fname in fnames if all(item in fname for item in keys)]

    keys=["GaussianMixture", "5"]
    list4 = [fname for fname in fnames if all(item in fname for item in keys)]
    
    #print("Var yes:", variablesYes, "\nVar no.:", variablesNo)
    imgs1=[]; imgs2=[]; imgs3=[]; imgs4=[]
    
    for i in range(len(list1)):
        imgs1.append(html.Img(src=f"{list1[i]}", style = {'width': '100%', 'padding':'0px', 'margin':'0px'}))
        imgs2.append(html.Img(src=f"{list2[i]}", style = {'width': '100%', 'padding':'0px', 'margin':'0px'}))
        imgs3.append(html.Img(src=f"{list3[i]}", style = {'width': '100%', 'padding':'0px', 'margin':'0px'}))
        imgs4.append(html.Img(src=f"{list4[i]}", style = {'width': '100%', 'padding':'0px', 'margin':'0px'}))
    
    Div1 = html.Div([i for i in imgs1], style=sty_fields)
    Div2 = html.Div([i for i in imgs2], style=sty_fields)
    Div3 = html.Div([i for i in imgs3], style=sty_fields)
    Div4 = html.Div([i for i in imgs4], style=sty_fields)
    
    row = [dbc.Col(Div1, style=sty_col_fields),
            dbc.Col(Div2, style=sty_col_fields),
            dbc.Col(Div3, style=sty_col_fields),
            dbc.Col(Div4, style=sty_col_fields)]
    
    # Rearrange the fields to show: 1st the "yes", then the "no"
    fnames_yes = np.array(fnames_input_fields)[input_show[2:]].tolist()
    fnames_no  = list(set(fnames_input_fields)-(set(fnames_yes)))
    input_fields = []
    for i, fname in enumerate(fnames_yes):
        input_fields += [html.Img(src=os.path.join(dir_input_fields, fname), style=sty_fields)]
    for i, fname in enumerate(fnames_no):
        input_fields += [html.Img(src=os.path.join(dir_input_fields, fname), style=sty_fields)]
    
    return(row, 
           html.Label(f"Num arqs: {len(fnames)}, {int(len(fnames)/4)} por col", style={'color':'darkblue', 'background-color':'gold', 'text-align':'center'}),
           input_fields)

if __name__=='__main__':
    app.run_server(debug=True, port=3000)

    
# https://youtu.be/ln8dyS2y4Nc