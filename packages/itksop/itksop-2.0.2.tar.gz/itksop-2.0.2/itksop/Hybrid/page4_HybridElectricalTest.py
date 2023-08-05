import datetime
import os 
import time 
import base64
import argparse

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from core.Page import Page
import core.tools as tools


#####################
### useful functions
#####################

infoList = ["  * Test the electronic performance of the hybrids...",
            "   * Nothing here..."]

#####################
### main part
#####################
def etestHybrid(df):
    ### directly write steps here or call functions. Both are OK.
    st.write('##### Operation steps for hybrid electrical test')
    st.write('###### 1. ')
    st.write('###### 2. ')
    st.write('###### 3. ')
    st.write('###### 4. ')
    st.write('###### 5. ')
    st.write('###### 6. ')

    if st.checkbox(' E-TEST finished. '):
        df.loc[len(df)-1,"State"] = 'HYBRID_E-TESTED'
    
    return df

def hybridETestFlow(filepath, client, rework=False):

    hybrid_df = pd.read_pickle(filepath)

    if hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] != 'E-TEST' or rework:
        
        hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'BONDED'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] = 'E-TEST'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operator"] = st.session_state['Hybrid Electrical Test']['uName']
        hybrid_df.loc[len(hybrid_df)-1,"State"] = 'E-TEST_NOT_STARTED_YET'

        hybrid_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
        # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'E-TEST_NOT_STARTED_YET':      ### TODO: Add timestamp for each step and change the way of data recording
            st.header('Introduction and setup for hybrid test')
            hybrid_df = etestHybrid(hybrid_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'HYBRID_E-TESTED':
            st.header('Hybrid Electrical Test Done Confirmation')
            if st.button('❗️ CONFIRM: hybrid electrical test done!'):
                hybrid_df.loc[len(hybrid_df)-1,"State"] = 'E-TEST_DONE'
                hybrid_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'E-TEST_DONE':
            hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'E-TESTED'
            success_str = '#### ' + hybrid_df.loc[len(hybrid_df)-1,'Local Name'] + ' --- Hybrid Electrical Test Done! 🎉🎉🎉🎉🎉🎉'
            st.success(success_str)
            hybrid_df.to_pickle(filepath)

    return hybrid_df
#####################
### main part
#####################

class Page4(Page):
    def __init__(self):
        super().__init__("Hybrid Electrical Test", ":electric_plug: Hybrid Electrical Test", infoList)

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
        hybrid_etest_u_df = df_havNextOp[df_havNextOp['Local Name'].str.contains('-Hybrid-') & (df_havNextOp['Next Operation'] == 'E-TEST') & (df_havNextOp['Next Operator'] == pageDict['uName'])]
        
        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        rework = False
        
        if not hybrid_etest_u_df.empty :
            task_selector = st.empty()
            with task_selector.container():
                hybrid_local_name = st.selectbox('Please select the hybrid you want to work on', selectbox_init_v_tpl + tuple(hybrid_etest_u_df['Local Name'].tolist()))

            if hybrid_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                hybrid_etest_u_df.set_index('Local Name', inplace=True)
                hybrid_sub_table_file_path = hybrid_etest_u_df.loc[hybrid_local_name,'Sub-table Path']
                hybrid_local_alias = hybrid_etest_u_df.loc[hybrid_local_name,'Local Alias']
                    
                st.info('###### Now working on: '+hybrid_local_name + ' (' + hybrid_local_alias + ') ')
                pageDict['result_dir'] = os.path.join(os.path.dirname(hybrid_sub_table_file_path), 'etest_results')  
                tools.mkdirs(pageDict['result_dir'])

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start current task from scratch) ❗️')
                    
                df_this_hybrid = hybridETestFlow(hybrid_sub_table_file_path, client, rework)

                if df_this_hybrid['Current Local Stage'].tolist()[-1] == 'E-TESTED':
                    this_hybrid_idx = inv_df['Local Name'].tolist().index(hybrid_local_name) 
                    inv_df.loc[this_hybrid_idx,'Current Local Stage'] = 'E-TESTED'
                    inv_df.loc[this_hybrid_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_hybrid_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operation DDL'] = np.nan
                    inv_df.to_pickle(inventory)

                st.write('---')
                st.write('#### Current Hybrid Info:')
                st.dataframe(df_this_hybrid) 
            
        
                
        
        