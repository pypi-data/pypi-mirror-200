import argparse
import base64
import datetime
import json
import mimetypes as mt
import os 
from PIL import Image
import time 

import numpy as np
import pandas as pd
import streamlit as st

from core.Page import Page
import core.tools as tools
# from utils.HybridMetrology.Gen_CDF import Gen_CDF_PPA, Gen_CDF_PPB
# from utils.HybridMetrology.process_data import process_data
# from utils.HybridMetrology.metrologyanalysis import analysis

#####################
### useful functions
#####################

infoList = ["  * Measure Modules",
            "   * Nothing here..."]

def measureModule(df):
    st.write('##### Operation steps for hybrid measurement')
    st.write('###### 1. Check the switch on the right side of the Smartscope, the power switch on the joystick.')
    st.write('###### 2. Open the portal. Program self-check. Click professional, open measuremind. Attention, in the self-check the lens can suddenly go down, keep a cerntain distance.')
    st.write('###### 3. ')
    st.write('###### 4. ')
    st.write('###### 5. ')
    st.write('----- Exception handling: if error occurs or the centroid finding do not find the correct object(cross mark or the shining pad), re-run the step.')
    st.write('###### 6. File-Save the output file. Use an external storage to save the file.')
    
    if st.checkbox(' Measurement finished. '):
        df.loc[len(df)-1,"State"] = 'MODULE_MEASURED'
    
    return df

def operation2():
    pass

def operation3():
    pass

def moduleMetrologyFlow(filepath, client, rework=False):

    module_df = pd.read_pickle(filepath)

    if module_df.loc[len(module_df)-1,"Current Operation"] != 'METROLOGY' or rework:
        
        module_df.loc[len(module_df)-1,"Current Local Stage"] = 'GLUED'
        module_df.loc[len(module_df)-1,"Current Operation"] = 'METROLOGY'
        module_df.loc[len(module_df)-1,"Current Operator"] = st.session_state['Module Metrology']['uName']
        module_df.loc[len(module_df)-1,"State"] = 'METROLOGY_NOT_STARTED_YET'

        module_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
        # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'METROLOGY_NOT_STARTED_YET':      ### TODO: Add timestamp for each step and change the way of data recording
            st.header('Measure module')
            module_df = measureModule(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()

        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'MODULE_MEASURED':
            st.header('Module Metrology Done Confirmation')
            if st.button('❗️ CONFIRM: module metrology done!'):
                module_df.loc[len(module_df)-1,"State"] = 'METROLOGY_DONE'
                module_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'METROLOGY_DONE':
            module_df.loc[len(module_df)-1,"Current Local Stage"] = 'MEASURED'
            success_str = '#### ' + module_df.loc[len(module_df)-1,'Local Name'] + ' --- Module Metrology Done! :tada::tada::tada::tada::tada::tada:'
            st.success(success_str)
            module_df.to_pickle(filepath)

        return module_df

#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Module Metrology", ":straight_ruler: Module Metrology", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### check requirements to do stuff
        doWork=False
        if not st.session_state.dummy:
            try:
                if st.session_state.myClient:
                    doWork=True
                if st.session_state.debug:
                    st.write(":white_check_mark: Got Token")
            except AttributeError:
                st.warning("No token, please authenticate first on page \" Overview-Homepage \" ")
        else:
            try:
                if st.session_state.Homepage['user'] != '':
                    doWork=True
                else: 
                    st.warning("No user name, please select your name first on page \" Overview-Homepage \" ")
            except KeyError:
                st.warning("No user name, please select your name first on page \" Overview-Homepage \" ")
            except AttributeError:
                st.warning("No user name, please select your name first on page \" Overview-Homepage \" ")

        ### gatekeeping
        if not doWork:
            st.stop()

        
        ### 
        ### get total inventory file
        inventory = os.path.join(tools.DATA_PATH, 'inventory.pkl')
        inv_df = tools.get_inventory(inventory)

        if not st.session_state.dummy:
            client = st.session_state.myClient
            pageDict['uName'] = tools.uid_to_uname(st.session_state.Homepage['user']['userIdentity']) # get uid from Homepage and convert to uname using local mapping
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) ]
        else:
            client='DUMMY'
            pageDict['uName'] = st.session_state.Homepage['user']
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) & (inv_df['Local Type'].str.contains("DUMMY"))]
            
        ### get sub_dataframe which contains entries that belong to this page and logged in user (to enable access control)
        module_mea_u_df = df_havNextOp[df_havNextOp['Local Name'].str.contains('-Module-') & (df_havNextOp['Next Operation'] == 'METROLOGY') & (df_havNextOp['Next Operator'] == pageDict['uName'])]
        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        rework = False

        if not module_mea_u_df.empty :
            # st.info('###### Hi '+pageDict['uName'].split(' ')[0]+', welcome to work!')
            task_selector = st.empty()
            with task_selector.container():
                module_local_name = st.selectbox('Please select the module you want to work on', selectbox_init_v_tpl + tuple(module_mea_u_df['Local Name'].tolist()))

            if module_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                module_mea_u_df.set_index('Local Name', inplace=True)
                module_sub_table_file_path = module_mea_u_df.loc[module_local_name,'Sub-table Path']
                module_local_alias = module_mea_u_df.loc[module_local_name,'Local Alias']
                module_atlas_sn = module_mea_u_df.loc[module_local_name,'ATLAS SN']
                    
                st.info('###### Now working on: '+module_local_name + ' (' + module_atlas_sn +', '+ module_local_alias + ') ')
                pageDict['result_dir'] = os.path.join(os.path.dirname(module_sub_table_file_path), 'metrology_results')  
                tools.mkdirs(pageDict['result_dir'])

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start current task from scratch) ❗️')

                df_this_module = moduleMetrologyFlow(module_sub_table_file_path, client, rework)

                if df_this_module['Current Local Stage'].tolist()[-1] == 'MEASURED':
                    this_module_idx = inv_df['Local Name'].tolist().index(module_local_name) 
                    inv_df.loc[this_module_idx,'Current Local Stage'] = 'MEASURED'
                    inv_df.loc[this_module_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_module_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_module_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_module_idx,'Next Operation DDL'] = np.nan
                    inv_df.to_pickle(inventory)

                st.write('---')
                st.write('#### Current module Info:')
                st.dataframe(df_this_module) 
