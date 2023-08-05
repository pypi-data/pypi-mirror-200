# Initialize with the ITk Database 
import pandas as pd
import streamlit as st
import sys 
import os 

### IHEP...
IHEP_USER_NAME = ('Xin Shi', 'Xiyuan Zhang', 'Shudong Wang', 'Zhan Li', 'Kaili Zhang', 'Tao Yang', 'Fabio Alves', 'Zijun Xu', 'Lei Guo', 'Yuqing Wang', 'Ye He', 'Yue Xu')
IHEP_USER_PWD = ('20230303_xs', '20230303_xz', '19491001_sw', '20230303_zl', '20230303_kz', '20230303_ty', '20230303_fa', '20230303_zx', '20230303_lg', '20230303_yw', '20230303_yh', '20230314_yx')
IHEP_ADMIN_NAME = ('Xin Shi', 'Shudong Wang', 'Zijun Xu', 'Xiyuan Zhang') 
IHEP_USER_ID = ('5780-4273-1', '3752-1075-1', '4324-6341-1', '1808-3011-1', '4548-5688-1', '6116-643-1', '2810-5129-1', '9188-484-1','2642-9979-1','4706-5607-1', '1144-4808-1')
IHEP_ADMIN_ID = ( '5780-4273-1', '3752-1075-1', '4324-6341-1','9188-484-1') 

IHEP_COMPONENT_TYPE = ('Hybrid', 'Module', 'Powerboard', 'BareModule', 'HybridFlex', 'ABCStar', 'HCCStar')
### DATA PATH
SOP_WEBPAGE_PATH = os.environ['ITK_SOP_WEBPAGE']
DATA_PATH = os.path.join(SOP_WEBPAGE_PATH, 'data') 

MODULE_DATA_PATH = os.path.join(DATA_PATH, 'module') 
HYBRID_DATA_PATH = os.path.join(DATA_PATH, 'hybrid') 
BAREMODULE_DATA_PATH = os.path.join(DATA_PATH, 'baremodule') 
HCCSTAR_DATA_PATH = os.path.join(DATA_PATH, 'hcc') 
ABCSTAR_DATA_PATH = os.path.join(DATA_PATH, 'abc') 
HYBRIDFLEX_DATA_PATH = os.path.join(DATA_PATH, 'hybridflex') 
PWB_DATA_PATH = os.path.join(DATA_PATH, 'powerboard') 
##### Hybrid realted
HYBRID_TYPES = ('X','Y')
HYBRID_VERSIONS = ('PPA','PPB','DUMMY')
HYBRID_LOCAL_STAGES = ('ASIC_ATTACHED', 'MEASURED', 'BONDED', 'E-TESTED', 'FINISHED_HYBRID', 'ON_MODULE', 'FAILED', 'SHIPPED')
HYBRID_NEXT_OPERATIONS = ('ASSEMBLY', 'METROLOGY', 'WIRE-BONDING', 'E-TEST', 'BURN-IN', 'SHIPMENT')
HYBRID_NEXT_OPERATORS = {   'ASSEMBLY': ('Zhan Li', 'Lei Guo', 'Yuqing Wang', 'Shudong Wang'),
                            'METROLOGY': ('Kaili Zhang', 'Lei Guo', 'Shudong Wang'),
                            'WIRE-BONDING': ('Xiyuan Zhang', 'Ye He'),
                            'E-TEST': ('Fabio Alves',),
                            'BURN-IN': ('Yue Xu',),
                            'SHIPMENT': ('Zhan Li', 'Tao Yang')
                        }

##### Module realted
MODULE_TYPES = ('LS','SS')
MODULE_VERSIONS = ('PPA','PPB','DUMMY')
MODULE_LOCAL_STAGES = ('GLUED', 'MEASURED', 'BONDED', 'E-TESTED', 'FINISHED_MODULE', 'FAILED', 'SHIPPED')
MODULE_NEXT_OPERATIONS = ( 'ASSEMBLY', 'METROLOGY', 'WIRE-BONDING', 'E-TEST', 'THERMAL-CYCLE', 'SHIPMENT')
MODULE_NEXT_OPERATORS = {   'ASSEMBLY': ('Shudong Wang',),
                            'METROLOGY': ('Tao Yang', 'Shudong Wang'),
                            'WIRE-BONDING': ('Xiyuan Zhang', 'Ye He'),
                            'E-TEST': ('Fabio Alves',),
                            'THERMAL-CYCLE': ('Hui Li',),
                            'SHIPMENT': ('Zhan Li', 'Tao Yang')
                        }

##### Powerboard realted
PWB_VERSIONS = ('PPA','PPB','DUMMY')
PWB_LOCAL_STAGES = ('RECEIVED', 'READY', 'ON_MODULE', 'FAILED', 'SHIPPED')
PWB_OPERATIONS = ('RECEPTION-TEST', 'SHIPMENT')

##### baremodule realted
BAREMODULE_TYPES = ('LS','SS')
BAREMODULE_VERSIONS = ('PP','DUMMY')
BAREMODULE_LOCAL_STAGES = ('RECEIVED', 'READY', 'ON_MODULE', 'FAILED', 'SHIPPED')
BAREMODULE_NEXT_OPERATIONS = ('RECEPTION-TEST', 'SHIPMENT')

##### HybridFlex realted
HYBRIDFLEX_TYPES = ('X','Y')
HYBRIDFLEX_VERSIONS = ('PPA','PPB','DUMMY')
HYBRIDFLEX_LOCAL_STAGES = ('RECEIVED', 'READY', 'ON_HYBRID', 'FAILED', 'SHIPPED')
HYBRIDFLEX_NEXT_OPERATIONS = ('RECEPTION-TEST', 'SHIPMENT')

##### ABCStar realted
ABCSTAR_VERSIONS = ('V0', 'V1','DUMMY')
ABCSTAR_LOCAL_STAGES = ('RECEIVED', 'READY', 'ON_HYBRID', 'FAILED', 'SHIPPED')
ABCSTAR_NEXT_OPERATIONS = ('RECEPTION-TEST', 'SHIPMENT')

##### HCCStar realted
HCCSTAR_VERSIONS = ('V0','V1','DUMMY')
HCCSTAR_LOCAL_STAGES = ('RECEIVED', 'READY', 'ON_HYBRID', 'FAILED', 'SHIPPED')
HCCSTAR_NEXT_OPERATIONS = ('RECEPTION-TEST', 'SHIPMENT')

# Functions
def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path, 0o755 )
        return True
    else:
        return False

def upload_inventory(src):
    uploaded_file = st.file_uploader("Choose an Excel file.")
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        if df is not None: 
            df.to_pickle(src)
            return df  

def get_inventory(src):
    if os.access(src, os.F_OK) :
        df = pd.read_pickle(src) 
    # else:   
    #     df = upload_inventory(src)
        return df 

def uid_to_uname(uid):
    if uid in IHEP_USER_ID:
        uname = IHEP_USER_NAME[IHEP_USER_ID.index(uid)]
        return uname
    else:
        return None   

def uname_to_upwd(uname):
    if uname in IHEP_USER_NAME:
        try:
            upwd = IHEP_USER_PWD[IHEP_USER_NAME.index(uname)]
            return upwd
        except IndexError:
            pass
    else:
        return None 
def comp_name_to_alias(local_name, inventory_df):
    comp_idx = inventory_df['Local Name'].tolist().index(local_name)
    local_alias = inventory_df.loc[comp_idx,'Local Alias']

    return local_alias

def comp_name_to_sn(local_name, inventory_df):
    comp_idx = inventory_df['Local Name'].tolist().index(local_name)
    atlas_sn = inventory_df.loc[comp_idx,'ATLAS SN']

    return atlas_sn

# def get_component_stage_tuple(componentType):
#     if componentType in IHEP_COMPONENT_TYPE:
#         if componentType == 'Hybrid':
#             return HYBRID_LOCAL_STAGES
#         if componentType == 'Module':
#             return MODULE_LOCAL_STAGES
#         if componentType == 'Powerboard':
#             return PWB_LOCAL_STAGES
#         if componentType == 'BareModule':
#             return BAREMODULE_LOCAL_STAGES
#         if componentType == 'HybridFlex':
#             return HYBRIDFLEX_LOCAL_STAGES
#         if componentType == 'ABCStar':
#             return ABCSTAR_LOCAL_STAGES
#         if componentType == 'HCCStar':
#             return HCCSTAR_LOCAL_STAGES 
#     else:
#         st.error('Invalid component type: ' + componentType )
#         return None


def modifyComponentStagebySN(atlas_sn, target_stage, operator, inventory_df):
    component_idx = inventory_df['ATLAS SN'].tolist().index(atlas_sn)  
    inventory_df.loc[component_idx,'Current Local Stage'] = target_stage
    inventory_df.loc[component_idx,'Current Operator'] = operator

    return inventory_df

def modifyComponentStagebyName(local_name, target_stage, operator, inventory_df):
    component_idx = inventory_df['Local Name'].tolist().index(local_name)  
    inventory_df.loc[component_idx,'Current Local Stage'] = target_stage
    inventory_df.loc[component_idx,'Current Operator'] = operator

    return inventory_df