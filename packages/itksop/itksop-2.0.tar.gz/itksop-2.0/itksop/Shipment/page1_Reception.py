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

infoList = ["  * Shipments to receive...",
            "   * Nothing here..."]
ihep_component_receive = ('ABC', 'HCC', 'HybridFlex', 'PowerBoard', 'BareModule')

def ABCReception(inv_path):
    inv_df = tools.get_inventory(inv_path)

    atlas_sn = st.text_input('Enter the ABCStar chip\'s ATLAS SN') ###TODO: more time-saving way
    if len(atlas_sn) != 14:
        st.error("ATLAS SN should have 14 digits")
    version = st.selectbox('Select the version of the ABCStar chip', ("",)+ tools.ABCSTAR_VERSIONS)
    local_type = 'ABCStar-' + version
    local_type_count = len(inv_df[inv_df["Local Type"] == local_type])
    local_name = "IHEP-"+local_type+"-"+str(local_type_count+1)
    current_local_stage = "RECEIVED"
    current_operator = st.session_state['Reception']['uName']
    local_alias = np.nan
    sub_table_file_name = local_name+".pkl"
    sub_table_file_dir = os.path.join(tools.ABCSTAR_DATA_PATH, local_name)
    tools.mkdirs(sub_table_file_dir)
    sub_table_file_path = os.path.join(sub_table_file_dir, sub_table_file_name)
    sub_df = pd.DataFrame(  {'Local Name': [local_name], } )
    # next_operation = np.nan
    # next_operator = np.nan
    # next_operation_DDL = np.nan

    if st.button("Write current component to local database"):
        if len(atlas_sn) == 14 and version != "":
            if len(inv_df[(inv_df["Local Name"] == local_name) | (inv_df["ATLAS SN"] == atlas_sn)]) == 0:
                dic = {'Local Name': local_name, 'ATLAS SN': atlas_sn, 'Local Alias': local_alias,
                        'Local Type': local_type, 'Current Local Stage': current_local_stage, 'Current Operator': current_operator, 'Next Operation':np.nan,
                        'Next Operator':np.nan, 'Next Operation DDL':np.nan, 'Sub-table Path': sub_table_file_path}
                
                inv_df = inv_df.append(dic,ignore_index=True)   # TODO: pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here, change to pandas.DataFrame.concat
                sub_df.to_pickle(sub_table_file_path)
                inv_df.to_pickle(inv_path)                                                                
                st.info("Component has been received to the local database!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Component already exists!")
        else:
            st.error("Please fill in all the fields correctly ")

def HCCReception(inv_path):
    inv_df = tools.get_inventory(inv_path)

    atlas_sn = st.text_input('Enter the HCCStar chip\'s ATLAS SN') ###TODO: more time-saving way
    if len(atlas_sn) != 14:
        st.error("ATLAS SN should have 14 digits")
    version = st.selectbox('Select the version of the HCCStar chip', ("",)+ tools.HCCSTAR_VERSIONS)
    local_type = 'HCCStar-' + version
    local_type_count = len(inv_df[inv_df["Local Type"] == local_type])
    local_name = "IHEP-"+local_type+"-"+str(local_type_count+1)
    current_local_stage = "RECEIVED"
    current_operator = st.session_state['Reception']['uName']
    local_alias = np.nan
    sub_table_file_name = local_name+".pkl"
    sub_table_file_dir = os.path.join(tools.HCCSTAR_DATA_PATH, local_name)
    tools.mkdirs(sub_table_file_dir)
    sub_table_file_path = os.path.join(sub_table_file_dir, sub_table_file_name)
    sub_df = pd.DataFrame(  {'Local Name': [local_name], } )

    if st.button("Write current component to local database"):
        if len(atlas_sn) == 14 and version != "":
            if len(inv_df[(inv_df["Local Name"] == local_name) | (inv_df["ATLAS SN"] == atlas_sn)]) == 0:
                dic = {'Local Name': local_name, 'ATLAS SN': atlas_sn, 'Local Alias': local_alias,
                        'Local Type': local_type, 'Current Local Stage': current_local_stage, 'Current Operator': current_operator, 'Next Operation':np.nan,
                        'Next Operator':np.nan, 'Next Operation DDL':np.nan, 'Sub-table Path': sub_table_file_path}
                
                inv_df = inv_df.append(dic,ignore_index=True)   # TODO: pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here, change to pandas.DataFrame.concat
                sub_df.to_pickle(sub_table_file_path)
                inv_df.to_pickle(inv_path)                                                                
                st.info("Component has been received to the local database!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Component already exists!")
        else:
            st.error("Please fill in all the fields correctly ")

def hybridFlexReception(inv_path):
    inv_df = tools.get_inventory(inv_path)

    atlas_sn = st.text_input('Enter the hybrid flex\'s ATLAS SN') ###TODO: more time-saving way
    if len(atlas_sn) != 14:
        st.error("ATLAS SN should have 14 digits")
    local_alias = st.text_input('Enter the hybrid flex\'s local alias (alternative identifier)', help='It\'s printed on the surface of PCB, should be in a form like \'GPC2104_X_002_B_H5\' ')
    flex_type = st.selectbox('Select the type of the hybrid flex', ("",)+ tools.HYBRIDFLEX_TYPES)
    version = st.selectbox('Select the version of the hybrid flex', ("",)+ tools.HYBRIDFLEX_VERSIONS)
    local_type = 'HybridFlex-' + flex_type + "-" + version
    local_type_count = len(inv_df[inv_df["Local Type"] == local_type])
    local_name = "IHEP-"+local_type+"-"+str(local_type_count+1)
    current_local_stage = "RECEIVED"
    current_operator = st.session_state['Reception']['uName']
    sub_table_file_name = local_name+".pkl"
    sub_table_file_dir = os.path.join(tools.HYBRIDFLEX_DATA_PATH, local_name)
    tools.mkdirs(sub_table_file_dir)
    sub_table_file_path = os.path.join(sub_table_file_dir, sub_table_file_name)
    sub_df = pd.DataFrame(  {'Local Name': [local_name], } )   

    if st.button("Write current component to local database"):
        if len(atlas_sn) == 14 and version != "":
            if len(inv_df[(inv_df["Local Name"] == local_name) | (inv_df["ATLAS SN"] == atlas_sn) | (inv_df["Local Alias"] == local_alias)]) == 0:  
                dic = {'Local Name': local_name, 'ATLAS SN': atlas_sn, 'Local Alias': local_alias,
                        'Local Type': local_type, 'Current Local Stage': current_local_stage, 'Current Operator': current_operator, 'Next Operation':np.nan,
                        'Next Operator':np.nan, 'Next Operation DDL':np.nan, 'Sub-table Path': sub_table_file_path}
                
                inv_df = inv_df.append(dic,ignore_index=True)   # TODO: pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here, change to pandas.DataFrame.concat
                sub_df.to_pickle(sub_table_file_path)
                inv_df.to_pickle(inv_path)                                                                
                st.info("Component has been received to the local database!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Component already exists!")
        else:
            st.error("Please fill in all the fields correctly ")

def powerBoardReception(inv_path):
    inv_df = tools.get_inventory(inv_path)

    atlas_sn = st.text_input('Enter the Powerboard\'s ATLAS SN') ###TODO: more time-saving way
    if len(atlas_sn) != 14:
        st.error("ATLAS SN should have 14 digits")
    local_alias = st.text_input('Enter the Powerboard\'s local alias, It\'s printed on the surface of shield box, should be in a form like \'300-0206\' ')
    version = st.selectbox('Select the version of the Powerboard', ("",)+ tools.PWB_VERSIONS)
    local_type = 'Powerboard-' + version
    local_type_count = len(inv_df[inv_df["Local Type"] == local_type])
    local_name = "IHEP-"+local_type+"-"+str(local_type_count+1)
    current_local_stage = "RECEIVED"
    current_operator = st.session_state['Reception']['uName']
    sub_table_file_name = local_name+".pkl"
    sub_table_file_dir = os.path.join(tools.PWB_DATA_PATH, local_name)
    tools.mkdirs(sub_table_file_dir)
    sub_table_file_path = os.path.join(sub_table_file_dir, sub_table_file_name)
    sub_df = pd.DataFrame(  {'Local Name': [local_name], } )

    if st.button("Write current component to local database"):
        if len(atlas_sn) == 14 and version != "":
            if len(inv_df[(inv_df["Local Name"] == local_name) | (inv_df["ATLAS SN"] == atlas_sn)]) == 0:
                dic = {'Local Name': local_name, 'ATLAS SN': atlas_sn, 'Local Alias': local_alias,
                        'Local Type': local_type, 'Current Local Stage': current_local_stage, 'Current Operator': current_operator, 'Next Operation':np.nan,
                        'Next Operator':np.nan, 'Next Operation DDL':np.nan, 'Sub-table Path': sub_table_file_path}
                
                inv_df = inv_df.append(dic,ignore_index=True)   # TODO: pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here, change to pandas.DataFrame.concat
                sub_df.to_pickle(sub_table_file_path)
                inv_df.to_pickle(inv_path)                                                                
                st.info("Component has been received to the local database!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Component already exists!")
        else:
            st.error("Please fill in all the fields correctly ")

def bareModuleReception(inv_path):
    inv_df = tools.get_inventory(inv_path)

    atlas_sn = st.text_input('Enter the bare module\'s ATLAS SN') ###TODO: more time-saving way
    if len(atlas_sn) != 14:
        st.error("ATLAS SN should have 14 digits")
    local_alias = st.text_input('Enter the bare module\'s local alias (SN of the sensor, printed on the envelope)')
    module_type = st.selectbox('Select the type of the bare module (can be infered from SN, will be removed)', ("",)+ tools.BAREMODULE_TYPES) ### Too messy here......
    version = st.selectbox('Select the version of the bare module', ("",)+ tools.BAREMODULE_VERSIONS)
    local_type = 'BareModule-' + module_type + "-" + version
    local_type_count = len(inv_df[inv_df["Local Type"] == local_type])
    local_name = "IHEP-"+local_type+"-"+str(local_type_count+1)
    current_local_stage = "RECEIVED"
    current_operator = st.session_state['Reception']['uName']
    sub_table_file_name = local_name+".pkl"
    sub_table_file_dir = os.path.join(tools.BAREMODULE_DATA_PATH, local_name)
    tools.mkdirs(sub_table_file_dir)
    sub_table_file_path = os.path.join(sub_table_file_dir, sub_table_file_name)
    sub_df = pd.DataFrame(  {'Local Name': [local_name], } )
    
    if st.button("Write current component to local database"):
        if len(atlas_sn) == 14 and version != "":
            if len(inv_df[(inv_df["Local Name"] == local_name) | (inv_df["ATLAS SN"] == atlas_sn)]) == 0:
                dic = {'Local Name': local_name, 'ATLAS SN': atlas_sn, 'Local Alias': local_alias,
                        'Local Type': local_type, 'Current Local Stage': current_local_stage, 'Current Operator': current_operator, 'Next Operation':np.nan,
                        'Next Operator':np.nan, 'Next Operation DDL':np.nan, 'Sub-table Path': sub_table_file_path}
                
                inv_df = inv_df.append(dic,ignore_index=True)   # TODO: pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here, change to pandas.DataFrame.concat
                sub_df.to_pickle(sub_table_file_path)
                inv_df.to_pickle(inv_path)                                                                
                st.info("Component has been received to the local database!")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.error("Component already exists!")
        else:
            st.error("Please fill in all the fields correctly ")

def VisualInspection(local_type, inv_path):
    inv_df = tools.get_inventory(inv_path)
    sub_inv_df = inv_df[(inv_df['Local Type'] == local_type) & (inv_df['Current Local Stage'] == 'RECEIVED')]
    local_name = st.selectbox('Please select the component you want to work on', ('',) + tuple(sub_inv_df['Local Name'].tolist()))
    
    if local_name != '':
        sub_inv_df.set_index('Local Name', inplace=True)
        sub_table_file_path = sub_inv_df.loc[local_name,'Sub-table Path']
        if st.checkbox("Start to upload visual inspection (reception) photos"):
            result_dir = os.path.join(os.path.dirname(sub_table_file_path),'VI_R_photos')
            tools.mkdirs(result_dir)

            st.write("### Visual Inspection")
            uploaded_images = st.file_uploader("Upload visual inspection (reception) photos ", accept_multiple_files=True, help='Can have multiple images uploaded at a time')  #TODO: file type protection?
            st.write("#### Uploaded photos")
            stored_raw_files = []
            # image_counter = 0
            for uploaded_image in uploaded_images:
                st.image(uploaded_image, caption="Visual inspection (reception) photo")
                stored_raw_file = os.path.join(result_dir, uploaded_image.name)
                stored_raw_files.append(stored_raw_file)
                with open(stored_raw_file,"wb") as f:
                    f.write(uploaded_image.getbuffer())
            ### write to local server, record directory
        if st.button('Passed'):
            this_idx = inv_df['Local Name'].tolist().index(local_name)  
            inv_df.loc[this_idx,'Current Local Stage'] = 'READY'
            inv_df.loc[this_idx,'Current Operator'] = st.session_state['Reception']['uName']
            inv_df.to_pickle(inv_path)                                                                
            time.sleep(1)
            st.experimental_rerun()

            # st.write("Images saved to local server")

def uploadIVTestResults():
    st.write("#### upload IV test dat file here...") 
    st.write("#### analysis here...")               #reuse Kenny's WebApp
    st.write("#### write to local server, record directory & show")
    pass

def componentReception(inv_path):
    component_type = st.selectbox("Select the type of component you're going to receive", ("",)+ihep_component_receive)

    if component_type == 'ABC':
        ABCReception(inv_path)
    elif component_type == 'HCC':
        HCCReception(inv_path)
    elif component_type == 'HybridFlex':
        hybridFlexReception(inv_path)
    elif component_type == 'PowerBoard':
        powerBoardReception(inv_path)
    elif component_type == 'BareModule':
        bareModuleReception(inv_path)

def componentTesting(inv_path):
    component_type = st.selectbox("Select the type of component you're going to test", ('',)+ihep_component_receive)

    if component_type == 'ABC':
        version = st.selectbox('Select the version of the ABCStar chip', ('',)+ tools.ABCSTAR_VERSIONS)
        local_type = 'ABCStar-' + version
        if version != '':
            VisualInspection(local_type, inv_path)
    elif component_type == 'HCC':
        version = st.selectbox('Select the version of the HCCStar chip', ('',)+ tools.HCCSTAR_VERSIONS)
        local_type = 'HCCStar-' + version
        if version != '':
            VisualInspection(local_type, inv_path)
    elif component_type == 'HybridFlex':
        flex_type = st.selectbox('Select the type of the hybrid flex', ('',)+ tools.HYBRIDFLEX_TYPES)
        version = st.selectbox('Select the version of the hybrid flex', ('',)+ tools.HYBRIDFLEX_VERSIONS)
        local_type = 'HybridFlex-' + flex_type + "-" + version
        if version != '' and local_type != '':
            VisualInspection(local_type, inv_path)
    elif component_type == 'PowerBoard':
        version = st.selectbox('Select the version of the powerboard', ('',)+ tools.PWB_VERSIONS)
        local_type = 'Powerboard-' + version
        if version != '':
            VisualInspection(local_type, inv_path)
    elif component_type == 'BareModule':
        bm_type = st.selectbox('Select the type of the bare module', ('',)+ tools.BAREMODULE_TYPES)
        version = st.selectbox('Select the version of the bare module', ('',)+ tools.BAREMODULE_VERSIONS)
        local_type = 'BareModule-' + bm_type + "-" + version
        if version != '' and local_type != '':
            VisualInspection(local_type, inv_path)

def receptionFlow():
    pass
#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Reception", ":truck: Reception", infoList)

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

        ##########
        inventory_path = os.path.join(tools.DATA_PATH, 'inventory.pkl')
        # inv_df = tools.get_inventory(inventory)
        if not st.session_state.dummy:
            client = st.session_state.myClient
            pageDict['uName'] = tools.uid_to_uname(st.session_state.Homepage['user']['userIdentity']) # get uid from Homepage and convert to uname using local mapping
        else:
            pageDict['uName'] = st.session_state.Homepage['user']

        task = st.radio("Select task:", ("Receive new components", "Test received components"))
        if task == "Receive new components":
            componentReception(inventory_path)
        elif task == "Test received components":
            componentTesting(inventory_path)