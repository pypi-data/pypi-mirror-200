import datetime
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

infoList = ["  * Bonding hybrids",
            "   * Nothing here..."]

def assembleHybridToTestPanel(df):
    pass

def bondHybrid(df):
    st.write('##### Operation steps for hybrid wirebonding')
    st.write('###### 1. ')
    st.write('###### 2. ')
    st.write('###### 3. ')
    st.write('###### 4. ')
    st.write('###### 5. ')
    st.write('###### 6. ')
    
    if st.checkbox(' Wirebonding finished. '):
        df.loc[len(df)-1,"State"] = 'HYBRID_BONDED'
    
    return df

def uploadWireBondingTest(df, client):
    st.subheader("Upload visual inspection test result")
    new_test_result = {}

    component = df.loc[len(df)-1, 'ATLAS SN']
    run_number = str(st.number_input("Enter run number",min_value= 1, step= 1)) #TODO: a more smart default value (get number of same testrun at current stage and +1)
    date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    date = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00",date.timetuple())
    bonder = st.text_input("Enter the model of wire bond machine", value="Hesse BJ820")
    properties = {
        "OPERATOR": st.session_state['Hybrid Wirebonding']['uName'],
        "BONDER": bonder
    }
    results = {
        "FAILED_ASIC_BACKEND": {},
        "TOTAL_FAILED_ASIC_BACKEND": 40,
        "REPAIRED_ASIC_BACKEND": {},
        "FAILED_HYBRID_TO_PANEL": {},
        "REPAIRED_HYBRID_TO_PANEL": {}
    }

    ##some hard coded ...
    data = {"component": component,
            "testType": "WIRE_BONDING",
            "institution": "IHEP",
            "runNumber": run_number,
            "date": date,
            "comments":[],
            "properties": properties,
            "results":{}
            }

    passed = st.checkbox("Passed", value=True)
    problems = st.checkbox("Problems during test")

    data["passed"] = passed
    data["problems"] = problems

    if not passed or problems:
        comment = st.text_area("Leave a comment about why visual inspection test is not passed / problems during test")
        data["comments"] = [comment]
    else:
        data["comments"] = []





def uploadVisualInspection(df, client):
    st.subheader("Upload visual inspection test result")
    new_test_result = {}

    test_time = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    test_time = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00",test_time.timetuple())

    run_number = str(st.number_input("Enter run number",min_value= 1, step= 1)) #TODO: a more smart default value (get number of same testrun at current stage and +1)

    data = {"component": df.loc[len(df)-1,"ATLAS SN"], 
            "testType": "VISUAL_INSPECTION",
            "institution" : "IHEP",
            "runNumber": run_number,
            "date" : test_time,
            "comments": [],
            "results":{}
            }

    passed = st.checkbox("Passed", value=True)
    problems = st.checkbox("Problems during test")

    data["passed"] = passed
    data["problems"] = problems

    if not passed or problems:
        comment = st.text_area("Leave a comment about why visual inspection test is not passed / problems during test")
        data["comments"] = [comment]                                        
    
    st.write("###### TestRun results")
    st.write(data)
    # Upload test result
    if st.button("Upload!"):
        with st.spinner("Uploading..."):
            new_test_result = client.post('uploadTestRunResults', json=data)
            time.sleep(1)

    return new_test_result

def hybridBondingFlow(filepath, client, rework=False):
    hybrid_df = pd.read_pickle(filepath)

    if hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] != 'WIRE-BONDING' or rework:
        
        hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'MEASURED'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] = 'WIRE-BONDING'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operator"] = st.session_state['Hybrid Wirebonding']['uName']
        hybrid_df.loc[len(hybrid_df)-1,"State"] = 'WIRE-BONDING_NOT_STARTED_YET'

        hybrid_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
        # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'WIRE-BONDING_NOT_STARTED_YET':      ### TODO: Add timestamp for each step and change the way of data recording
            st.header('Bond hybrid')
            hybrid_df = bondHybrid(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'HYBRID_BONDED':
            st.header('Hybrid Wire-bonding Done Confirmation')
            if st.button('❗️ CONFIRM: hybrid wire-bonding done!'):
                hybrid_df.loc[len(hybrid_df)-1,"State"] = 'WIRE-BONDING_DONE'
                hybrid_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'WIRE-BONDING_DONE':
            hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'BONDED'
            success_str = '#### ' + hybrid_df.loc[len(hybrid_df)-1,'Local Name'] + ' --- Hybrid Wire-bonding Done! 🎉🎉🎉🎉🎉🎉'
            st.success(success_str)
            hybrid_df.to_pickle(filepath)

    return hybrid_df
#####################
### main part
#####################

class Page3(Page):
    def __init__(self):
        super().__init__("Hybrid Wirebonding", ":link: Hybrid Wirebonding", infoList)

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
        hybrid_wire_u_df = df_havNextOp[df_havNextOp['Local Name'].str.contains('-Hybrid-') & (df_havNextOp['Next Operation'] == 'WIRE-BONDING') & (df_havNextOp['Next Operator'] == pageDict['uName'])]

        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        rework = False

        if not hybrid_wire_u_df.empty :
            task_selector = st.empty()
            with task_selector.container():
                hybrid_local_name = st.selectbox('Please select the hybrid you want to work on', selectbox_init_v_tpl + tuple(hybrid_wire_u_df['Local Name'].tolist()))

            if hybrid_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                hybrid_wire_u_df.set_index('Local Name', inplace=True)
                hybrid_sub_table_file_path = hybrid_wire_u_df.loc[hybrid_local_name,'Sub-table Path']
                hybrid_local_alias = hybrid_wire_u_df.loc[hybrid_local_name,'Local Alias']
                
                st.info('###### Now working on: '+hybrid_local_name + ' (' + hybrid_local_alias + ') ')
                pageDict['result_dir'] = os.path.join( os.path.dirname(hybrid_sub_table_file_path), 'wirebonding_results')  
                tools.mkdirs(pageDict['result_dir'])

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start current task from scratch) ❗️')

                df_this_hybrid = hybridBondingFlow(hybrid_sub_table_file_path, client, rework)

                if df_this_hybrid['Current Local Stage'].tolist()[-1] == 'BONDED':
                    this_hybrid_idx = inv_df['Local Name'].tolist().index(hybrid_local_name) 
                    inv_df.loc[this_hybrid_idx,'Current Local Stage'] = 'BONDED'
                    inv_df.loc[this_hybrid_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_hybrid_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operation DDL'] = np.nan
                    inv_df.to_pickle(inventory)

                st.write('---')
                st.write('#### Current Hybrid Info:')
                st.dataframe(df_this_hybrid) 
