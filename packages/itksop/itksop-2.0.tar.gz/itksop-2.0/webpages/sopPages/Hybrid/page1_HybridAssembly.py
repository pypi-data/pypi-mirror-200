import datetime
import os 
import random
import time 

import numpy as np
import pandas as pd
import streamlit as st

from core.Page import Page
import core.tools as tools

#####################
### useful functions
#####################

infoList=["  * Assemble Hybrids...",
          "   * Nothing..."]

###
### functions of sub_steps
###
def positionCalibration():
    state = False
    step0 = step1 = step2 = step3 = step4 = step5 = step6 = step7 = step8 = step9 = step10 = False

    step0 = st.checkbox('Get ready for position calibration')
    step0_tips = st.empty()
    with step0_tips.container():
        st.write('###### Tips:')
        st.write('* Turn on the vacuum pump if it is off')
        st.write('* Use a tweezer to place the HFFC(hybrid flex for calibration) on the corresponding location of the hybrid assembly jig')
        st.write('* Turn of the vacuum of the hybrid assembly jig')

    if step0:
        step0_tips.empty()
        step1 = st.checkbox('Press \'Mode\' on the controller of the dispenser, select \'Teaching Mode\', then press \'Enter\'')
    
    if step1:
        step2 = st.checkbox('Confirm the program number in teaching mode')
        step2_tips = st.empty()
        with step2_tips.container():
            st.write('###### Tips:')
            st.write('* PPA: Program 70 for X hybrid; Program 71 for Y hybrid')
            st.write('* PPB: Program 72 for X hybrid; Program 73 for Y hybrid')

    if step2:
        step2_tips.empty()
        step3 = st.checkbox('Press \'Edit\' and select \'Block Editing\', then press \'Enter\'. Press \'F4\' on the keyboard(Select all points in the program)')

    if step3:
        step4 = st.checkbox('Select \'Jog Offset\', insert \'3\'(i.e. select the 3rd point) and press \'Enter\' ')
        step4_tips = st.empty()
        with step4_tips.container():
            st.write('###### Tips:')
            st.write('* The 3rd point is the central point of the 1st pad, making it easy to calibrate the position')

    if step4:
        step4_tips.empty()
        step5 = st.checkbox('\'Original Position\' should be shown on the screen now. Press \'Enter\', change \'Original Position\' into \'Shift Position\' ')

    if step5:
        step6 = st.checkbox('Press \'Go\' on the keyboard to move the needle to the \'Shift Position\'')
        step6_tips = st.empty()
        with step6_tips.container():
            st.write('###### Tips:')
            st.write('* A possible problem of this step: needle might hit the pad if original position is too low (solution needed here...)')

    if step6:
        step6_tips.empty()
        step7 = st.checkbox('Use direction keys of the X/Y direction to adjust the horizontal position of the needle, keep the needle centered on the first pad')

    if step7:
        step8 = st.checkbox('Use direction keys of the Z direction to adjust the height of the needle')
        step8_tips = st.empty()
        with step8_tips.container():
            st.write('###### Tips:')
            st.write('* Place a 0.5 mm feeler gauge between the needle and HFFC')
            st.write('* Adjust the height to let the needle just touch the ruler without high friction')

    if step8:
        step8_tips.empty()
        st.write('###### The needle is at the right position now')
        step9 = st.checkbox('Press \'Enter\', then press \'Esc\' to get back to the program and then press \'Save\'')

    if step9:
        step10 = st.checkbox('Press \'Go\' to get back to home point (initial poisition)')

    if step10:
        state = True

    return state

def weighComponent( componentName ):
    componentName = str(componentName)

    weight = st.number_input('Insert weight of the '+ componentName + ' (unit: gram) ',key=componentName+'_weight',value=0.0, step = 0.00001, format='%.5f')
    st.write('The weight of '+componentName+' is ', weight, ' g')
    
    return weight

def placeASICs(df, ASICType, ASICCount):
    state = False 
    gelpack_lid_removed = gelpackNchips_weighed = chips_placed = chips_SN_recorded = False

    selectbox_init_v = ''
    selectbox_init_v_tpl = (selectbox_init_v,)
    ASICType =str(ASICType)

    inventory_df = st.session_state['Hybrid Assembly']['inventory_df']  ###not very elegant?????
    ava_chips_list=inventory_df[inventory_df['Local Type'].str.contains(ASICType) & (inventory_df['Current Local Stage']=='READY')].loc[:,'ATLAS SN'].to_list()

    gelpack_lid_removed = st.checkbox('Remove the lid of '+ASICType+' chips gel pack')
    if gelpack_lid_removed:
        st.write('###### Weigh the gel pack and chips on it together')
        gelpackNchips_weight = weighComponent(ASICType+' gel pack + chips')
        if gelpackNchips_weight > 0:
            gelpackNchips_weighed = True
    
    if gelpackNchips_weighed:
        if st.checkbox('Put the '+ ASICType +' gel pack on the TRAY-VAC and turn on valve of the compressed air'):
            chips_placed =st.checkbox('Use a vacuum pen to pick up '+str(ASICCount)+' ' +ASICType+' chip(s) and place it/them on the chip tray')

    if chips_placed:
        st.write('###### Record the ATLAS SN of selected chip(s)')
        chip_SN = []
        for i in range(ASICCount):
            chip_SN.append(st.selectbox('Please select the ATLAS SN of '+ASICType+' chip '+str(i), selectbox_init_v_tpl + tuple(ava_chips_list)) )

        for i in range(ASICCount):
            if chip_SN[i] != selectbox_init_v:
                df['ATLAS SN of '+ASICType+' chip '+str(i)] = np.nan
                df.loc[len(df)-1,'ATLAS SN of '+ASICType+' chip '+str(i)] = chip_SN[i]
                
        chips_SN_recorded = st.checkbox('All '+ ASICType +' chip(s) recorded')
    
    if chips_SN_recorded:
        st.write('###### Weigh the gel pack with '+ str(ASICCount) +' chip(s) removed')
        gelpack_weight = weighComponent(ASICType+' gel pack with '+ str(ASICCount) +' chip(s) removed')
        chips_weight = gelpackNchips_weight - gelpack_weight
        st.write('The weight of chip(s) is ', chips_weight, ' g')
        if chips_weight > 0 and chips_weight < 1:
            df['Weight of ' + ASICType + ' chip(s) (g)'] =  np.nan
            df.loc[len(df)-1,'Weight of ' + ASICType + ' chip(s) (g)'] = chips_weight
            state = True

    return state, df

###
### functions of steps
###
def prepGlueDispenser(df):
    glue_installed = position_calibrated = air_compressor_opened = connectivity_checked = False

    # st.write('##### Get the dispenser ready!')
    glue_installed = st.checkbox('Install glue')
    glue_installation_tips = st.empty()
    with glue_installation_tips.container():
         st.write('###### Tips:')
         st.write('* Take a tube of glue out of the black box under the table')
         st.write('* Twiste off the front lid of the glue tube and install a needle')
         st.write('* Open the rear cover of the glue tube and install the vacuum pipe of the dispenser')
         st.write('* Place the glue tube on the bracket on the dispenser and tighten it with a screwdriver')

    if glue_installed:
        glue_installation_tips.empty()
        position_calibrated = positionCalibration()

    if position_calibrated:
        air_compressor_opened = st.checkbox('Turn on the dispenser dedicated air compressor')
        air_compressor_tips = st.empty()
        with air_compressor_tips.container():
            st.write('###### Tips:')
            st.write('* The glue dispenser has a dedicated air compressor')
            st.write('* Turn on the power and valve of the compressor, pull the red switch on it to activate the air compressor')

    if air_compressor_opened:
        air_compressor_tips.empty()
        if st.checkbox('Place a piece of cleanroom wiper right under the needle of glue tube and push \'Purge\' on the dispenser'):
            connectivity_checked = st.checkbox('Glue flows smoothly!')
    
    if connectivity_checked:
        df.loc[len(df)-1,"State"] = 'DISPENSER_PREPED'

    return df

def calibrateGlueWeight(df):
    hffc_weighed = hffc_placed = glue_dispensed = glue_weighed = False

    st.write('###### Weigh the bare HFFC(hybrid flex for calibration)')
    hffc_weight = weighComponent('HFFC(hybrid flex for calibration) ')
    if hffc_weight > 0:
        hffc_weighed = True

    if hffc_weighed:
        hffc_placed = st.checkbox('Use a tweezer to place the HFFC on the hybrid assembly jig and turn on the vacuum of the jig')

    if hffc_placed:
        sub_step1 = sub_step2 = sub_step3 = False
        sub_step1 = st.checkbox('Clean the needle with a piece of cleanroom wipper')
        if sub_step1:
            sub_step2 = st.checkbox('Press \'Mode\' on the controller of the dispenser, switch to \'Run Mode\' and press \'Enter\' ')
        if sub_step2:
            sub_step3 = st.checkbox('Press the green \'Start\' button to start dispensing')
        if sub_step3:
            glue_dispensed = st.checkbox('Glue dispensing finished!')
    
    if glue_dispensed:
        st.write('###### Weigh the HFFC with glue on it')
        hffc_removed = st.checkbox('Use a tweezer to take the HFFC from the jig and weigh it, don\'t touch the glue on it!')
        if hffc_removed:
            hffcNglue_weight = weighComponent('HFFC + glue')
            glue_weight = hffcNglue_weight - hffc_weight
            st.write('The weight of glue is ', glue_weight, ' g')
            glue_weight_tips = st.empty()
            with glue_weight_tips.container():
                st.write('###### Tips:')
                st.write('* The standard weight of the glue on PPA (DUMMY) hybrid is 43.5 +/- 2.6mg, PPB hybrid is 43.8 +/- 2.62mg')
                st.write('* Each ABCStar V1 chip is glued down with 4.20 +/- 0.25 mg and each HCCStar V0 chip with 1.5 +/- 0.1 mg (or 1.8 +/- 0.12 mg for V1)')

            if "PPA" in df.loc[len(df)-1,"Local Name"] or "DUMMY" in df.loc[len(df)-1,"Local Name"]:
                if glue_weight < 0.0461 and glue_weight > 0.0409 :   #TODO: Use a file that contains all these specs instead ... 
                    glue_weighed = True
                elif glue_weight > 0:
                    st.warning('###### Glue weight doesn\'t meet the requirement! Clean the HFFC and the jig, adjust the dispensing time and try again') ### TODO: add functions to facilitate dispensing time adjustment
            elif "PPB" in df.loc[len(df)-1,"Local Name"]:
                if glue_weight < 0.04642 and glue_weight > 0.04118 :
                    glue_weighed = True
                elif glue_weight > 0:
                    st.warning('###### Glue weight doesn\'t meet the requirement! Clean the HFFC and the jig, adjust the dispensing time and try again') ### TODO: add functions to facilitate dispensing time adjustment


                
    if glue_weighed:
        if st.checkbox('Clean the HFFC and the jig!'):
            glue_weight_tips.empty()
            df.loc[len(df)-1,"State"] = 'GLUE_WEIGHT_CALED'
    
    return df
    

def dispenseGlue(df):
    flex_cut = flex_weighed = flex_placed = glue_dispensed = glue_weighed = False

    st.info('###### Hybrid Flex Name: '+ df.loc[len(df)-1,'Hybrid Flex Name'] +' ( '+str(df.loc[len(df)-1,'Local Alias'])+' ) ')   ### the local alias of hybrid flex == the local alias of hybird assembly
    flex_cut = st.checkbox('Use a graver to cut off the specified hybrid flex')

    st.write('###### Weigh the bare hybrid flex')
    if flex_cut:
        flex_weight = weighComponent('hybrid flex')
        if flex_weight > 0:
            df['Weight of Hybrid Flex (g)'] = np.nan
            df.loc[len(df)-1,'Weight of Hybrid Flex (g)'] = flex_weight
            flex_weighed = True

    if flex_weighed:
        flex_placed = st.checkbox('Use a tweezer to place the hybrid flex on the hybrid assembly jig and turn on the vacuum')
    
    if flex_placed:
        purge_glue = st.checkbox('Push \'Purge\' on the dispenser, make sure there are glue come out')
        if purge_glue:
            glue_dispensed = st.checkbox('Push \'Start\' on the dispenser, wait for the dispenser to finish glue dispensing')
    
    # if glue_dispensed:
    #     st.write('###### Weigh the hybrid flex with glue on it')
    #     flex_removed = st.checkbox('Use a tweezer to take the hybrid flex from the jig and weigh it, don\'t touch the glue on it!')
    #     if flex_removed:
    #         flexNglue_weight = weighComponent('hybrid flex + glue')
    #         glue_weight = flexNglue_weight - flex_weight
    #         st.write('The weight of glue is ', glue_weight, ' g')
    #         glue_weight_tips = st.empty()
    #         with glue_weight_tips.container():
    #             st.write('###### Tips:')
    #             st.write('* The standard weight of the glue on PPA hybrid is 43.5 +/- 2.6mg')
    #             st.write('* Each ABCStar V1 chip is glued down with 4.20 +/- 0.25 mg and each HCCStar V0 chip with 1.5 +/- 0.1 mg (or 1.8 +/- 0.12 mg for V1)')

    #         if glue_weight > 0.01:
    #             df['Weight of Glue on Hybrid Flex (g)'] =  np.nan
    #             df.loc[len(df)-1,'Weight of Glue on Hybrid Flex (g)'] = glue_weight
    #             glue_weighed = True

    if glue_dispensed:
        if st.checkbox('Keep hybrid flex on the jig and keep the vacuum on'):
            # glue_weight_tips.empty()
            df.loc[len(df)-1,"State"] = 'GLUE_DISPENSED'
    
    return df

def attachASICs(df):
    gel_pack_ready = ABCStar_placed = HCCStar_placed = chips_glued = hybrid_weighed = False

    gel_pack_ready = st.checkbox('Take ABCStar chips gel pack and HCCStar chips gel pack out of the drying cabinet')
    if gel_pack_ready:
        st.write('##### For ABCStar Chips')
        ABCStar_placed, df = placeASICs(df, 'ABCStar', 10) 
    
    if ABCStar_placed:
        st.write('##### For HCCStar Chips')
        HCCStar_placed, df = placeASICs(df, 'HCCStar', 1) 
    
    if HCCStar_placed:
        sub_step1 = sub_step2 = sub_step3 = sub_step4 = False
        sub_step1 = st.checkbox('Find the correspoding hybrid pickup tool, leave the vacuum closed and put it on the chip tray')
        if sub_step1:
            sub_step2 = st.checkbox('Turn on the vacuum of the hybrid pickup tool, make sure all chips are picked up and no significant deviation in position')
        if sub_step2:
            sub_step3 = st.checkbox('Move the pickup tool to the hybrid assembly jig and add weights that correspond to the pickup tool')
        if sub_step3:
            sub_step4 = st.checkbox('Use a black box to cover the UV light. Wear your goggles and turn on the UV light for 5 minutes')
        if sub_step4:
            chips_glued = st.checkbox('5 minutes is up! Turn off the UV light and the vacuum of the hybrid pickup tool, remove the weight on the puckup tool')

    if chips_glued:
        st.write('###### Turn off the vacuum of hybrid assembly jig and weigh the finished hybrid')
        hybrid_weight = weighComponent('the finished hybrid')
        if hybrid_weight > 0:
            df['Weight of Finished Hybrid (g)'] = np.nan    
            df.loc[len(df)-1,'Weight of Finished Hybrid (g)'] = hybrid_weight
            hybrid_weighed = True
    
    if hybrid_weighed:
        if st.checkbox('Put the finished hybrid back to the drying cabinet'):
            df.loc[len(df)-1,"State"] = 'CHIPS_ATTACHED'
    
    return df
    

def cleanUp(df):
    compressor_off = glue_tube_uninstalled = False

    compressor_off = st.checkbox('Turn off the the dispenser dedicated air compressor')
    if compressor_off:
        glue_tube_uninstalled = st.checkbox('Uninstall the glue tube and put it back to the black box')
    if glue_tube_uninstalled:
        df.loc[len(df)-1,"State"] = 'CLEANED_UP'
    
    return df

def registerHybridInITkPD(df, client):
    hybrid_type = "X" if "X" in df.loc[len(df)-1,"Local Name"] else "Y"  #TODO: more flexible here
    assembly_jig = st.text_input('Enter the SN of the hybrid assembly jig you used')
    glue_syringe = st.text_input('Enter the ATLAS SN of the glue syringe you used') #TODO:change to select box based on entires in db
    local_name = df.loc[len(df)-1,"Local Name"]
    assembly_chip_tray = st.text_input('Enter the SN of the chip tray you used')
    assembly_pickup_tool = st.text_input('Enter the SN of the pick-up tool you used')

    data={"project":"S",
          "subproject":"SB",
          "institution":"IHEP",
          "componentType":"HYBRID_ASSEMBLY",
          "type": hybrid_type,
          "properties":{
            "ASSEMBLY_JIG":assembly_jig,
            "GLUE_SYRINGE":glue_syringe,
            "LOCAL_NAME":local_name,
            "ASSEMBLY_CHIPTRAY":assembly_chip_tray,
            "ASSEMBLY_PICKUP_TOOL":assembly_pickup_tool,
            "PICK_AND_PLACE_MACHINE":False,
          }
          }
    
    st.write("###### Check inputs")
    st.write(data)

    if assembly_jig != "" and glue_syringe != "" and local_name != "" and assembly_chip_tray != "" and assembly_pickup_tool != "":
        if st.button("Register Hybrid"):
            if client is not "DUMMY":     
                with st.spinner('Registering...'):
                    register_output = client.post("registerComponent", json=data)  
                    atlas_sn = register_output["component"]["serialNumber"]
                    st.session_state['Hybrid Assembly']['hybridAtlasSN'] = atlas_sn
                    time.sleep(1)
                st.success("Hybrid Assembly Registered")
            else:      ### for dummy 
                with st.spinner('Registering...'):
                    if "-X" in local_name:
                        atlas_sn = "86USBHX" + str("{0:07}".format(random.randint(1,9999999)))   #dummy SN haha, not safe TODO: dummy ATLAS SN generator?
                    else:
                        atlas_sn = "86USBHY" + str("{0:07}".format(random.randint(1,9999999)))   #dummy SN haha, not safe

                    st.session_state['Hybrid Assembly']['hybridAtlasSN'] = atlas_sn
                    time.sleep(1)
                st.success("Hybrid Assembly Registered")
        if st.checkbox('Registered, nothing wrong...'):
            try:
                df.loc[len(df)-1,"ATLAS SN"] = st.session_state['Hybrid Assembly']['hybridAtlasSN']
                df["ASSEMBLY_JIG"] = assembly_jig
                df["GLUE_SYRINGE"] = glue_syringe
                df["ASSEMBLY_CHIPTRAY"] = assembly_chip_tray
                df["ASSEMBLY_PICKUP_TOOL"] = assembly_pickup_tool
                df["PICK_AND_PLACE_MACHINE"] = False
                df.loc[len(df)-1,"State"] = 'HYBRID_REGISTERED' #TODO: change State based on the output of registeration?
            except KeyError:
                st.error('Not registered yet!')
                st.stop()

    return df

def assembleHybridChildren(df, client):
    hybrid_SN = df.loc[len(df)-1,"ATLAS SN"]
    flex_SN = df.loc[len(df)-1,"ATLAS SN of Hybrid Flex"]

    st.write('##### HCC child properties')
    hcc_SN = df.loc[len(df)-1,"ATLAS SN of HCCStar chip 0"]
    hcc_wafer_num = st.text_input('Enter the WAFER NUMBER of the HCCStar chip 0 you attached')
    hcc_fuse_id = st.text_input('Enter the FUSE ID of the HCC chip 0 you attached')

    st.write('##### ABC children properties')
    abc_SNs = [df.loc[len(df)-1,"ATLAS SN of ABCStar chip "+str(i)] for i in range(10)]
    if st.checkbox("Not all ABCStar chips have the same WAFER NUMBER"):
        abc_wafer_nums=[]
        for i in range(10):
            abc_wafer_nums.append(st.text_input('Enter the WAFER NUMBER of the ABCStar chip ' + str(i) + ' you attached'))
            #TODO: More flexible & time-saving way to enter wafer number
    else:
        abc_wafer_num  = st.text_input('Enter the wafer number of all the ABCStar chips you attached')
        abc_wafer_nums = [abc_wafer_num for i in range(10)] 

    if hcc_wafer_num != '' and '' not in abc_wafer_nums:
        if st.button("Assemble Children Components"):
            if client is not "DUMMY":
                with st.spinner('Assembling...'):
                    #assemble Hybrid Flex
                    client.post("assembleComponent", json={"parent": hybrid_SN, "child":flex_SN})

                    #assemble HCCStar
                    client.post("assembleComponent", json={"parent": hybrid_SN, "child":hcc_SN, "properties":{"WAFER_NUMBER":hcc_wafer_num, "POSITION_ON_WAFER":"", "FUSE_ID":hcc_fuse_id}}) #TODO: Add POSITION ON WAFER here

                    #assemble ABCStar
                    for i in range(10):
                        client.post("assembleComponent", json={"parent": hybrid_SN, "child":abc_SNs[i], "properties":{"ABC_POSITION":str(i), "WAFER_NUMBER":abc_wafer_nums[i], "POSITION_ON_WAFER":""}}) #TODO: Add POSITION ON WAFER here

                    #change stage of flex
                    client.post("setComponentStage", json={"component": flex_SN, "stage": "ON_HYBRID"}) #TODO: check and change stage of ABC & HCC if necessary
                    
                    time.sleep(1)
                st.success("Children Assembled")
            else:     ### for dummy 
                with st.spinner('Assembling...'):
                    time.sleep(1)
                st.success("Children Assembled")

        if st.checkbox('Assembled, nothing wrong...'):
            try:
                #TODO: Add POSITION ON WAFER of ASICs
                df["HCC_WAFER_NUMBER"] = hcc_wafer_num
                df["HCC_FUSE_ID"] = hcc_fuse_id
                for i in range(10):
                    df["ABC"+str(i)+"WAFER_NUMBER"] = abc_wafer_nums[i]
                df.loc[len(df)-1,"State"] = 'CHILDREN_ASSEMBLED' #TODO: change State based on the outputs of assembling
            except KeyError:
                st.error('Children not assembled yet!')
                st.stop()
    
    return df

def uploadGlueWeight(df, client):
    st.subheader("Upload glue weight (ASICs on hybrid) test result")
    new_test_result = {}

    weight_of_hybrid_all = df.loc[len(df)-1, "Weight of Finished Hybrid (g)"]
    weight_of_hybrid_flex = df.loc[len(df)-1, "Weight of Hybrid Flex (g)"]
    weight_of_ASICs = df.loc[len(df)-1, "Weight of ABCStar chip(s) (g)"] + df.loc[len(df)-1, "Weight of HCCStar chip(s) (g)"]
    weight_of_glue = weight_of_hybrid_all - weight_of_ASICs -weight_of_hybrid_flex
    weight_of_glue_and_flex = weight_of_glue + weight_of_hybrid_flex

    results = {
        "GW_GLUE_ASICS": weight_of_glue,
        "GW_HYBRID_HT": weight_of_hybrid_flex,
        "GW_HYBRID_HTG": weight_of_glue_and_flex,
        "GW_HYBRID_HTGA": weight_of_hybrid_all,
        "GW_ASIC": weight_of_ASICs
    }

    passed = False
    if "PPA" in df.loc[len(df)-1,"Local Name"] or "DUMMY" in df.loc[len(df)-1,"Local Name"]:
        if weight_of_glue < 0.0461 and weight_of_glue > 0.0409 :   #TODO: Use a file that contains all these specs instead ... 
            passed = True
    elif "PPB" in df.loc[len(df)-1,"Local Name"]:
        if weight_of_glue < 0.04642 and weight_of_glue > 0.04118 :
            passed = True

    date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    date = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00", date.timetuple())

    run_number = str(st.number_input("Enter run number",min_value= 0, step= 1, key= "GW_RUN_NUM")) #TODO: a more smart default value (get number of same testrun at current stage and +1)

    data = {"testType": "ASIC_GLUE_WEIGHT",
            "componentType" : "HYBRID_ASSEMBLY",
            'component': df.loc[len(df)-1,"ATLAS SN"], 
            "institution" : "IHEP",
            "passed" : passed, 
            "date" : date,
            "results" : results, 
            "runNumber": run_number,
            "comments": []
            } 

    problems = st.checkbox("Problems during test", key='GW_PROBLEM')

    data["problems"] = problems

    if problems:
        problem_comment = st.text_area("Leave a comment about problems during test", key='GW_COMMENT')
        data["comments"] = [problem_comment,]
    else:
        data.pop("comments", 0)
    
    st.write("###### TestRun results")
    st.write(data)
    # Upload test result
    if run_number != '0':
        if st.button("Upload!"):
            if client is not "DUMMY":
                with st.spinner("Uploading..."):
                    client.post('uploadTestRunResults', json=data)
                    time.sleep(1)
                st.success("Glue Weight Test Result Uploaded")
            else:
                with st.spinner("Uploading..."):
                    time.sleep(1)
                st.success("Glue Weight Test Result Uploaded")
        if st.checkbox('Uploaded, nothing wrong...',  key= "GW_UP_CHECK"):
            df["Glue Weight Passed"] = passed
            df["Glue Weight Problems"] = problems
            df["Glue Weight Test Date"] = date
            if problems:
                df["Glue Weight Problem Comment"] = problem_comment
            df.loc[len(df)-1,"State"] = 'GW_UPLOADED' #TODO: DANGER! change State based on the outputs of uploading
    
    return df

def uploadVisualInspection(df, client):
    st.subheader("Upload visual inspection test result")
    new_test_result = {}

    date = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    date = time.strftime("%Y-%m-%dT%H:%M:%S.000+08:00",date.timetuple())

    run_number = str(st.number_input("Enter run number",min_value= 0, step= 1, key= "VI_RUN_NUM")) #TODO: a more smart default value (get number of same testrun at current stage and +1)

    data = {"component": df.loc[len(df)-1,"ATLAS SN"], 
            "testType": "VISUAL_INSPECTION",
            "institution" : "IHEP",
            "runNumber": run_number,
            "date" : date,
            "comments": [],
            "results":{}
            }

    passed = st.checkbox("Passed", value=True, key='VI_PASS')
    problems = st.checkbox("Problems during test", key='VI_PROBLEM')

    data["passed"] = passed
    data["problems"] = problems

    if not passed or problems:
        comment = st.text_area("Leave a comment about why visual inspection test is not passed / problems during test", key='VI_COMMENT')
        data["comments"] = [comment]                                        
    
    st.write("###### TestRun results")
    st.write(data)
    # Upload test result
    if run_number != '0':
        if st.button("Upload!"):            
            if client is not "DUMMY":
                with st.spinner("Uploading..."):
                    client.post('uploadTestRunResults', json=data)
                    time.sleep(1)
                st.success("Visual Inspection Result Uploaded")
            else:
                with st.spinner("Uploading..."):
                    time.sleep(1)
                st.success("Visual Inspection Result Uploaded")

        if st.checkbox('Uploaded, nothing wrong...', key= "VI_UP_CHECK"):
            df["Visual Inspection (A) Passed"] = passed
            df["Visual Inspection (A) Problems"] = problems
            df["Visual Inspection (A) Test Date"] = date
            if not passed or problems:
                df["Visual Inspection (A) Problem Comment"] = comment
            df.loc[len(df)-1,"State"] = 'VI_UPLOADED' #TODO: DANGER! change State based on the outputs of uploading

    return df

def hybridAssemblyFlow(filepath, client, rework = False):

    hybrid_df = pd.read_pickle(filepath)

    if hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] != 'ASSEMBLY' or rework:
        
        hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = np.nan
        hybrid_df.loc[len(hybrid_df)-1,"Current Operation"] = 'ASSEMBLY'
        hybrid_df.loc[len(hybrid_df)-1,"Current Operator"] = st.session_state['Hybrid Assembly']['uName']
        hybrid_df.loc[len(hybrid_df)-1,"State"] = 'ASSEMBLY_NOT_STARTED_YET'

        hybrid_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
         # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'ASSEMBLY_NOT_STARTED_YET':      ### Shudong TODO: Add timestamp for each step and change the way of data recording
            st.header('Prepare glue dispener')
            hybrid_df = prepGlueDispenser(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'DISPENSER_PREPED':
            st.header('Calibrate glue weight')
            hybrid_df = calibrateGlueWeight(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'GLUE_WEIGHT_CALED':
            st.header('Dispense glue')
            hybrid_df = dispenseGlue(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'GLUE_DISPENSED':
            st.header('Attach ASICs')
            hybrid_df = attachASICs(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()
        
        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'CHIPS_ATTACHED':
            st.header('Clean up!')
            hybrid_df = cleanUp(hybrid_df)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'CLEANED_UP':
            st.header('Register hybrid in ITkDB')
            hybrid_df = registerHybridInITkPD(hybrid_df, client)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'HYBRID_REGISTERED':
            st.header('Assemble child components')
            hybrid_df = assembleHybridChildren(hybrid_df, client)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'CHILDREN_ASSEMBLED':
            st.header('Upload glue weight')
            hybrid_df = uploadGlueWeight(hybrid_df, client)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'GW_UPLOADED':
            st.header('Upload visual inspection')
            hybrid_df = uploadVisualInspection(hybrid_df, client)
            st.write('_______')
            if st.button('❗️ CONFIRM: current step done', key = hybrid_df.loc[len(hybrid_df)-1,"State"]+'_done' ):
                hybrid_df.to_pickle(filepath)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'VI_UPLOADED':
            st.header('Hybrid Assembly Done Confirmation')
            if st.button('❗️ CONFIRM: hybrid assembly done!'):
                hybrid_df.loc[len(hybrid_df)-1,"State"] = 'ASSEMBLY_DONE'
                hybrid_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        hybrid_df = pd.read_pickle(filepath)
        if hybrid_df.loc[len(hybrid_df)-1,"State"] == 'ASSEMBLY_DONE':
            hybrid_df.loc[len(hybrid_df)-1,"Current Local Stage"] = 'ASIC_ATTACHED'
            success_str = '#### ' + hybrid_df.loc[len(hybrid_df)-1,'Local Name'] + ' --- Hybrid Assembly Done! 🎉🎉🎉🎉🎉🎉'
            st.success(success_str)
            hybrid_df.to_pickle(filepath)

    return hybrid_df





#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Hybrid Assembly", ":gear: Hybrid Assembly", infoList)

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
        pageDict['inventory_df'] = inv_df

        if not st.session_state.dummy:
            client = st.session_state.myClient
            pageDict['uName'] = tools.uid_to_uname(st.session_state.Homepage['user']['userIdentity']) # get uid from Homepage and convert to uname using local mapping
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) ]
        else:
            client='DUMMY'
            pageDict['uName'] = st.session_state.Homepage['user']
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) & (inv_df['Local Type'].str.contains("DUMMY"))]
        ### get sub_dataframe which contains entries that belong to this page and logged in user (to enable access control)
        hybrid_asm_u_df = df_havNextOp[df_havNextOp['Local Name'].str.contains('-Hybrid-') & (df_havNextOp['Next Operation'] == 'ASSEMBLY') & (df_havNextOp['Next Operator'] == pageDict['uName'])]
        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        if not hybrid_asm_u_df.empty :
            # st.info('###### Hi '+pageDict['uName'].split(' ')[0]+', welcome to work!')
            task_selector = st.empty()
            with task_selector.container():
                hybrid_local_name = st.selectbox('Please select the hybrid you want to work on', selectbox_init_v_tpl + tuple(hybrid_asm_u_df['Local Name'].tolist()))
                
            rework = False

            if hybrid_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                hybrid_asm_u_df.set_index('Local Name', inplace=True)
                hybrid_sub_table_file_path = hybrid_asm_u_df.loc[hybrid_local_name,'Sub-table Path']
                hybrid_local_alias = hybrid_asm_u_df.loc[hybrid_local_name,'Local Alias']
                
                st.info('###### Now working on: '+hybrid_local_name + ' (' + hybrid_local_alias + ') ')
                pageDict['result_dir'] = os.path.join(os.path.dirname(hybrid_sub_table_file_path), 'assembly_results')  
                tools.mkdirs(pageDict['result_dir'])

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start from scratch) ❗️')

                df_this_hybrid = hybridAssemblyFlow(hybrid_sub_table_file_path, client, rework)

                if df_this_hybrid['Current Local Stage'].tolist()[-1] == 'ASIC_ATTACHED':
                    this_hybrid_idx = inv_df['Local Name'].tolist().index(hybrid_local_name)  
                    inv_df.loc[this_hybrid_idx,'ATLAS SN'] = df_this_hybrid['ATLAS SN'].tolist()[-1]
                    inv_df.loc[this_hybrid_idx,'Current Local Stage'] = 'ASIC_ATTACHED'
                    inv_df.loc[this_hybrid_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_hybrid_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_hybrid_idx,'Next Operation DDL'] = np.nan

                    flex_SN = df_this_hybrid.loc[len(df_this_hybrid)-1,"ATLAS SN of Hybrid Flex"]
                    hcc_SN = df_this_hybrid.loc[len(df_this_hybrid)-1,"ATLAS SN of HCCStar chip 0"]
                    abc_SNs = [df_this_hybrid.loc[len(df_this_hybrid)-1,"ATLAS SN of ABCStar chip "+str(i)] for i in range(10)]
                    
                    inv_df = tools.modifyComponentStagebySN(flex_SN , "ON_HYBRID", pageDict['uName'], inv_df)
                    inv_df = tools.modifyComponentStagebySN(hcc_SN , "ON_HYBRID", pageDict['uName'], inv_df)
                    for i in range(10):
                        inv_df = tools.modifyComponentStagebySN(abc_SNs[i] , "ON_HYBRID", pageDict['uName'], inv_df)

                    inv_df.to_pickle(inventory)

                st.write('---')
                st.write('#### Current Hybrid Info:')
                st.dataframe(df_this_hybrid)