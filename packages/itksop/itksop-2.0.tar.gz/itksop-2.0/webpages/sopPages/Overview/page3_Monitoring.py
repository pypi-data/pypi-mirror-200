import os
import time 

import numpy as np
import pandas as pd
import streamlit as st

from core.Page import Page
import core.tools as tools
#####################
### useful functions
#####################

infoList=["  * Nothing here...",
        "   * Nothing here..."]

def showHybridAssemblyResults():
    st.write('#### Assembly Results')
    pass

def showHybridMetrologyResults():
    st.write('#### Metrology Results')
    pass

def showHybridWireBondingResults():
    st.write('#### Wire Bonding Results')
    pass

def showHybridElectricalTestResults():
    st.write('#### Electrical Test Results')
    pass

def showHybridBurnInResults():
    st.write('#### Burn In Results')
    pass

def showHybridResults():
    pass

#####################
### main part
#####################

class Page3(Page):
    def __init__(self):
        super().__init__("Production Monitoring", ":video_camera: Production Monitoring", infoList)

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

        inventory = os.path.join(tools.DATA_PATH, 'inventory.pkl')
        inv_df = tools.get_inventory(inventory)
        
        comp_type = st.selectbox('Select component type', ('',)+tools.IHEP_COMPONENT_TYPE)
        if not st.session_state.dummy:
            sub_inv_df = inv_df[inv_df['Local Name'].str.contains('-'+comp_type+'-')]
        else:
            sub_inv_df = inv_df[inv_df['Local Name'].str.contains('-'+comp_type+'-') & inv_df['Local Name'].str.contains('DUMMY')]
        comp_local_name = st.selectbox('Select component:', ['']+sub_inv_df['Local Name'].tolist())
        if comp_local_name != '':
            sub_inv_df.set_index('Local Name', inplace=True)
            comp_sub_table_path = sub_inv_df.loc[comp_local_name, 'Sub-table Path']
            
            if isinstance(comp_sub_table_path,str):
                comp_sub_table = tools.get_inventory(comp_sub_table_path) 
                st.dataframe(comp_sub_table)
                # comp_local_stage = comp_sub_table.loc[len(comp_sub_table)-1, 'Current Local Stage']
                

            
        




