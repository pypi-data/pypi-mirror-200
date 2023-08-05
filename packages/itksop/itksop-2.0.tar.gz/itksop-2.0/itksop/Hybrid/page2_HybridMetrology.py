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
from utils.HybridMetrology.Gen_CDF import Gen_CDF_PPA, Gen_CDF_PPB
# from utils.HybridMetrology.process_data import process_data
from utils.HybridMetrology.metrologyanalysis import analysis

#####################
### useful functions
#####################

infoList = ["  * Measure Hybrids",
            "   * Nothing here..."]

def measureHybrid(df):
    st.write('##### Operation steps for hybrid measurement')
    st.write('###### 1. Check the switch on the right side of the Smartscope, the power switch on the joystick.')
    st.write('###### 2. Open the portal. Program self-check. Click professional, open measuremind. Attention, in the self-check the lens can suddenly go down, keep a cerntain distance.')
    st.write('###### 3. Use a tweezer to put the hybrid on the jig. Put the jig on the platform, make sure positioning bars work. Connect vacuum tube to the jig and turn on the vacuum. ')
    st.write('###### 4. Find the most left fiducial mark on the hybrid before loading the routine. Focus, then set X,Y,Z=0. Then load the the routine. ')
    st.write('###### 5. Step by step run the routine until x-axis set. Then run automatically.')
    st.write('----- Exception handling: if error occurs or the centroid finding do not find the correct object(cross mark or the shining pad), re-run the step.')
    st.write('###### 6. File-Save the output file. Use an external storage to save the file.')
    
    if st.checkbox(' Measurement finished. '):
        df.loc[len(df)-1,"State"] = 'HYBRID_MEASURED'
    
    return df

# def st_display_pdf(pdf_file):
#     with open(pdf_file, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="600" type="application/pdf">'
#     st.markdown(pdf_display, unsafe_allow_html=True)

# def metrology_processing():
#     raw_file = st.file_uploader("Upload the raw file obtained from SmartScope to local storage", help='Only accept one .txt file at a time')  
#     if raw_file is not None:
#         st.info('Working on: '+raw_file.name)
#         hybrid_name = st.text_input('Enter hybrid\'s  name') 
#         hybrid_type = st.selectbox('Select hybrid type', ('HX','HY'))
#         campaign = st.selectbox('Select production campaign', ('PPA','PPB'))
#         if ' ' in hybrid_name:
#             st.error('ERROR: The hybrid\'s name should not contain space')
#             st.stop()
#         run_num = st.number_input('Enter run number', value=0)
#         result_dir = "/home/atlasitk/ihep-sop/data/standalone_metrology_result/"+hybrid_name 
#         tools.mkdirs(result_dir)

#         stored_raw_file = os.path.join(result_dir, raw_file.name)
#         with open(stored_raw_file,"wb") as f:
#             f.write(raw_file.getbuffer())
        
#         cdf_outfile_name = "HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num)+'.txt'
#         cdf_outfile_path = os.path.join(result_dir,cdf_outfile_name)
#         itk_strip_sub = 'SB'
#         hybrid_ref_id = hybrid_name
#         institute = 'IHEP'
#         operator = st.text_input('Enter the operator''s name')
#         instrument = 'SmartScope CNC300'
#         program_name = st.text_input('Enter Program Name') 
        
#         if run_num != 0 and operator != '':
#             warning_placeholder = st.empty()
#             if os.path.exists(cdf_outfile_path):
#                 with warning_placeholder.container():
#                     st.warning(cdf_outfile_name+' already exists! Insert another run number or ignore this message if you do want to process this file in the next step.')

#             else:
#                 if st.button('Convert raw data'):
#                     with st.spinner('Processing...'):
#                         # convert_raw(raw_file, cdf_outfile_path, itk_strip_sub, hybrid_type, hybrid_ref_id, institute, operator, instrument, run_num)
#                         HybridMetrology(stored_raw_file, cdf_outfile_path, itk_strip_sub, hybrid_type, hybrid_ref_id, institute, operator, instrument, program_name, run_num)
#                         time.sleep(1)
#                     st.info('Raw data converted')

#             if st.checkbox('Raw file conversion finished'):
#                 infile = open(cdf_outfile_path, 'r')
#                 if infile is not None:
#                     st.info('Working on: '+str(infile.name))
#                     outpath = result_dir
#                     run_num_str = str(infile.name).rstrip('.txt').split('_')[-1]                                      
#                     args_dict = {
#                         'inputFile': cdf_outfile_path,
#                         'outputDir': result_dir,
#                         'type': hybrid_type,
#                         'campaign': campaign,
#                         'tag': "",
#                         "useEdges": False, 
#                         "isBowTest": False,
#                         "skipJSON": False, 
#                         "passed": False,
#                         "problems": False, 
#                         "download_prototype": False,
#                     }
#                     if st.checkbox('Check to start process CDF data'):
#                         st.write('#### Outputs:')
#                         # txt_path, json_path = process_data(infile, outpath, run_num_str) #TODO: cope with multiple tests
#                         args = argparse.Namespace(**args_dict)
#                         analysis.analysis(args)
#                         # time.sleep(1)

#                         pdf_glue_height = os.path.join(result_dir,"HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num),"plots","asic_glue_height.pdf")
#                         pdf_package_height = os.path.join(result_dir,"HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num),"plots","asic_package_height.pdf")
#                         pdf_asic_relative_position = os.path.join(result_dir,"HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num),"plots","asic_relative_position.pdf")
#                         pdf_asic_tilt = os.path.join(result_dir,"HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num),"plots","asic_tilt.pdf")
#                         pdf_full_hybrid = os.path.join(result_dir,"HybridMetrologyCDF_"+hybrid_name+'_run'+str(run_num),"plots","full_hybrid.pdf")

#                         col1, col2 = st.columns(2)
#                         with col1:
#                             st_display_pdf(pdf_glue_height)
#                         with col2:
#                             st_display_pdf(pdf_package_height)
                        
#                         col3, col4 = st.columns(2)
#                         with col3:
#                             st_display_pdf(pdf_asic_relative_position)
#                         with col4:
#                             st_display_pdf(pdf_asic_tilt)

#                         col5, col6 = st.columns(2)
#                         with col5:
#                             st_display_pdf(pdf_full_hybrid)


#                     if st.button('CDF data process finished'):
#                         st.balloons()
    

def convertRawFile(df):
    raw_file = st.file_uploader("Upload the raw file obtained from SmartScope to local database", help='Only accept one .txt file at a time')  
    if raw_file is not None:
        st.info('Working on: '+raw_file.name)
        hybrid_local_name = df.loc[len(df)-1, 'Local Name']
        run_num = st.number_input('Insert run number', value=0, step=1)
        result_dir = st.session_state['Hybrid Metrology']['result_dir'] 
        
        ### save raw file to result_dir
        stored_raw_file = os.path.join(result_dir, raw_file.name)
        with open(stored_raw_file,"wb") as f:
            f.write(raw_file.getbuffer())

        cdf_outfile_name = "HybridMetrologyCDF_" + hybrid_local_name + '_run_'+str(run_num)+'.txt'
        cdf_outfile_path = os.path.join(result_dir,cdf_outfile_name)

        ### TODO: hard coded, not good
        itk_strip_sub = 'SB'
        hybrid_type = 'HX'
        if '-Y-' in hybrid_local_name:
            hybrid_type = 'HY'
        hybrid_ref_id = df.loc[len(df)-1, 'ATLAS SN']
        institute = 'IHEP'
        operator = st.session_state['Hybrid Metrology']['uName']
        instrument = 'SmartScope CNC300'
        program_name = st.text_input('Enter Program Name') 
        
        if run_num != 0 and program_name != '' :
            warning_placeholder = st.empty()
            if os.path.exists(cdf_outfile_path):
                with warning_placeholder.container():
                    st.warning(cdf_outfile_name+' already exists! Insert another run number or ignore this message if you do want to process this file in the next step.')

            else:
                if st.button('Convert raw data'):
                    with st.spinner('Processing...'):
                        if 'PPA' in hybrid_local_name or 'DUMMY' in  hybrid_local_name:
                            Gen_CDF_PPA(stored_raw_file, cdf_outfile_path, itk_strip_sub, hybrid_type, hybrid_ref_id, institute, operator, instrument, program_name, run_num)
                        elif 'PPB' in hybrid_local_name:
                            Gen_CDF_PPB(stored_raw_file, cdf_outfile_path, itk_strip_sub, hybrid_type, hybrid_ref_id, institute, operator, instrument, program_name, run_num)
                        time.sleep(1)
                    st.info('Raw data converted')

            if st.checkbox('Raw file conversion finished'):
                df['Raw File Path'] = np.nan
                df.loc[len(df)-1, 'Raw File Path'] = stored_raw_file
                df['CDF File Path'] = np.nan
                df.loc[len(df)-1, 'CDF File Path'] = cdf_outfile_path
                df.loc[len(df)-1,"State"] = 'RAW_PROCESSED'
    
        # if os.path.exists(cdf_outfile_path):
        #     st.write('###### The converted file (CDF file) will be automatically passed to the next step, but you can also download the file here')
        #     st.download_button(label='Download converted file (CDF file)', data=open(cdf_outfile_path,'r'),file_name=outfile_name, mime='text/plain')
        
        
    return df

def processCDF(df):
    infile_path = df.loc[len(df)-1, 'CDF File Path']
    infile = open(infile_path, 'r')
    if infile is not None:
        st.info('Working on: '+str(infile.name))
        outpath = os.path.dirname(infile_path)
        hybrid_local_name = df.loc[len(df)-1, 'Local Name']
        hybrid_type = 'HX'
        if '-Y-' in hybrid_local_name:
            hybrid_type = 'HY'

        if 'PPA' in hybrid_local_name or 'DUMMY' in  hybrid_local_name:
            campaign = 'PPA'
        elif 'PPB' in hybrid_local_name:
            campaign = 'PPB'
        
        # run_num_str = str(infile.name).rstrip('.txt').split('_')[-1]
        args_dict = {
            'inputFile': infile_path,
            'outputDir': outpath,
            'type': hybrid_type,
            'campaign': campaign,
            'tag': "",
            "useEdges": False, 
            "isBowTest": False,
            "skipJSON": False, 
            "passed": False,
            "problems": False, 
            "download_prototype": False,
        }
        if st.checkbox('Check to start process CDF data'):
            st.write('#### Outputs:')
            # txt_path, json_path = process_data(infile, outpath, run_num_str) #TODO: cope with multiple tests
            args = argparse.Namespace(**args_dict)
            analysis.analysis(args)

            png_glue_height = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"plots","asic_glue_height.png")
            png_package_height = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"plots","asic_package_height.png")
            png_asic_relative_position = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"plots","asic_relative_position.png")
            png_asic_tilt = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"plots","asic_tilt.png")
            png_full_hybrid = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"plots","full_hybrid.png")

            col1, col2 = st.columns(2)
            with col1:
                st.image(Image.open(png_glue_height), caption= 'ASIC glue height')
            with col2:
                st.image(Image.open(png_package_height), caption= 'Total package height')
            
            col3, col4 = st.columns(2)
            with col3:
                st.image(Image.open(png_asic_relative_position), caption= 'ASIC relative position')
            with col4:
                st.image(Image.open(png_asic_tilt), caption= 'ASIC tilt' )

            col5, col6 = st.columns(2)
            with col5:
                st.image(Image.open(png_full_hybrid), caption= 'Full hybrid')

        if st.checkbox('CDF data process finished'):
            df['JSON File Path'] = np.nan
            df.loc[len(df)-1, 'JSON File Path'] = os.path.join(outpath, os.path.basename(infile_path).split('.')[0],"results.json")
            df.loc[len(df)-1,"State"] = 'CDF_PROCESSED'
    
    return df
    
def uploadMetrologyResults(df,client):
    cdf_path = df.loc[len(df)-1, 'CDF File Path']
    json_path = df.loc[len(df)-1, 'JSON File Path']
    # Read test data from json
    with open (json_path) as f:
        data = json.load(f)
    
    data["componentType"] = "HYBRID_ASSEMBLY"
    data["component"] = df.loc[len(df)-1, 'ATLAS SN']

    # date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    # date = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00",date.timetuple())
    
    # data["date"] = date

    problems = st.checkbox("Problems during test")

    data["problems"] = problems

    if problems:
        problem_comment = st.text_area("Leave a comment about problems during test")
        data["comments"] = [problem_comment]
    else:
        data.pop("comments", 0)

    if st.button("Upload!"):
        if client is not "DUMMY":
            with st.spinner("Uploading..."):
                client.post('uploadTestRunResults', json=data)  #TODO: upload defects at the same time 

                client.post('createTestRunAttachment', data={ "testRun": new_test_result['testRun']['id'], "type" : "file", "title" : os.path.basename(cdf_path)},
                                        files={"data" : (os.path.basename(cdf_path), open(cdf_path, "rb"), mt.guess_type(cdf_path)[0])})
                time.sleep(1)
                st.success("Metrology Result Uploaded")
        else:
            with st.spinner("Uploading..."):
                time.sleep(1)
            st.success("Metrology Result Uploaded")

    if st.checkbox('Uploaded, nothing wrong...'):
        df["Metrology Passed"] = data["passed"]
        df["Metrology Problems"] = data["problems"]
        df["Metrology Test Date"] = data["date"]
        if problems:
            df["Merology Problem Comment"] = data["comments"]
        df.loc[len(df)-1,"State"] = 'MT_UPLOADED' #TODO: DANGER! change State based on the outputs of uploading
    

    return df

def hybridMetrologyFlow(filepath, client, rework=False):

    hybrid_df = pd.read_pickle(filepath)

    if hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] != 'METROLOGY' or rework:
        
        hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'ASIC_ATTACHED'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] = 'METROLOGY'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operator"] = st.session_state['Hybrid Metrology']['uName']
        hybrid_df.loc[len(hybrid_df)-1,"State"] = 'METROLOGY_NOT_STARTED_YET'

        hybrid_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
        # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'METROLOGY_NOT_STARTED_YET':      ### TODO: Add timestamp for each step and change the way of data recording
            st.header('Measure hybrid')
            hybrid_df = measureHybrid(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'HYBRID_MEASURED':
            st.header('Convert raw data file to CDF file')
            hybrid_df = convertRawFile(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'RAW_PROCESSED':
            st.header('Process data')
            hybrid_df = processCDF(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'CDF_PROCESSED':
            st.header('Upload metrology results')
            hybrid_df = uploadMetrologyResults(hybrid_df, client)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'MT_UPLOADED':
            st.header('Hybrid Metrology Done Confirmation')
            if st.button('❗️ CONFIRM: hybrid metrology done!'):
                hybrid_df.loc[len(hybrid_df)-1,"State"] = 'METROLOGY_DONE'
                hybrid_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'METROLOGY_DONE':
            hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'MEASURED'
            success_str = '#### ' + hybrid_df.loc[len(hybrid_df)-1,'Local Name'] + ' --- Hybrid Metrology Done! 🎉🎉🎉🎉🎉🎉'
            st.success(success_str)
            hybrid_df.to_pickle(filepath)

    return hybrid_df
#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Hybrid Metrology", ":straight_ruler: Hybrid Metrology", infoList)

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]
        
        ### Select branches
        # branch = st.selectbox('Select branch:', ('', 'Standalone Metrology Result Processing', 'Production Flow'))

        # st.write('---')
        # if branch == 'Standalone Metrology Result Processing':
        #     st.write('## Standalone Metrology Result Processing')

            # metrology_processing()

            # st.write('---')
        
        # if branch == 'Production Flow':
        st.write('## Production Flow')
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
        hybrid_mea_u_df = df_havNextOp[df_havNextOp['Local Type'].str.contains('Hybrid') & (df_havNextOp['Next Operation'] == 'METROLOGY') & (df_havNextOp['Next Operator'] == pageDict['uName'])]
        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        rework = False

        if not hybrid_mea_u_df.empty :
            # st.info('###### Hi '+pageDict['uName'].split(' ')[0]+', welcome to work!')
            task_selector = st.empty()
            with task_selector.container():
                hybrid_local_name = st.selectbox('Please select the hybrid you want to work on', selectbox_init_v_tpl + tuple(hybrid_mea_u_df['Local Name'].tolist()))

            if hybrid_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                hybrid_mea_u_df.set_index('Local Name', inplace=True)
                hybrid_sub_table_file_path = hybrid_mea_u_df.loc[hybrid_local_name,'Sub-table Path']
                hybrid_local_alias = hybrid_mea_u_df.loc[hybrid_local_name,'Local Alias']
                
                st.info('###### Now working on: '+hybrid_local_name + ' (' + hybrid_local_alias + ') ')
                pageDict['result_dir'] = os.path.join(os.path.dirname(hybrid_sub_table_file_path), 'metrology_results')  
                tools.mkdirs(pageDict['result_dir'])

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start current task from scratch) ❗️')

                df_this_hybrid = hybridMetrologyFlow(hybrid_sub_table_file_path, client, rework)

                if df_this_hybrid['Current Local Stage'].tolist()[-1] == 'MEASURED':
                    this_hybrid_idx = inv_df['Local Name'].tolist().index(hybrid_local_name) 
                    inv_df.loc[this_hybrid_idx,'Current Local Stage'] = 'MEASURED'
                    inv_df.loc[this_hybrid_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_hybrid_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operation DDL'] = np.nan
                    inv_df.to_pickle(inventory)

                st.write('---')
                st.write('#### Current Hybrid Info:')
                st.dataframe(df_this_hybrid) 
            
        
                