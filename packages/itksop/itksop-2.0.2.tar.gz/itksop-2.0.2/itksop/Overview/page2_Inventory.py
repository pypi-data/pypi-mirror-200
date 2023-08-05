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
#####################
### main part
#####################

class Page2(Page):
    def __init__(self):
        super().__init__("Inventory", ":card_file_box: Inventory", infoList)

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

        ### TODO?: Access control or not? only ihep users?
        ### get inventory file
        inventory = os.path.join(tools.DATA_PATH, 'inventory.pkl')
        inv_df = tools.get_inventory(inventory)  

        ### display number of parts
        st.header(':bar_chart: Inventory Statistics')
        st.subheader('Unused Parts Counts')     
        
        tab_ppa, tab_ppb, tab_dummy = st.tabs(["PPA", "PPB", "DUMMY"])

        with tab_ppa:
            st.write('##### Module related')
            col_hx_ppa_u, col_hy_ppa_u, col_pb_ppa_u, col_bm_ls_u, col_bm_ss_u = st.columns(5)

            #TODO: recommanded to use df.query instead
            col_hx_ppa_u.metric('Hybrid X PPA',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-PPA') & (inv_df['Current Local Stage']=='READY') ]))
            col_hy_ppa_u.metric('Hybrid Y PPA',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-PPA') & (inv_df['Current Local Stage']=='READY') ]))
            col_pb_ppa_u.metric('Powerboard PPA',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-PPA') & (inv_df['Current Local Stage']=='READY') ]))
            col_bm_ls_u.metric('Bare Module LS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-PP') & (inv_df['Current Local Stage']=='READY') ]  )) 
            col_bm_ss_u.metric('Bare Module SS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-PP') & (inv_df['Current Local Stage']=='READY') ]  )) 
            
            st.write('##### Hybrid related')
            col_hfx_ppa_u, col_hfy_ppa_u, col_abc_v1_u, col_hcc_v0_u = st.columns(4)

            col_hfx_ppa_u.metric('Hybrid Flex X PPA',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-PPA') & (inv_df['Current Local Stage']=='READY') ]))
            col_hfy_ppa_u.metric('Hybrid Flex Y PPA',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-PPA') & (inv_df['Current Local Stage']=='READY') ]))
            col_abc_v1_u.metric('ABCStar V1',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-V1') & (inv_df['Current Local Stage']=='READY') ]))
            col_hcc_v0_u.metric('HCCStar V0',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-V0') & (inv_df['Current Local Stage']=='READY') ]))

            with st.expander('Show all parts counts'):
                st.subheader('All Parts Counts')
                st.write('##### Module related')
                col_m_ls_ppa, col_m_ss_ppa, col_hx_ppa, col_hy_ppa, col_pb_ppa, col_bm_ls, col_bm_ss = st.columns(7)

                col_m_ls_ppa.metric('Module LS PPA',len(inv_df[ inv_df['Local Type'] == 'Module-LS-PPA' ]))
                col_m_ss_ppa.metric('Module SS PPA',len(inv_df[ inv_df['Local Type'] == 'Module-SS-PPA' ]))
                col_hx_ppa.metric('Hybrid X PPA',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-PPA') ]))
                col_hy_ppa.metric('Hybrid Y PPA',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-PPA') ]))
                col_pb_ppa.metric('Powerboard PPA',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-PPA') ]))
                col_bm_ls.metric('Bare Module LS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-PP')]  ))
                col_bm_ss.metric('Bare Module SS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-PP')]  ))
                
                st.write('##### Hybrid related')
                col_hfx_ppa, col_hfy_ppa, col_abc_v1, col_hcc_v0 = st.columns(4)

                col_hfx_ppa.metric('Hybrid Flex X PPA',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-PPA') ]))
                col_hfy_ppa.metric('Hybrid Flex Y PPA',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-PPA') ]))
                col_abc_v1.metric('ABCStar V1',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-V1') ]))
                col_hcc_v0.metric('HCCStar V0',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-V0') ]))


        with tab_ppb:
            st.write('##### Module related')
            col_hx_ppb_u, col_hy_ppb_u, col_pb_ppb_u, col_bm_ls_u, col_bm_ss_u = st.columns(5)

            #TODO: recommanded to use df.query instead
            col_hx_ppb_u.metric('Hybrid X PPB',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-PPB') & (inv_df['Current Local Stage']=='READY') ]))
            col_hy_ppb_u.metric('Hybrid Y PPB',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-PPB') & (inv_df['Current Local Stage']=='READY') ]))
            col_pb_ppb_u.metric('Powerboard PPB',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-PPB') & (inv_df['Current Local Stage']=='READY') ]))
            col_bm_ls_u.metric('Bare Module LS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-PP') & (inv_df['Current Local Stage']=='READY') ]  )) 
            col_bm_ss_u.metric('Bare Module SS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-PP') & (inv_df['Current Local Stage']=='READY') ]  )) 
            
            st.write('##### Hybrid related')
            col_hfx_ppb_u, col_hfy_ppb_u, col_abc_v1_u, col_hcc_v1_u = st.columns(4)

            col_hfx_ppb_u.metric('Hybrid Flex X PPB',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-PPB') & (inv_df['Current Local Stage']=='READY') ]))
            col_hfy_ppb_u.metric('Hybrid Flex Y PPB',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-PPB') & (inv_df['Current Local Stage']=='READY') ]))
            col_abc_v1_u.metric('ABCStar V1',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-V1') & (inv_df['Current Local Stage']=='READY') ]))
            col_hcc_v1_u.metric('HCCStar V1',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-V1') & (inv_df['Current Local Stage']=='READY') ]))

            with st.expander('Show all parts counts'):
                st.subheader('All Parts Counts')
                st.write('##### Module related')
                col_m_ls_ppb, col_m_ss_ppb, col_hx_ppb, col_hy_ppb, col_pb_ppb, col_bm_ls, col_bm_ss = st.columns(7)

                col_m_ls_ppb.metric('Module LS PPB',len(inv_df[ inv_df['Local Type'] == 'Module-LS-PPB' ]))
                col_m_ss_ppb.metric('Module SS PPB',len(inv_df[ inv_df['Local Type'] == 'Module-SS-PPB' ]))
                col_hx_ppb.metric('Hybrid X PPB',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-PPB') ]))
                col_hy_ppb.metric('Hybrid Y PPB',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-PPB') ]))
                col_pb_ppb.metric('Powerboard PPB',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-PPB') ]))
                col_bm_ls.metric('Bare Module LS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-PP')]  ))
                col_bm_ss.metric('Bare Module SS PP',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-PP')]  ))
                
                st.write('##### Hybrid related')
                col_hfx_ppb, col_hfy_ppb, col_abc_v1, col_hcc_v1 = st.columns(4)

                col_hfx_ppb.metric('Hybrid Flex X PPB',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-PPB') ]))
                col_hfy_ppb.metric('Hybrid Flex Y PPB',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-PPB') ]))
                col_abc_v1.metric('ABCStar V1',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-V1') ]))
                col_hcc_v1.metric('HCCStar V1',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-V1') ]))

        with tab_dummy:
            st.write('##### Module related')
            col_hx_dummy_u, col_hy_dummy_u, col_pb_dummy_u, col_bm_ls_dummy_u, col_bm_ss_dummy_u = st.columns(5)

            #TODO: recommanded to use df.query instead
            col_hx_dummy_u.metric('Hybrid X DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_hy_dummy_u.metric('Hybrid Y DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_pb_dummy_u.metric('Powerboard DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_bm_ls_dummy_u.metric('Bare Module LS DUMMY',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-DUMMY') & (inv_df['Current Local Stage']=='READY') ]  )) 
            col_bm_ss_dummy_u.metric('Bare Module SS DUMMY',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-DUMMY') & (inv_df['Current Local Stage']=='READY') ]  )) 
            
            st.write('##### Hybrid related')
            col_hfx_dummy_u, col_hfy_dummy_u, col_abc_dummy_u, col_hcc_dummy_u = st.columns(4)

            col_hfx_dummy_u.metric('Hybrid Flex X DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_hfy_dummy_u.metric('Hybrid Flex Y DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_abc_dummy_u.metric('ABCStar DUMMY',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))
            col_hcc_dummy_u.metric('HCCStar DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-DUMMY') & (inv_df['Current Local Stage']=='READY') ]))

            with st.expander('Show all parts counts'):
                st.subheader('All Parts Counts')
                st.write('##### Module related')
                col_m_ls_dummy, col_m_ss_dummy, col_hx_dummy, col_hy_dummy, col_pb_dummy, col_bm_ls_dummy, col_bm_ss_dummy = st.columns(7)

                col_m_ls_dummy.metric('Module LS DUMMY',len(inv_df[ inv_df['Local Type'] == 'Module-LS-DUMMY' ]))
                col_m_ss_dummy.metric('Module SS DUMMY',len(inv_df[ inv_df['Local Type'] == 'Module-SS-DUMMY' ]))
                col_hx_dummy.metric('Hybrid X DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-X-DUMMY') ]))
                col_hy_dummy.metric('Hybrid Y DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Hybrid-Y-DUMMY') ]))
                col_pb_dummy.metric('Powerboard DUMMY',len(inv_df[inv_df['Local Type'].str.contains('Powerboard-DUMMY') ]))
                col_bm_ls_dummy.metric('Bare Module LS DUMMY',len(inv_df[inv_df['Local Type'].str.contains('BareModule-LS-DUMMY')]  ))
                col_bm_ss_dummy.metric('Bare Module SS DUMMY',len(inv_df[inv_df['Local Type'].str.contains('BareModule-SS-DUMMY')]  ))
                
                st.write('##### Hybrid related')
                col_hfx_dummy, col_hfy_dummy, col_abc_dummy, col_hcc_dummy = st.columns(4)

                col_hfx_dummy.metric('Hybrid Flex X DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-X-DUMMY') ]))
                col_hfy_dummy.metric('Hybrid Flex Y DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HybridFlex-Y-DUMMY') ]))
                col_abc_dummy.metric('ABCStar DUMMY',len(inv_df[inv_df['Local Type'].str.contains('ABCStar-DUMMY') ]))
                col_hcc_dummy.metric('HCCStar DUMMY',len(inv_df[inv_df['Local Type'].str.contains('HCCStar-DUMMY') ]))

        st.write('---')

        st.header(':card_index_dividers: Inventory by Types')
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Modules", "Hybrids", "Powerboards", "Bare Modules", "Hybrid Flexes", "ABCStar Chips", "HCCStar Chips"])

        ### display inventory table by type
        with tab1:
            st.subheader('Modules')

            module_df = inv_df[inv_df['Local Name'].str.contains('-Module-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            module_df.index = module_df.index+1 # reset index in a more user friendly way
            st.dataframe(module_df,use_container_width=True)  

        with tab2:
            st.subheader('Hybrids')

            hybrid_df = inv_df[inv_df['Local Name'].str.contains('-Hybrid-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)  ### 'Hybrid-' to avoid selecting hybridflexes
            hybrid_df.index = hybrid_df.index+1
            st.dataframe(hybrid_df,use_container_width = True) 

        with tab3:
            st.subheader('Powerboards')

            pb_df = inv_df[inv_df['Local Name'].str.contains('-Powerboard-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            pb_df.index = pb_df.index+1
            st.dataframe(pb_df,use_container_width = True) 

        with tab4:
            st.subheader('Bare Modules')

            baremodule_df = inv_df[inv_df['Local Name'].str.contains('-BareModule-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            baremodule_df.index = baremodule_df.index+1
            st.dataframe(baremodule_df,use_container_width = True) 

        with tab5:
            st.subheader('Hybrid Flexes')

            hybflex_df = inv_df[inv_df['Local Name'].str.contains('-HybridFlex-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            hybflex_df.index = hybflex_df.index+1
            st.dataframe(hybflex_df, use_container_width = True) 

        with tab6:
            st.subheader('ABCStar Chips')

            abcs_df = inv_df[inv_df['Local Name'].str.contains('-ABCStar-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            abcs_df.index = abcs_df.index+1
            st.dataframe(abcs_df, use_container_width = True) 

        with tab7:
            st.subheader('HCCStar Chips')

            hccs_df = inv_df[inv_df['Local Name'].str.contains('-HCCStar-')].loc[:,'Local Name':'Next Operation DDL'].reset_index(drop=True)
            hccs_df.index = hccs_df.index+1
            st.dataframe(hccs_df, use_container_width = True) 


        st.write('---')
        
        selectbox_init_v = '<CHOOSE A VALUE>'
        selectbox_init_v_tpl = (selectbox_init_v,)
        
        # tooooooooo ugly down below need to be improved! Kill ifs !
        high_auth = False
        if not st.session_state.dummy:
            if st.session_state.Homepage['user']['userIdentity'] in tools.IHEP_ADMIN_ID :
                high_auth = True
        else:
            if st.session_state.Homepage['user'] in tools.IHEP_ADMIN_NAME:
                high_auth = True

        if high_auth :  #Only admin have access to this section
            st.header('🧮 Task Assignment')
            tab_module, tab_hyb, tab_ship = st.tabs(['Module Task', 'Hybrid Task', 'Shipment Task']) 
            with tab_module:
                pageDict['module_type'] = st.selectbox( "Please select type of module", selectbox_init_v_tpl +tools.MODULE_TYPES )       ###TODO: no reason for using pageDict，make it simple
                pageDict['module_version'] = st.selectbox("Please select version of module", selectbox_init_v_tpl +tools.MODULE_VERSIONS)
                if pageDict['module_type'] != selectbox_init_v and  pageDict['module_version'] != selectbox_init_v :
                    num_of_choosed_modules = len( module_df[ module_df['Local Type'].str.contains(pageDict['module_version']) & module_df['Local Type'].str.contains(pageDict['module_type']) ])
                    new_module_number = num_of_choosed_modules+1
                    module_number_list = list(range(1,new_module_number+1))
                    pageDict['module_num'] = st.selectbox( "Please select module number", selectbox_init_v_tpl +tuple([str(x) for x in module_number_list]))
                    if pageDict['module_num'] != selectbox_init_v:
                        pageDict['module_name'] = 'IHEP-Module-' + pageDict['module_type'] + '-' + pageDict['module_version'] + '-' + pageDict['module_num']
                        # New module and exisiting modules have different options
                        if int(pageDict['module_num']) != new_module_number :
                            st.info('###### Now working on the task assignment of ' + pageDict['module_name'] )
                            st.dataframe(module_df[module_df['Local Name'] == pageDict['module_name']] )
                            module_next_operation = st.selectbox( "Please select the next operation", selectbox_init_v_tpl + tools.MODULE_NEXT_OPERATIONS)
                            if module_next_operation != selectbox_init_v:
                                module_next_operator = st.selectbox( "Please select the next operator", selectbox_init_v_tpl + tools.MODULE_NEXT_OPERATORS[module_next_operation] )
                                module_next_operation_DDL = st.date_input("Please select the deadline for the next operation")
                                module_invetory_idx =  inv_df[inv_df['Local Name'] == pageDict['module_name']].index[0]
                                if st.checkbox('I\'ve confirmed that all the values I entered are correct.') and module_next_operator != selectbox_init_v:
                                    if st.button('Assign task!'):
                                        inv_df.loc[module_invetory_idx, 'Next Operation'] = module_next_operation
                                        inv_df.loc[module_invetory_idx, 'Next Operator'] = module_next_operator
                                        inv_df.loc[module_invetory_idx, 'Next Operation DDL'] = module_next_operation_DDL
                                        with st.spinner('Assigning Task...'):
                                            inv_df.to_pickle(inventory)
                                            time.sleep(1)
                                        st.experimental_rerun()                                     # EXPERIMENTAL METHOD: might change & cause an error due to upgrade of streamlit
                        else:
                            st.info('###### Now working on the task assignment of ' + pageDict['module_name'] + ' (a new module)' )
                            time.sleep(1)
                            module_next_operation = st.selectbox( "Please select the next operation (only one option is available for a new module )", selectbox_init_v_tpl + tuple([tools.MODULE_NEXT_OPERATIONS[0]]))
                            if module_next_operation != selectbox_init_v:
                                module_next_operator = st.selectbox( "Please select the next operator", selectbox_init_v_tpl + tools.MODULE_NEXT_OPERATORS[module_next_operation] )
                                module_next_operation_DDL = st.date_input("Please select the deadline for the next operation")
                                ### get available bare module and select one
                                module_ava_bm_name_list = baremodule_df[(baremodule_df['Current Local Stage']=='READY') & (baremodule_df['Local Type'].str.contains(pageDict['module_type'])) & (baremodule_df['Local Type'].str.contains(pageDict['module_version']))].loc[:, 'Local Name'].tolist()                                    #TODO: show alias of the component at the same time
                                # module_ava_bm_alias_list = [inv_df.set_index('Local Name').loc[name, 'Local Alias'] for name in module_ava_bm_name_list]
                                # module_ava_bm_list = [ (name+' ('+alias+') ') for name,alias in zip(module_ava_bm_name_list, module_ava_bm_alias_list) ]
                                module_bm_name = st.selectbox( "Please select the bare module that the operator should use", selectbox_init_v_tpl + tuple(module_ava_bm_name_list) )
                                ### get available hybrid X and select one, TODO:criteria need to be modified
                                module_ava_hybX_list = hybrid_df[(hybrid_df['Current Local Stage']=='E-TESTED') & (hybrid_df['Local Type'].str.contains('X')) & (hybrid_df['Local Type'].str.contains(pageDict['module_version']))].loc[:, 'Local Name'].tolist()
                                module_hybX_name = st.selectbox( "Please select the hybrid X that the operator should use", selectbox_init_v_tpl + tuple(module_ava_hybX_list) )    
                                ### set hybrid Y name by module_type
                                module_hybY_name = np.nan  ### TODO:can bre reomved
                                if pageDict['module_type'] == 'SS':
                                    ### get available hybrid Y and select one, TODO:criteria need to be modified
                                    module_ava_hybY_list = hybrid_df[(hybrid_df['Current Local Stage']=='E-TESTED') & (hybrid_df['Local Type'].str.contains('Y')) & (hybrid_df['Local Type'].str.contains(pageDict['module_version']))].loc[:, 'Local Name'].tolist()
                                    module_hybY_name = st.selectbox( "Please select the hybrid Y that the operator should use", selectbox_init_v_tpl + tuple(module_ava_hybY_list) )
                                ### get available powerboards and select one
                                module_ava_pb_list = pb_df[(pb_df['Current Local Stage']=='READY') & (pb_df['Local Type'].str.contains(pageDict['module_version']))].loc[:, 'Local Name'].tolist()
                                module_pb_name = st.selectbox( "Please select the powerboard that the operator should use", selectbox_init_v_tpl + tuple(module_ava_pb_list) )
                                ### a bool variable to show if every option is selected
                                all_selected = all( v != selectbox_init_v for v in (module_next_operator, module_bm_name, module_hybX_name, module_hybY_name, module_pb_name))
                                if all_selected:
                                    module_bm_inv_idx = inv_df['Local Name'].tolist().index(module_bm_name)

                                    module_sub_table_file_name = pageDict['module_name']+".pkl"
                                    module_sub_table_file_dir = os.path.join(tools.MODULE_DATA_PATH, pageDict['module_name'])
                                    tools.mkdirs(module_sub_table_file_dir)
                                    module_sub_table_file_path = os.path.join(module_sub_table_file_dir, module_sub_table_file_name)
                                    module_sub_df = pd.DataFrame(  {'Local Name': [pageDict['module_name']],
                                                            'ATLAS SN': [inv_df.loc[module_bm_inv_idx,'ATLAS SN']],  ### just take the property of bare module, because bare module IS the module in ITkDB
                                                            'Local Alias': [inv_df.loc[module_bm_inv_idx,'Local Alias']],  ### just take the property of bare module, because bare module IS the module in ITkDB
                                                            'Current Local Stage': ['HV_TAB_ATTACHED'],
                                                            'Current Operation' : [np.nan],
                                                            'Current Operator' : [np.nan],
                                                            'State': ['ASSEMBLY_NOT_STARTED_YET'],
                                                            'Bare Module Name' : [module_bm_name],
                                                            'Hybrid X Name': [module_hybX_name],
                                                            'Powerboard Name': [module_pb_name]
                                                            } )
                                    if pageDict['module_type'] == 'SS':
                                        module_sub_df.insert(7,'Hybrid Y Name', module_hybY_name)

                                    df_tmp_m = pd.DataFrame({ 'Local Name': [pageDict['module_name']],
                                                            'ATLAS SN': [inv_df.loc[module_bm_inv_idx,'ATLAS SN']], ### just take the property of bare module, because bare module IS the module in ITkDB
                                                            'Local Alias': [inv_df.loc[module_bm_inv_idx,'Local Alias']], ### just take the property of bare module, because bare module IS the module in ITkDB
                                                            'Local Type': [ 'Module-'+pageDict['module_type']+'-'+pageDict['module_version'] ],
                                                            'Current Local Stage': ['HV_TAB_ATTACHED'],
                                                            'Current Operator' : [np.nan],
                                                            'Next Operation': [module_next_operation],
                                                            'Next Operator' : [module_next_operator],
                                                            'Next Operation DDL': [module_next_operation_DDL],
                                                            'Sub-table Path': [module_sub_table_file_path]
                                                        })
                                    st.dataframe(df_tmp_m)
                                    if st.checkbox('I\'ve confirmed that all the values I entered are correct.'):
                                        if st.button('Assign task!'):
                                            with st.spinner('Assigning Task...'):
                                                inv_df = inv_df.append(df_tmp_m, ignore_index=True)              # pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here
                                                module_sub_df.to_pickle(module_sub_table_file_path)
                                                inv_df.to_pickle(inventory)                                      ### TODO: modify the next ops of corresponding bare module, hybrid and powerboard in inventory
                                                time.sleep(1)
                                            st.experimental_rerun()                                     # EXPERIMENTAL METHOD: might change & cause an error due to upgrade of streamlit
                                    
            with tab_hyb:
                hybrid_type = st.selectbox( "Please select type of hybrid", selectbox_init_v_tpl +tools.HYBRID_TYPES )
                hybrid_version = st.selectbox("Please select version of hybrid", selectbox_init_v_tpl +tools.HYBRID_VERSIONS)
                if hybrid_type != selectbox_init_v and hybrid_version != selectbox_init_v :
                    num_of_choosed_hybrids = len( hybrid_df[hybrid_df['Local Type'].str.contains(hybrid_version) & hybrid_df['Local Type'].str.contains(hybrid_type) ])
                    new_hybrid_number = num_of_choosed_hybrids+1
                    hybrid_number_list = list(range(1,new_hybrid_number+1))
                    hybrid_num = st.selectbox( "Please select hybrid number", selectbox_init_v_tpl +tuple([str(x) for x in hybrid_number_list]))
                    if hybrid_num != selectbox_init_v:
                        hybrid_name = 'IHEP-Hybrid-' + hybrid_type + '-' + hybrid_version + '-' + hybrid_num
                        # New hybrids and exisiting hybrids have different options
                        if int(hybrid_num) != new_hybrid_number :
                            st.info('###### Now working on the task assignment of ' +hybrid_name )
                            st.dataframe(hybrid_df[hybrid_df['Local Name'] == hybrid_name] )
                            hybrid_next_operation = st.selectbox( "Please select the next operation", selectbox_init_v_tpl + tools.HYBRID_NEXT_OPERATIONS)
                            if hybrid_next_operation != selectbox_init_v:
                                hybrid_next_operator = st.selectbox( "Please select the next operator", selectbox_init_v_tpl + tools.HYBRID_NEXT_OPERATORS[hybrid_next_operation] )
                                hybrid_next_operation_DDL = st.date_input("Please select the deadline for the next operation")
                                hybrid_invetory_idx =  inv_df[inv_df['Local Name'] == hybrid_name ].index[0]
                                if st.checkbox('I\'ve confirmed that all the values I entered are correct.') and hybrid_next_operator != selectbox_init_v:
                                    if st.button('Assign task!'):
                                        inv_df.loc[hybrid_invetory_idx, 'Next Operation'] = hybrid_next_operation
                                        inv_df.loc[hybrid_invetory_idx, 'Next Operator'] = hybrid_next_operator
                                        inv_df.loc[hybrid_invetory_idx, 'Next Operation DDL'] = hybrid_next_operation_DDL
                                        with st.spinner('Assigning Task...'):
                                            inv_df.to_pickle(inventory)
                                            time.sleep(1)
                                        st.experimental_rerun()                                     # EXPERIMENTAL METHOD: might change & cause an error due to upgrade of streamlit
                        else:
                            st.info('###### Now working on the task assignment of ' + hybrid_name + ' (a new hybrid)' )
                            hybrid_next_operation = st.selectbox( "Please select the next operation (only one option is available for a new hybrid )", selectbox_init_v_tpl + tuple([tools.HYBRID_NEXT_OPERATIONS[0]]))
                            if hybrid_next_operation != selectbox_init_v:
                                hybrid_next_operator = st.selectbox( "Please select the next operator", selectbox_init_v_tpl + tools.HYBRID_NEXT_OPERATORS[hybrid_next_operation] )
                                hybrid_next_operation_DDL = st.date_input("Please select the deadline for the next operation")
                                ### get available flex and select one
                                hybrid_ava_flex_list = hybflex_df[(hybflex_df['Current Local Stage']=='READY') & hybflex_df['Local Type'].str.contains(hybrid_type) & hybflex_df['Local Type'].str.contains(hybrid_version) ].loc[:, 'Local Name'].tolist()  #TODO: show alias of the component at the same time
                                hybrid_flex_name = st.selectbox( "Please select the hybrid flex that the operator should use", selectbox_init_v_tpl + tuple(hybrid_ava_flex_list) )
                                if hybrid_flex_name != selectbox_init_v:
                                    hybrid_flex_inv_idx = inv_df['Local Name'].tolist().index(hybrid_flex_name)

                                    hybrid_sub_table_file_name = hybrid_name+".pkl"
                                    hybrid_sub_table_file_dir = os.path.join(tools.HYBRID_DATA_PATH, hybrid_name)
                                    tools.mkdirs(hybrid_sub_table_file_dir)
                                    hybrid_sub_table_file_path = os.path.join(hybrid_sub_table_file_dir, hybrid_sub_table_file_name)
                                    hybrid_sub_df = pd.DataFrame(  {'Local Name': [hybrid_name],
                                                            'ATLAS SN': [np.nan],  
                                                            'Local Alias': [inv_df.loc[hybrid_flex_inv_idx,'Local Alias']],  ### just take the local alias of flex
                                                            'Current Local Stage': [np.nan],
                                                            'Current Operation' : [np.nan],
                                                            'Current Operator' : [np.nan],
                                                            'State': ['ASSEMBLY_NOT_STARTED_YET'],
                                                            'Hybrid Flex Name': [hybrid_flex_name],
                                                            'ATLAS SN of Hybrid Flex': [inv_df.loc[hybrid_flex_inv_idx,'ATLAS SN']]
                                                            } )

                                    df_tmp_h = pd.DataFrame({ 'Local Name': [ hybrid_name ],
                                                            'ATLAS SN': [np.nan], ### just take the property of bare module, because bare module IS the module in ITkDB
                                                            'Local Alias': [inv_df.loc[hybrid_flex_inv_idx,'Local Alias']],  ### just take the local alias of flex
                                                            'Local Type': [ 'Hybrid-'+hybrid_type+'-'+hybrid_version ],
                                                            'Current Local Stage': [np.nan],
                                                            'Current Operator' : [np.nan],
                                                            'Next Operation': [hybrid_next_operation],
                                                            'Next Operator' : [hybrid_next_operator],
                                                            'Next Operation DDL': [hybrid_next_operation_DDL],
                                                            'Sub-table Path': [hybrid_sub_table_file_path]
                                                        })
                                    st.dataframe(df_tmp_h)
                                    if st.checkbox('I\'ve confirmed that all the values I entered are correct.'):
                                        if st.button('Assign task!'):
                                            with st.spinner('Assigning Task...'):
                                                inv_df = inv_df.append(df_tmp_h, ignore_index=True)              # pandas.DataFrame.append deprecated since pandas version 1.4.0 --- need to be improved here
                                                hybrid_sub_df.to_pickle(hybrid_sub_table_file_path)
                                                inv_df.to_pickle(inventory)                                      ### TODO: modify the next ops of corresponding bm, hybrid and powerboard in inventory
                                                time.sleep(1)
                                            st.experimental_rerun()                                     # EXPERIMENTAL METHOD: might change & cause an error due to upgrade of streamlit
                                    
            with tab_ship:
                pass

            st.write('---')

            ### show total inventory
            st.header(':card_file_box: Total Inventory')
            with st.expander("Expand to show the total inventory ..."):
                st.dataframe(inv_df)

            # with st.expander("Update the inventory ..."):
            #     tools.upload_inventory(inventory)
