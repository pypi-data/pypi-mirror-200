# Initialize with the ITk Database 
import itkdb
import pandas as pd
import numpy as np
import sys 
import os 
import maskpass 
import datetime 
import copy 
import streamlit as st 
import plotly.graph_objs as go
import logging 
import core.tools as tools

logger = logging.getLogger() 
logger.setLevel(logging.WARNING)
# logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)


# Global variables 
MODULE_CLUSTERS = {'UKCHINA':   ['IHEP', 'RAL', 'LIV', 'GL', 'BHM', 'SHF', 'CAM', 'QMUL'], 
                   'US':        ['BNL', 'UCSC', 'LBNL_STRIP_MODULES'],  
                   'FREIBURG':  ['ADELAIDE', 'TUDO', 'UNIFREIBURG', 'MELB'], 
                   'VALENCIA':  ['CUNI', 'ARGOTECH', 'UIO', 'LUND', 'UPPSALA', 'NOTE', 'IFIC', 'NBI'], 
                   'VANCOUVER': ['TRIUMF', 'SFU', 'UBC', 'UT', 'CEL', 'MONTREAL'],
                   'DESY':      ['DESYHH', 'DESYZ', 'HUBERLIN']}

MODULE_SITES_BARREL = MODULE_CLUSTERS['UKCHINA'] + MODULE_CLUSTERS['US'] 

MODULE_SITES_ENDCAP = MODULE_CLUSTERS['FREIBURG'] +  MODULE_CLUSTERS['VALENCIA'] + \
                      MODULE_CLUSTERS['VANCOUVER'] + MODULE_CLUSTERS['DESY']  

MODULE_SITES = MODULE_SITES_BARREL + MODULE_SITES_ENDCAP  


HYBRID_CLUSTERS = {'UKCHINA':   ['IHEP', 'RAL', 'LIV', 'BHM'], 
                   'US':        ['BNL', 'UCSC', 'LBNL_STRIP_MODULES'],  
                   'FREIBURG':  ['UNIFREIBURG'], 
                   'VALENCIA':  ['UPPSALA'], 
                   'VANCOUVER': ['UT'],
                   'DESY':      ['HUBERLIN']} 

HYBRID_SITES_BARREL = HYBRID_CLUSTERS['UKCHINA'] + HYBRID_CLUSTERS['US'] 

HYBRID_SITES_ENDCAP = HYBRID_CLUSTERS['FREIBURG'] +  HYBRID_CLUSTERS['VALENCIA'] + \
                      HYBRID_CLUSTERS['VANCOUVER'] + HYBRID_CLUSTERS['DESY']  

HYBRID_SITES = HYBRID_SITES_BARREL + HYBRID_SITES_ENDCAP


HYBRID_FLEX_STAGES = ['FROM_MANUFACURER', 'READY_FOR_SMD_ATTACHMENT', 'SMD_ATTACHMENT',
                      'SMD_POPULATED','SMD_COMPLETED','AT_HYBRID_ASSEMBLY_SITE', 'ON_HYBRID' ] 

HYBRID_FLEX_TYPES = [ 'X', 'Y', 'R0H0', 'R0H1', 'R1H0', 'R1H1', 'R2H0', 'R3H0', 'R3H1', 'R3H2',
                    'R3H3', 'R4H0', 'R5H0', 'R5H1'] 

HYBRID_ASSEMBLY_STAGES = ['ASIC_ATTACHMENT', 'WIRE_BONDING', 'BURN_IN', 'FINISHED_HYBRID', 'ON_MODULE']  

HYBRID_ASSEMBLY_TYPES = [ 'X', 'Y', 'R0H0', 'R0H1', 'R1H0', 'R1H1', 'R2H0', 'R3H0', 'R3H1', 'R3H2',
                          'R3H3', 'R4H0', 'R5H0', 'R5H1']
                          
MODULE_ASSEMBLY_STAGES = ['HV_TAB_ATTACHED', 'GLUED', 'BONDED', 'TESTED', 'FINISHED']  

MODULE_ASSEMBLY_TYPES = ['BARREL_SS_MODULE', 'BARREL_LS_MODULE', 'R1', 'R2', 'R3', 'R4', 'R5', 
                         'R3M0', 'R3M1', 'R4M0', 'R4M1', 'R5M0', 'R5M1'] 

MODULE_ASSEMBLY_TYPES_SHORT = ['SS', 'LS', 'R1', 'R2', 'R3','R4','R5']  

DATA_PATH = tools.DATA_PATH 

# Functions

@st.cache_data 
def get_access_codes(): 
    access_code1 = maskpass.askpass(prompt='Input access_code1: ') 
    access_code2 = maskpass.askpass(prompt='Input access_code2: ') 
    return access_code1, access_code2 
    

def get_client(): 
    access_code1, access_code2 = get_access_codes()   
    user = itkdb.core.User(access_code1=access_code1, access_code2=access_code2)
    user.authenticate()
    client = itkdb.Client(user=user)
    return client 

def get_complist(myClient, site): 
    compList = myClient.get('listComponents', json={'project': 'S', 'institution': site, 'pageInfo': {'pageSize': 4000}})
    return pd.DataFrame(compList.data)  

@st.cache_data 
def get_sites_data(sites): 
    df_sites = []
    client = get_client()
    for site in sites: 
        df_sites.append(get_complist(client, site))
    return pd.concat(df_sites) 

def check_outfile(dst): 
    check_outfile_path(dst) 
    if os.access(dst, os.F_OK) :
        key = input('%s already exist, still want to proceed? [N/yes]' %dst )
        if key != 'yes': 
            return False 
    return True 
 

def check_outfile_path(outfile):
    path, tail = os.path.split(outfile)
    if path != '' and not os.access(path, os.F_OK) :
        sys.stdout.write('Creating dir %s ...\n'  % path)
        os.makedirs(path)


def check_and_join(filepath, filename):
    if not os.access(filepath, os.F_OK):
        sys.stdout.write('creating dir %s ...' % filepath)
        os.makedirs(filepath)
        sys.stdout.write(' OK.\n')
    file_ = os.path.join(filepath, filename)
    return file_

def save_pdb_data(df, dst): 
    check_outfile_path(dst) 
    if os.access(dst, os.F_OK) :
        key = input('%s already exist, do you want to replace? [N/yes]' %dst )
        if key != 'yes': 
            return 
    df.to_pickle(dst) 
    sys.stdout.write('Saved as: %s\n' %dst)


def read_pdb_data(sites=MODULE_SITES): 
    df_sites = [] 
    filename = 'pdb_{0}.pkl' 
    for site in sites: 
        src = os.path.join(DATA_PATH, filename.format(site))
        logging.info('Reading from {0}...'.format(src)) 
        df = pd.read_pickle(src) 
        df_sites.append(df) 
    return pd.concat(df_sites) 


def in_stage(row, stage):
    row_stages = getattr(row, 'stages') 
    if not hasattr(row_stages, '__iter__'): 
        return False 
    for rs in row_stages: 
        row_stage = rs['code'] 
        if row_stage == stage: 
            return True 
    # row_stage = getattr(row, 'currentStage')['code'] 
    # if row_stage == stage: 
    #     return True 

    return False 

def in_site(row, site):
    row_site = getattr(row, 'institution')['code']
    if isinstance(site, str): 
        if row_site == site: 
            return True 
    elif isinstance(site, list): 
        if row_site in site: 
            return True
    else:
        raise NameError(site) 
    return False 

def is_component(row, component):
    row_component = getattr(row, 'componentType')['code'] 
    info_msg = 'component = {0}, row_component = {1}'.format(component, row_component) 
    if row_component == component: 
        return True 
    else:
        logging.debug(info_msg) 
        return False

def is_type(row, typ):
    row_type = getattr(row, 'type')['code'] 
    if row_type == typ: 
        return True 
    else:
        return False

def in_past_days(row, d): 
    state_time  = getattr(row, 'stateTs')
    state_date = state_time.split('T')[0]
    state_date = datetime.date.fromisoformat(state_date)
    today = datetime.date.today()
    time_passed = today - state_date
    return time_passed < datetime.timedelta(days=d)  


def get_yield(df, component, stage, typ, day=9999, site='all'): 
    yld = 0 
    n_tot = 0 
    n_component = 0 
    n_type = 0 
    n_stage = 0 
    n_day = 0 
    n_site = 0 
    for row in df.itertuples(): 
        n_tot += 1 
        if not is_component(row, component): 
            continue 
        n_component +=1 
        if not is_type(row, typ):
            continue 
        n_type += 1 
        if not in_stage(row, stage): 
            continue 
        n_stage += 1 
        if (day != 9999) and (not in_past_days(row, day)):
            continue 
        n_day += 1 
        if (site != 'all') and (not in_site(row, site)):
            continue 
        n_site += 1 
        yld += 1
 
    info_msg = 'n_tot = {0}, n_component = {1}, n_type = {2}, n_stage = {3}, n_day = {4}, n_site = {5}'
    info_msg = info_msg.format(n_tot, n_component, n_type, n_stage, n_day, n_site)      
    logging.info(info_msg) 

    return yld  


def get_stages_types_yield(df, component, stages, types, sites='all'): 
    data = {'Stage': stages}
    yields = [] 
    for n in range(len(stages)):
        yields.append(0)

    for type in types: 
        for stage in stages: 
            stage_index = stages.index(stage)
            yields[stage_index] = get_yield(df, component, stage, type, site=sites)
        if type == 'BARREL_SS_MODULE': 
            label = 'SS'
        elif type == 'BARREL_LS_MODULE': 
            label = 'LS'
        else:
            label = type 
        data[label] = copy.deepcopy(yields) 
    return pd.DataFrame(data)


def get_hybrid_flex_stages_yield(df): 
    component = 'HYBRID_FLEX'
    stages = HYBRID_FLEX_STAGES  
    types = HYBRID_FLEX_TYPES
    return get_stages_types_yield(df, component, stages, types) 


def get_hybrid_assembly_stages_yield(df): 
    component = 'HYBRID_ASSEMBLY'
    stages = HYBRID_ASSEMBLY_STAGES  
    types = HYBRID_ASSEMBLY_TYPES
    sites = HYBRID_SITES    
    return get_stages_types_yield(df, component, stages, types, sites=sites) 


def get_module_assembly_stages_yield(df): 
    component = 'MODULE'
    stages = MODULE_ASSEMBLY_STAGES  
    types = MODULE_ASSEMBLY_TYPES
    sites = MODULE_SITES 
    return get_stages_types_yield(df, component, stages, types, sites=sites) 

   
def cal_stage_eff(df):
    df_eff = df.copy() 
    df_num = df_eff.iloc[:,1:]
    df_den = df_num.shift()
    eff = df_num/df_den 
    df_eff.iloc[:,1:] = eff.round(2) 
    return df_eff 


def get_days_types_yield(df, component, stage, types, days, sites): 
    data = {'Days': days}  
    yields = [] 
    for n in range(len(days)):
        yields.append(0)
    for type in types: 
        for day in days:
            day_index = days.index(day)
            yields[day_index] = get_yield(df, component, stage, type, day=day, site=sites) 
        if type == 'BARREL_SS_MODULE': 
            label = 'SS'
        elif type == 'BARREL_LS_MODULE': 
            label = 'LS'
        else:
            label = type 
        data[label] = copy.deepcopy(yields) 
    return pd.DataFrame(data) 


def get_hybrid_assembly_days_yield(df): 
    component = 'HYBRID_ASSEMBLY'
    stage = 'FINISHED_HYBRID'   
    types = HYBRID_ASSEMBLY_TYPES
    sites = HYBRID_SITES 
    days = [30, 90, 9999]
    return get_days_types_yield(df, component, stage, types, days, sites)  


def get_module_assembly_days_yield(df): 
    component = 'MODULE'
    stage = 'FINISHED' 
    types = MODULE_ASSEMBLY_TYPES
    sites = MODULE_SITES
    days = [30, 90, 9999]
    return get_days_types_yield(df, component, stage, types, days, sites)  


def draw_hybrid_assembly_days_yield(df):  
    ax = df.plot(kind='bar', x='Days')
    ax.set_title("Hybrid Assembly") 
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    ax.plot()


def draw_module_assembly_days_yield(df):  
    ax = df.plot(kind='bar', x='Days')
    ax.set_title("Module Assembly") 
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    ax.plot()


def get_sites_types_yield(df, component, stage, types, sites):
    data = {'Sites': sites}  
    yields = [] 
    for n in range(len(sites)):
        yields.append(0)
    for type in types: 
        for site in sites:
            site_index = sites.index(site) 
            yields[site_index] = get_yield(df, component, stage, type, site=site)  
        if type == 'BARREL_SS_MODULE': 
            label = 'SS'
        elif type == 'BARREL_LS_MODULE': 
            label = 'LS'
        else:
            label = type 
        data[label] = copy.deepcopy(yields) 
    return pd.DataFrame(data) 


def get_hybrid_assembly_sites_yield(df, sites=None): 
    component = 'HYBRID_ASSEMBLY'
    stage = 'FINISHED_HYBRID' 
    types = HYBRID_ASSEMBLY_TYPES
    if sites is None: 
        sites = HYBRID_SITES
    return get_sites_types_yield(df, component, stage, types, sites)   


def get_module_assembly_sites_yield(df, sites=MODULE_SITES): 
    component = 'MODULE'
    stage = 'FINISHED' 
    types = MODULE_ASSEMBLY_TYPES
    return get_sites_types_yield(df, component, stage, types, sites)   


def draw_hybrid_assembly_sites_yield(df):
    ax = df.plot(kind='bar', x='Sites') 
    ax.set_title("Hybrid Assembly") 
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    ax.plot()


def draw_module_assembly_sites_yield(df):
    ax = df.plot(kind='bar', x='Sites') 
    ax.set_title("Module Assembly") 
    ax.legend(bbox_to_anchor=(1.0, 1.0))
    ax.plot()


def get_serial_number(df, component): 
    sn = []  
    for row in df.itertuples(): 
        if not is_component(row, component): 
            continue 
        serial_number = getattr(row, 'serialNumber')
        sn.append(serial_number)
    return sn 

def get_child_name_sn(child):
    name = None 
    sn = None 

    type = child['type'] 
    if type != None: 
        name = type['name'] 

    sn =  child['component']
    if sn != None: 
        sn = sn['serialNumber']
    return name, sn  


def get_number_of_children(sn, client):
    children = client.get('getComponent', json={"component":sn})['children']
    
    n_all = 0 
    n_valid = 0 

    for child in children: 
        name, sn = get_child_name_sn(child) 
        n_all = n_all + 1 
        if sn != None: 
            n_valid = n_valid + 1  
    return n_all, n_valid    

@st.cache_data 
def get_hybrid_assembly_components(df, client): 
    component = 'HYBRID_ASSEMBLY'
    sns = get_serial_number(df, component)
    data = {}
    sn_list = []
    n_all_list = []
    n_valid_list = []

    n = 0 
    
    for sn in sns: 
        n = n + 1 
        if n > 20: 
            break  

        sn_list.append(sn) 
        n_all, n_valid = get_number_of_children(sn, client)
        n_all_list.append(n_all)
        n_valid_list.append(n_valid) 
    
    data['SN'] = copy.deepcopy(sn_list) 
    data['Number of Children'] = copy.deepcopy(n_all_list)
    data['Number of valid '] = copy.deepcopy(n_valid_list)   
    return pd.DataFrame(data)
    
@st.cache_data
def get_module_assembly_components(df, client): 
    component = 'MODULE'
    sns = get_serial_number(df, component)
    data = {}
    sn_list = []
    n_all_list = []
    n_valid_list = []

    n = 0 
    
    for sn in sns: 
        n = n + 1 
        if n > 20: 
            break  

        sn_list.append(sn) 
        n_all, n_valid = get_number_of_children(sn, client)
        n_all_list.append(n_all)
        n_valid_list.append(n_valid) 
    
    data['SN'] = copy.deepcopy(sn_list) 
    data['Number of Children'] = copy.deepcopy(n_all_list)
    data['Number of valid '] = copy.deepcopy(n_valid_list)   
    return pd.DataFrame(data)

def fill_yield_with_type(df, col, xmax):
    y = []
    for idx in range(xmax):
        y.append(df[col].values[idx])
    return y 


def plot_hybrid_assembly_days_yield(df):
    x = ['30 days', '90 days', 'all time']
    xmax = len(x)
    data = []
    for t in HYBRID_ASSEMBLY_TYPES: 
        y = fill_yield_with_type(df, t, xmax) 
        trace = go.Bar(x=x, y=y, name=t)
        data.append(trace)
    layout = go.Layout(title = 'Hybrid assembly in Days', 
                  yaxis = dict(title='Production yields'))
    fig = go.Figure(data=data, layout=layout) 
    return fig 


def plot_hybrid_assembly_sites_yield(df):
    x = df['Sites']
    xmax = len(x) 
    data = []
    for t in HYBRID_ASSEMBLY_TYPES: 
        y = fill_yield_with_type(df, t, xmax)  
        trace = go.Bar(x=x, y=y, name=t)
        data.append(trace)
    layout = go.Layout(title = 'Hybrid assembly across sites', 
                  yaxis = dict(title='Production yields'))
    fig = go.Figure(data=data, layout=layout) 
    return fig 


def plot_module_assembly_days_yield(df):
    x = ['30 days', '90 days', 'all time']
    xmax = len(x) 
    data = []
    for t in MODULE_ASSEMBLY_TYPES_SHORT: 
        y = fill_yield_with_type(df, t, xmax) 
        trace = go.Bar(x=x, y=y, name=t)
        data.append(trace)
    layout = go.Layout(title = 'Module assembly in Days', 
                  yaxis = dict(title='Production yields'))
    fig = go.Figure(data=data, layout=layout) 
    return fig 


def plot_module_assembly_sites_yield(df):
    x = df['Sites']
    xmax = len(x) 
    data = []
    for t in MODULE_ASSEMBLY_TYPES_SHORT: 
        y = fill_yield_with_type(df, t, xmax)  
        trace = go.Bar(x=x, y=y, name=t)
        data.append(trace)
    layout = go.Layout(title = 'Module assembly across sites', 
                  yaxis = dict(title='Production yields'))
    fig = go.Figure(data=data, layout=layout) 
    return fig 


def upload_inventory(src):
    uploaded_file = st.file_uploader("Choose an Excel file.")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        if df is not None: 
            df.to_pickle(src)
            return df  



