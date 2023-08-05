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

infoList = ["  * Assemble Modules",
            "   * Nothing here..."]

def removeHyb(df, pageDict):

    if 'LS' in df.loc[len(df)-1, 'Local Name']:
        st.info('###### Hybrid X Name: '+df.loc[len(df)-1, 'Hybrid X Name']+' ( '+tools.comp_name_to_alias(df.loc[len(df)-1, 'Hybrid X Name'], pageDict['inventory_df'])+' ) ')
    if 'SS' in df.loc[len(df)-1, 'Local Name']:
        st.info('###### Hybrid X Name: '+df.loc[len(df)-1, 'Hybrid X Name']+' ( '+tools.comp_name_to_alias(df.loc[len(df)-1, 'Hybrid X Name'], pageDict['inventory_df'])+' ) ' 
                + '\n###### Hybrid Y Name:'+df.loc[len(df)-1, 'Hybrid Y Name']+' ( '+tools.comp_name_to_alias(df.loc[len(df)-1, 'Hybrid Y Name'], pageDict['inventory_df'])+' )' )

    remove_wires = st.checkbox('Break all wires which connect the test panel and hybrid(s), be CAREFUL!!!')  ###TODO: disassemble hybrids from test panel in ITkDB in the meantime
    if remove_wires:
        place_hyb_boards = st.checkbox('Use tweezers to put hybrid(s) on a jig/tray')
        if place_hyb_boards:
            st.success('**Hybrid(s) removed! :tada:**')
            df.loc[len(df)-1,"State"] = 'HYB_REMOVED'

    return df

def removePWB(df,pageDict):

    st.info('###### Powerboard Name: '+df.loc[len(df)-1, 'Powerboard Name']+' ( '+tools.comp_name_to_alias(df.loc[len(df)-1, 'Powerboard Name'], pageDict['inventory_df'])+' ) ')

    remove_wires = st.checkbox('Break all wires which connect the test panel and the powerboard, be CAREFUL!!!')  ###TODO: disassemble pwb from testpanel in ITkDB in the meantime
    if remove_wires:
        place_power_board = st.checkbox('Use tweezers to put powerboard on a jig/tray')
        if place_power_board:
            st.success('**Powerboard removed! :tada:**')
            df.loc[len(df)-1,"State"] = 'PWB_REMOVED'
    
    return df

def removeBareModule(df,pageDict):
    state = False

    st.info('###### Bare Module Name: '+df.loc[len(df)-1, 'Bare Module Name']+' ( '+tools.comp_name_to_alias(df.loc[len(df)-1, 'Bare Module Name'], pageDict['inventory_df'])+' ) ')
    
    remove_wires = st.checkbox('Break all wires around the bare module, be CAREFUL!!!')
    if remove_wires:
        st.warning('##### Keep the sensor on the frame now, don\'t move it!')
        state = True
    
    return state

def cutHybTabs(key = 'cut_X_tabs'):
    state = False
    st.write('##### Cut hybrid tabs')
    if st.checkbox('Place hybrid on hybrid assembly jig',key=key+'_place'):
        if st.checkbox('Turn on the vaccum of the hybrid assembly jig',key=key+'_vaccum', help='Use a tweezer to push the hybrid before turn on the vaccum'):
            state = st.checkbox('Use a graver to cut the 3 tabs', key=key+'_cut')
            return state

    return state


def hybridWeight(df):

    tabs_X_cut = weigh_X_hybNtab = weigh_X_hyb_done = False
    tabs_Y_cut = weigh_Y_hybNtab = weigh_Y_hyb_done = False
    hybridXWithTabs = hybridXWeight = hybridXTabs = 0
    hybridYWithTabs = hybridYWeight = hybridYTabs = 0

    if '-LS-' in df.loc[len(df)-1, 'Local Name']:    
        st.write('##### Weigh Hybrid X')
        hybridXWithTabs = st.number_input('Insert weight of hybrid X with tabs',key='hybXWithTabs_weight_LS',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of hybrid X with tabs is ', hybridXWithTabs)
        if hybridXWithTabs > 2 and hybridXWithTabs <3 : ### TODO: hard coded, not good. Better way of protection
            tabs_X_cut = cutHybTabs()

        if tabs_X_cut:
            hybridXTabs  = st.number_input('Insert weight of three tabs in total',key='hybXTabs_weight_LS',value=0.0, step = 0.00001, format='%.5f')
            st.write('The weight of tabs of hybrid X in total is', hybridXTabs)
            hybridXWeight   = hybridXWithTabs - hybridXTabs

        if hybridXWithTabs > 2 and hybridXTabs > 0.1 and hybridXWeight > 1.5:  ### TODO: hard coded, not good. Better way of protection
            st.write('##### The weight of hybrid X is', hybridXWeight)
            df['Weight of Hybrid X (g)'] = np.nan
            df.loc[len(df)-1,'Weight of Hybrid X (g)'] = hybridXWeight
            if st.checkbox('Pickup hybrid with pickup tool and place it on the stand & tighten two bolts'): 
                weigh_X_hyb_done = True

    if '-SS-' in df.loc[len(df)-1, 'Local Name']:
        # Weigh hybrid X
        st.write('##### Weigh Hybrid X')
        hybridXWithTabs = st.number_input('Insert weight of hybrid X with tabs',key='hybXWithTabs_weight_SS',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of hybrid X with tabs is ', hybridXWithTabs)
        if hybridXWithTabs > 2 and hybridXWithTabs <3 :   ### TODO: hard coded, not good. Better way of protection
            tabs_X_cut = cutHybTabs()

        if tabs_X_cut:
            hybridXTabs  = st.number_input('Insert weight of three tabs in total',key='hybXTabs_weight_SS',value=0.0, step = 0.00001, format='%.5f')
            st.write('The weight of tabs of hybrid X in total is', hybridXTabs)
            hybridXWeight   = hybridXWithTabs - hybridXTabs

        if hybridXWithTabs > 2 and hybridXTabs > 0.1 and hybridXWeight > 1.5:  ### TODO: hard coded, not good. Better way of protection
            st.write('##### The weight of hybrid X is', hybridXWeight)
            df['Weight of Hybrid X (g)'] = np.nan
            df.loc[len(df)-1,'Weight of Hybrid X (g)'] = hybridXWeight  
            weigh_X_hyb_done = True

        st.write('---')
        # Weigh hybrid Y
        st.write('##### Weigh Hybrid Y')
        hybridYWithTabs = st.number_input('Insert weight of hybrid Y with tabs',key='hybYWithTabs_weight_SS',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of hybrid Y with tabs is ', hybridYWithTabs)
        if hybridYWithTabs > 2 and hybridYWithTabs <3 : ### TODO: hard coded, not good. Better way of protection
            tabs_Y_cut = cutHybTabs(key = 'cut_Y_tabs')

        if tabs_Y_cut:
            hybridYTabs  = st.number_input('Insert weight of three tabs in total',key='hybYTabs_weight_SS',value=0.0, step = 0.00001, format='%.5f')
            st.write('The weight of tabs of hybrid Y in total is', hybridYTabs)
            hybridYWeight   = hybridYWithTabs - hybridYTabs

        if hybridYWithTabs > 2 and hybridYTabs > 0.1 and hybridYWeight > 1.5:  ### TODO: hard coded, not good. Better way of protection
            st.write('##### The weight of hybrid Y is', hybridYWeight)
            df['Weight of Hybrid Y (g)'] = np.nan
            df.loc[len(df)-1,'Weight of Hybrid Y (g)'] = hybridYWeight
            if st.checkbox('Pickup hybrids with pickup tool and place them on the stand & tighten two bolts'):
                weigh_Y_hyb_done = True

    if ('LS' in df.loc[len(df)-1, 'Local Name']) and  weigh_X_hyb_done:
        st.success('**Hybrid weighed!:tada: Leave the vacuum on!**')
        df.loc[len(df)-1,"State"] = 'HYB_WEIGHED'

    if ('SS' in df.loc[len(df)-1, 'Local Name']) and  weigh_X_hyb_done and weigh_Y_hyb_done:
        st.success('**Hybrids weighed!:tada: Leave the vacuum on!**')
        df.loc[len(df)-1,"State"] = 'HYB_WEIGHED'

    return df

def pwbWeight(df):

    pwbWeight = st.number_input('Insert weight of powerboard',key='pwb_weight',value=0.0, step = 0.00001, format='%.5f')
    st.write('The weight of powerboard is ', pwbWeight)

    if pwbWeight > 1.5:                      ### TODO: hard coded, not good. Better way of protection
        st.write('##### The weight of powerboard is', pwbWeight)
        df['Weight of Powerboard (g)'] = np.nan
        df.loc[len(df)-1,'Weight of Powerboard (g)'] = pwbWeight
        st.success('**Powerboard weighed!:tada:**')
        df.loc[len(df)-1,"State"] = 'PWB_WEIGHED'
    
    return df

def pwbAlign():
    state = False

    st.write('##### Align powerboard')
    if st.checkbox('Powerboard aligned!'):
        state = True

    return state

def bareModuleWeight(df):
    state = False
    weigh_tray = weigh_tray_pass = False
    sensorTray =  trayNbm = bareModule = 0

    st.write('##### Weigh the sensor tray')
    sensorTray = st.number_input('Insert weight of sensor tray',key='sensorTray_weight1',value=0.0, step = 0.00001, format='%.5f')
    st.write('The weight of sensor tray is ', sensorTray)
    if sensorTray > 38 and sensorTray < 45 :  ### TODO: hard coded, not good. Better way of protection
        weigh_tray_pass = True

    if weigh_tray_pass:
        st.write('##### Weigh the bare module and tray')
        trayNbm = st.number_input('Insert weight of tray + bare module',key='trayNbm_weight',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of tray and bare module in total is', trayNbm)
        bareModule   = trayNbm - sensorTray

    if sensorTray > 38 and bareModule > 0:                            ### TODO: hard coded, not good. Better way of protection
        st.write('##### The weight of bare module is', bareModule)
        df['Weight of Bare Module (g)'] = np.nan
        df.loc[len(df)-1,'Weight of Bare Module (g)'] = bareModule
        st.success('**Bare Module weighed!:tada:**')
        state = True
    
    return state, df

def hybGlueWeight(df):

    weigh_tray_pass = False
    sensorTray =  trayNbmNhyb = bmNhyb = hybGlue = 0

    st.write('##### Weigh the sensor tray')
    sensorTray = st.number_input('Insert weight of sensor tray',key='sensorTray_weight2',value=0.0, step = 0.00001, format='%.5f')
    st.write('The weight of sensor tray is ', sensorTray)
    if sensorTray > 38 and sensorTray < 45 :    ### TODO: hard coded, not good. Better way of protection
        weigh_tray_pass = True

    if weigh_tray_pass:
        st.write('##### Weigh the bare module + hybrid(s) + glue + tray ')
        trayNbmNhyb = st.number_input('Insert weight of bare module + hybrid(s) + glue + tray ',key='trayNbmNhyb_weight',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of bare module + hybrid(s) + tray in total is', trayNbmNhyb)
        bmNhyb  = trayNbmNhyb - sensorTray

    if sensorTray > 38 and bmNhyb > 0:          ### TODO: hard coded, not good. Better way of protection
        st.write(' The weight of bare module + hybrid(s) + glue is', bmNhyb)

        if 'LS' in df.loc[len(df)-1, 'Local Name']:
            hybGlue = bmNhyb - df.loc[len(df)-1, 'Weight of Bare Module (g)'] - df.loc[len(df)-1, 'Weight of Hybrid X (g)']
        elif 'SS' in df.loc[len(df)-1, 'Local Name']:
            hybGlue = bmNhyb - df.loc[len(df)-1, 'Weight of Bare Module (g)'] - df.loc[len(df)-1, 'Weight of Hybrid X (g)'] - df.loc[len(df)-1, 'Weight of Hybrid Y (g)']

        if hybGlue > 0:
            st.write('##### The weight of glue under hybrid is', hybGlue)
            df['Weight of Glue Under Hybrid(s) (g)'] = np.nan
            df.loc[len(df)-1,'Weight of Glue Under Hybrid(s) (g)'] = hybGlue
            df.loc[len(df)-1,"State"] = 'HYB_GLUE_WEIGHED'
            st.success('**Glue under hybrid(s) weighed!:tada:**')

    return df

def pwbGlueWeight(df):

    weigh_tray_pass = False
    sensorTray =  trayNbmNhybNpwb = bmNhybNpwb = pwbGlue = 0

    st.write('##### Weigh the sensor tray')
    sensorTray = st.number_input('Insert weight of sensor tray',key='sensorTray_weight3',value=0.0, step = 0.00001, format='%.5f')
    st.write('The weight of sensor tray is ', sensorTray)
    if sensorTray > 38 and sensorTray < 45 :          ### TODO: hard coded, not good. Better way of protection
        weigh_tray_pass = True

    if weigh_tray_pass:
        st.write('##### Weigh the bare module + hybrid(s) + powerboard + glue + tray')
        trayNbmNhybNpwb = st.number_input('Insert weight of bare module + hybrid(s) + powerboard + glue + tray ',key='trayNbmNhybNpwb_weight',value=0.0, step = 0.00001, format='%.5f')
        st.write('The weight of  bare module + hybrid(s) + powerboard + glue + tray in total is', trayNbmNhybNpwb)
        bmNhybNpwb  = trayNbmNhybNpwb - sensorTray

    if sensorTray > 38 and bmNhybNpwb > 0:          ### TODO: hard coded, not good. Better way of protection
        st.write(' The weight of bare module + hybrid(s) + powerboard + glue is', bmNhybNpwb)

        if 'LS' in df.loc[len(df)-1, 'Local Name']:
            pwbGlue = bmNhybNpwb - df.loc[len(df)-1, 'Weight of Bare Module (g)'] - df.loc[len(df)-1, 'Weight of Hybrid X (g)'] - df.loc[len(df)-1, 'Weight of Glue Under Hybrid(s) (g)'] - df.loc[len(df)-1, 'Weight of Powerboard (g)']
        elif 'SS' in df.loc[len(df)-1, 'Local Name']:
            pwbGlue = bmNhybNpwb - df.loc[len(df)-1, 'Weight of Bare Module (g)'] - df.loc[len(df)-1, 'Weight of Hybrid X (g)'] - df.loc[len(df)-1, 'Weight of Hybrid Y (g)'] - df.loc[len(df)-1, 'Weight of Glue Under Hybrid(s) (g)'] - df.loc[len(df)-1, 'Weight of Powerboard (g)']

        if pwbGlue > 0:
            st.write('##### The weight of glue under powerboard is', pwbGlue)
            df['Weight of Glue Under Powerboard (g)'] = np.nan
            df.loc[len(df)-1, 'Weight of Glue Under Powerboard (g)'] = pwbGlue
            df.loc[len(df)-1,"State"] = 'PWB_GLUE_WEIGHED'
            st.success('**Glue under powerboard weighed!:tada:**')

    return df


def preGlueHybrid(df,pageDict):

    sensor_removed = bare_module_weighed = bare_module_aligned = False

    sensor_removed = removeBareModule(df, pageDict)
    if sensor_removed:
        bare_module_weighed, df = bareModuleWeight(df)

    if bare_module_weighed and sensor_removed:
        st.write('##### Check list:')
        bare_module_aligned  = st.checkbox('Place bare module on module assembly jig & align it')
        
        if bare_module_aligned == True:
            df.loc[len(df)-1,"State"] = 'GLUE_HYB_PREPED'

    return df

def glueHybrid(df):

    check1 = check2 = check3 = check4 = check5 = check6 = check7 = check8 = False

    st.write('##### Check list:')
    check1 = st.checkbox('Check: hybrid stencil, glue scraper and a piece of cleanroom wipper are ready')
    check2 = st.checkbox('⏰ After the 20 minutes countdown, take the mixed glue from the fume hood.')
    check3 = st.checkbox('Add the stencil on top of the hybrid.')
    check4 = st.checkbox('Use the glue scraper to apply the glue')
    check5 = st.checkbox('Carefully lift the stencil & check for air bubbles')
    check6 = st.checkbox('Take the pickup tool and turn it upside down and place it on the bare module')
    check7 = st.checkbox('Add weights that correspond to your pickup tool')
    check8 = st.checkbox('Clean the stencil and the scraper with isopropanol')

    if check1 == check2 == check3 == check4 == check5 == check6 == check7 == check8 == True :
        df.loc[len(df)-1,"State"] = 'HYB_GLUED'

    return df


def preGluePowerBoard(df):

    power_board_aligned= hyb_module_aligned = power_board_on_stand = False

    power_board_aligned = pwbAlign()
    if power_board_aligned:
        st.write('##### Check list:')
        hyb_module_aligned  = st.checkbox('Place hybrid-module on module assembly jig & align hybird-module')
        power_board_on_stand = st.checkbox('Pickup powerboard with pickup tool and place it on the stand & tighten two bolts')
        if hyb_module_aligned == power_board_on_stand == True:
            df.loc[len(df)-1,"State"] = 'GLUE_PWB_PREPED'

    return df

def gluePowerBoard(df):

    check1 = check2 = check3 = check4 = check5 = check6 = check7 = check8 = False

    st.write('##### Check list:')
    check1 = st.checkbox('Check: powerboard stencil, glue scraper and a piece of cleanroom wipper are ready')
    check2 = st.checkbox('⏰ After the 20 minutes countdown, take the mixed glue from the fume hood.')
    check3 = st.checkbox('Add the stencil on top of the powerboard.')
    check4 = st.checkbox('Use the glue scraper to apply the glue')
    check5 = st.checkbox('Carefully lift the stencil & check for air bubbles')
    check6 = st.checkbox('Take the pickup tool and turn it upside down and place it on the module')
    check7 = st.checkbox('Add weights that correspond to your pickup tool')
    check8 = st.checkbox('Clean the stencil and the scraper with isopropanol')

    if check1 == check2 == check3 == check4 == check5 == check6 == check7 == check8 == True :
        df.loc[len(df)-1,"State"] = 'PWB_GLUED'

    return df

def preGlueMixing(df):

    check1 = check2 = check3 = check4 = check5 = False

    st.write('##### Check list:')
    check1 = st.checkbox('Activate the fume hood - ventilation and illumination')
    check2 = st.checkbox('Take the Epoxy Resin and Hardener storage jar out of the fridge')
    check3 = st.checkbox('Make sure you have enough glue boats')
    check4 = st.checkbox('Make sure you have stirring swabs near you')
    check5 = st.checkbox('Turn on the high accuracy balance inside the fume hood')

    if check1 == check2 == check3 == check4 == check5 ==True :
        if df.loc[len(df)-1,"State"] == 'HYB_WEIGHED':
            df.loc[len(df)-1,"State"] = 'HYB_GLUE_MIX_PREPED'
        elif df.loc[len(df)-1,"State"] == 'PWB_WEIGHED':
            df.loc[len(df)-1,"State"] = 'PWB_GLUE_MIX_PREPED'

    return df


def glueMixing(df):

    glue_ratio_pass = stir_done = False
    boat = epoxyAndboat = epoxy = hardener = 0

    st.write('##### Start Mixing!')
    boat = st.number_input('Insert weight of a glue boat',key='boat_weight',value=0.0, step = 0.0001, format='%.4f')
    st.write('The weight of the glue boat is ', boat)
    #

    if boat > 0.5:
        epoxyAndboat = st.number_input('Insert weight of epoxy + glue boat',key='epoxyAndTray_weight',value=0.0, step = 0.0001, format='%.4f')
        st.write('The weight of epoxy + glue boat is', epoxyAndboat)
        epoxy = epoxyAndboat - boat
        if epoxyAndboat > boat:
            st.write('The weight of epoxy is ', epoxy)
        #

    if (epoxy <= 10.1 and epoxy >= 9.9) or (epoxy <= 5.05 and epoxy >= 4.95):
        st.success('✅ Epoxy weight meets the requirement!')
        hardener = st.number_input('Insert weight of hardener',key='hardener_weight',value=0.0, step = 0.0001, format='%.4f')
        st.write('The weight of hardener is', hardener)

        if (epoxy <= 10.1 and epoxy >= 9.9 and hardener <= 0.909 and hardener >= 0.891) or (epoxy <= 5.05 and epoxy >= 4.95 and hardener <= 0.4545 and hardener >= 0.4455):
            st.success('✅ Glue ratio meets the requirement!')
            glue_ratio_pass = True
        elif hardener > 0.0:
            st.warning('❗️ Glue ratio doesn\'t meets the requirement!  Adjust it')
    elif epoxy > 0.0:
        st.warning('❗️ Epoxy weight doesn\'t meet the requirement!  Adjust it')
        
    if glue_ratio_pass:
        st.write('##### Stir the glue with a swab for 5 minutes!')
        if st.checkbox('⏰Start a 5 minutes countdown timer'):
            if st.checkbox('⏰5 minutes is up!'):
                stir_done = True

    if stir_done:
        st.write('##### Let the polaris glue cure for 20 minutes!')
        if st.checkbox('⏰Start a 20 minutes countdown timer'):
            #if st.checkbox('10 seconds is up!'):
            if df.loc[len(df)-1,"State"] == 'HYB_GLUE_MIX_PREPED':
                df.loc[len(df)-1,"State"] = 'HYB_GLUE_MIXED'
            elif df.loc[len(df)-1,"State"] == 'PWB_GLUE_MIX_PREPED':
                df.loc[len(df)-1,"State"] = 'PWB_GLUE_MIXED'

    return df

def assembleModuleChildren(df, client, pageDict):
    hybX_SN = tools.comp_name_to_sn(df.loc[len(df)-1,"Hybrid X Name"], pageDict['inventory_df'])
    if '-SS-' in df.loc[len(df)-1,"Local Name"]:
        hybY_SN = tools.comp_name_to_sn(df.loc[len(df)-1,"Hybrid Y Name"], pageDict['inventory_df'])
    pwb_SN = tools.comp_name_to_sn(df.loc[len(df)-1,"Powerboard Name"], pageDict['inventory_df'])
    pass

def uploadGlueWeight(df, client):
    pass

def uploadVisualInspection(df, client):
    pass

### module assembly operation flow
def moduleAssemblyFlow(filepath, client, pageDict, rework = False):

    module_df = pd.read_pickle(filepath)

    if module_df.loc[len(module_df)-1,"Current Operation"] != 'ASSEMBLY' or rework:
        
        module_df.loc[len(module_df)-1,"Current Local Stage"] = 'HV_TAB_ATTACHED'
        module_df.loc[len(module_df)-1,"Current Operation"] = 'ASSEMBLY'
        module_df.loc[len(module_df)-1,"Current Operator"] = st.session_state['Module Assembly']['uName']
        module_df.loc[len(module_df)-1,"State"] = 'ASSEMBLY_NOT_STARTED_YET'

        module_df.to_pickle(filepath)
        st.experimental_rerun()
    else:
        # flow 
        #------------ooooo00000ooooo------------     ### maybe can by improved by using st.empty()
        # HYB section
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'ASSEMBLY_NOT_STARTED_YET':
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Remove hybrid(s) from the test panel')
            module_df = removeHyb(module_df, pageDict)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done1' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)  ### ugly, but have to do this because it won't read the df again if you don't force it like this, very weird. 
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_REMOVED': 
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Weigh hybrid(s), cut&weigh tabs')
            module_df = hybridWeight(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done2' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()

        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_WEIGHED':
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Prepare for glue mixing')
            module_df = preGlueMixing(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done3' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_GLUE_MIX_PREPED':
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Glue mixing')
            module_df = glueMixing(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done4' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_GLUE_MIXED':
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Prepare for gluing hybrid(s) on sensor')
            module_df = preGlueHybrid(module_df,pageDict)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done5' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'GLUE_HYB_PREPED':
            st.header('Glue Hybrid(s) on Sensor')
            st.subheader('Glue Hybrid(s) on sensor')
            module_df = glueHybrid(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done6' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
            if module_df.loc[len(module_df)-1,"State"] == 'HYB_GLUED':
                st.success('Hybrid glued on sensor!:tada::tada::tada::tada::tada::tada:')
                st.write('##### Wait for 6 hours to let the glue cure...')

        module_df = pd.read_pickle(filepath)                
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_GLUED':
            st.header('Glue Hybrid(s) on Sensor')
            if st.checkbox('6 hours later......'):
                st.subheader('Weigh glue mass under hybrid')
                module_df = hybGlueWeight(module_df)
                st.write('---')
                if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done7' ):
                    module_df.to_pickle(filepath)
                    st.experimental_rerun()

        #------------ooooo00000ooooo------------
        # PWB section
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'HYB_GLUE_WEIGHED':
            st.header('Glue Powerborad on Sensor')
            st.subheader('Remove powerboard from the test panel')
            module_df = removePWB(module_df,pageDict)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done8' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_REMOVED': 
            st.header('Glue Powerborad on Sensor')
            st.subheader('Weigh powerboard')
            module_df = pwbWeight(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done9' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_WEIGHED':
            st.header('Glue Powerborad on Sensor')
            st.subheader('Prepare for glue mixing')
            module_df = preGlueMixing(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done10' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_GLUE_MIX_PREPED':
            st.header('Glue Powerborad on Sensor')
            st.subheader('Glue mixing')
            module_df = glueMixing(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done11' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_GLUE_MIXED':
            st.header('Glue Powerborad on Sensor')
            st.subheader('Prepare for gluing powerboard on sensor')
            module_df = preGluePowerBoard(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done12' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'GLUE_PWB_PREPED':
            st.header('Glue Powerborad on Sensor')
            st.subheader('Glue powerboard on sensor')
            module_df = gluePowerBoard(module_df)
            st.write('---')
            if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done13' ):
                module_df.to_pickle(filepath)
                st.experimental_rerun()
            if module_df.loc[len(module_df)-1,"State"] == 'PWB_GLUED':
                st.success('Powerboard glued on sensor!:tada::tada::tada::tada::tada::tada:')
                st.write('##### Wait for 6 hours to let the glue cure...')

        module_df = pd.read_pickle(filepath)               
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_GLUED':
            st.header('Glue Powerborad on Sensor')
            if st.checkbox('6 hours later......'):
                st.subheader('Weigh glue mass under powerboard')
                module_df = pwbGlueWeight(module_df)
                st.write('---')
                if st.button('❗️ CONFIRM: current step done', key = module_df.loc[len(module_df)-1,"State"]+'_done14' ):
                    module_df.to_pickle(filepath)
                    st.experimental_rerun()
        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'PWB_GLUE_WEIGHED':
            st.header('Module Assembly Done Confirmation')
            if st.button('❗️ CONFIRM: module assembly done!'):
                module_df.loc[len(module_df)-1,"State"] = 'ASSEMBLY_DONE'
                module_df.to_pickle(filepath)
                st.balloons()
                time.sleep(3)
                st.experimental_rerun()

        
        module_df = pd.read_pickle(filepath)
        if module_df.loc[len(module_df)-1,"State"] == 'ASSEMBLY_DONE':
            module_df.loc[0,"Current Local Stage"] = 'GLUED'
            success_str = '#### ' + module_df.loc[len(module_df)-1,'Local Name'] + ' --- Module Assembly Done! :tada::tada::tada::tada::tada::tada:'
            st.success(success_str)
            module_df.to_pickle(filepath)
            # st.experimental_rerun()

    return module_df


#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Module Assembly", ":gear: Module Assembly", infoList)

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
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) ]  ### & (inv_df['Local Type'].str.contains("PPA") | inv_df['Local Type'].str.contains("PPB"))
        else:
            client='DUMMY'
            pageDict['uName'] = st.session_state.Homepage['user']
            df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) & (inv_df['Local Type'].str.contains("DUMMY"))]

        ### get sub_dataframe which contains entries that belong to this page and logged in user (to enable access control)
        module_asm_u_df = df_havNextOp[df_havNextOp['Local Name'].str.contains('-Module-') & (df_havNextOp['Next Operation'] == 'ASSEMBLY') & (df_havNextOp['Next Operator'] == pageDict['uName'])]
        ### 
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)

        if not module_asm_u_df.empty :
            task_selector = st.empty()
            with task_selector.container():
                module_local_name = st.selectbox('Please select the module you want to work on', selectbox_init_v_tpl + tuple(module_asm_u_df['Local Name'].tolist()))
                
            rework = False

            if module_local_name != selectbox_init_v and st.checkbox('Check to start!'):
                task_selector.empty()
                module_asm_u_df.set_index('Local Name', inplace=True)
                module_sub_table_file_path = module_asm_u_df.loc[module_local_name,'Sub-table Path']
                module_local_alias = module_asm_u_df.loc[module_local_name,'Local Alias']
                module_atlas_sn = module_asm_u_df.loc[module_local_name,'ATLAS SN']
                    
                st.info('###### Now working on: '+module_local_name + ' (' + module_atlas_sn +', '+ module_local_alias + ') ')

                with st.expander('Expand to show the REWORK button'):
                    rework = st.button('REWORK (start from scratch) ❗️')

                df_this_module = moduleAssemblyFlow(module_sub_table_file_path, client, pageDict, rework)

                if df_this_module['Current Local Stage'].tolist()[-1] == 'GLUED':
                    this_module_idx = inv_df['Local Name'].tolist().index(module_local_name)   ### TODO: modify the local stage of corresponding hybrid and powerboard in inventory
                    inv_df.loc[this_module_idx,'Current Local Stage'] = 'GLUED'
                    inv_df.loc[this_module_idx,'Current Operator'] = pageDict['uName']
                    inv_df.loc[this_module_idx,'Next Operation'] = np.nan
                    inv_df.loc[this_module_idx,'Next Operator'] = np.nan
                    inv_df.loc[this_module_idx,'Next Operation DDL'] = np.nan
                    inv_df.to_pickle(inventory)

                    hybX_name = df_this_module.loc[len(df_this_module)-1,"Hybrid X Name"]
                    pwb_name = df_this_module.loc[len(df_this_module)-1,"Powerboard Name"]
                    bm_name = df_this_module.loc[len(df_this_module)-1, 'Bare Module Name']

                    inv_df = tools.modifyComponentStagebyName(hybX_name , "ON_MODULE", pageDict['uName'], inv_df)
                    inv_df = tools.modifyComponentStagebyName(pwb_name , "ON_MODULE", pageDict['uName'], inv_df)
                    inv_df = tools.modifyComponentStagebyName(bm_name , "ON_MODULE", pageDict['uName'], inv_df)

                    if '-SS-' in df_this_module.loc[len(df_this_module)-1,"Local Name"]:
                        hybY_name = df_this_module.loc[len(df_this_module)-1,"Hybrid Y Name"]
                        inv_df = tools.modifyComponentStagebyName(hybY_name , "ON_MODULE", pageDict['uName'], inv_df)

                st.write('---')
                st.write('#### Current Module Info:')
                st.dataframe(df_this_module)

