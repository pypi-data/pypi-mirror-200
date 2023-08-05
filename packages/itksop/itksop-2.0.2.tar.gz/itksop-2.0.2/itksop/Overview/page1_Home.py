### based on https://gitlab.cern.ch/wraight/itk_pdb_testapp/-/blob/master/corePages/pageA.py
### standard
import streamlit as st
from core.Page import Page
### custom
import datetime
import os
import sys
import json
import pandas as pd
import numpy as np
### PDB stuff
import itkdb
import core.tools as tools
import core.DBaccess as DBaccess
import core.stInfrastructure as infra

#####################
### Top page
#####################

### format datetime
def DateFormat(dt):
    return str("{0:04}-{1:02}-{2:02}".format(dt.year,dt.month,dt.day))+" @ "+str("{0:02}:{1:02}".format(dt.hour,dt.minute))


def GetCodes(args):
    code1,code2=None,None
    for a in args:
        if "ac1" in a: code1=a[4::].strip('"').strip("'")
        if "ac2" in a: code2=a[4::].strip('"').strip("'")
    return code1,code2

def Bulletin(inv_df, dummy):
    st.header(':pushpin: Bulletin Board')
    placeholder=st.empty()
    placeholder.info('Nothing here...')
    df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) ]
    if dummy:
        df_havNextOp = inv_df[(inv_df['Next Operator'].notnull()) & (inv_df['Next Operation'].notnull()) & (inv_df['Local Type'].str.contains("DUMMY"))]
    if not df_havNextOp.empty:
        with placeholder.container():
            for idx, row in df_havNextOp.iterrows():
                if pd.isna(row['Local Alias']):
                    if type(row['Next Operator'])==str:
                        st.info('###### '+str(row['Next Operator']) + ', please work on ' + str(row['Next Operation']) + ' of ' + str(row['Local Name']) + ' and finish before ' + str(row['Next Operation DDL']) )
                    else:
                        st.info('###### '+str(', '.join(row['Next Operator'])) + ', please work on ' + str(row['Next Operation']) + ' of ' + str(row['Local Name']) + ' and finish before ' + str(row['Next Operation DDL']))
                else:
                    if type(row['Next Operator'])==str :
                        st.info('###### '+str(row['Next Operator'])+', please work on '+str(row['Next Operation'])+' of '+str(row['Local Name']) + ' (' + str(row['Local Alias']) + ') ' + ' and finish before '+ str(row['Next Operation DDL']))
                    else:
                        st.info('###### '+str(', '.join(row['Next Operator']))+', please work on '+str(row['Next Operation'])+' of '+str(row['Local Name']) + ' (' + str(row['Local Alias']) + ') ' + ' and finish before '+ str(row['Next Operation DDL']))


#####################
### main part
#####################

class Page1(Page):
    def __init__(self):
        super().__init__("Homepage", ":house_with_garden: Homepage", ['nothing to report'])

    def main(self):
        super().main()

        ### getting attribute
        pageDict=st.session_state[self.name]

        ### get inventory data
        inventory = os.path.join(tools.DATA_PATH, 'inventory.pkl')

        inv_df = tools.get_inventory(inventory)  
        # pageDict['dfInventory'] = inv_df
        
        ### Bulletin
        Bulletin(inv_df, st.session_state.dummy)
        st.write('---')

        ### Authentication
        st.header(':ticket: Get Your Ticket!')

        nowTime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))) #UTC+8 Beijing Time
        st.write("### :calendar: "+DateFormat(nowTime))

        # token check
        # try:
        #     if pageDict['token']:
        #         st.write(":white_check_mark: Got Token")
        #     else:
        #         st.write("No user found")
        # except KeyError:
        #     st.write("No user state set form commandline")

        # if st.session_state.debug: st.write("sys args:",sys.argv)
        # if len(sys.argv)>1:
        #     ac1,ac2=GetCodes(sys.argv)
        #     st.info("Read codes from commandLine")
        #     #st.write(ac1,",",ac2)
        #     if ac1==None or ac2==None:
        #         st.error("Problem recognising credentials. Please check arguments and try again.")
        #     else:
        #         pageDict['time']=str("{0:02}:{1:02}".format(nowTime.hour,nowTime.minute))
        #         pageDict['ac1'],pageDict['ac2']=ac1,ac2
        #         st.session_state.myClient=DBaccess.AuthenticateUser(pageDict['ac1'],pageDict['ac2'])
        # else:

        # input passwords
        if not st.session_state.dummy: 
            infra.TextBox(pageDict, 'ac1', 'Enter password 1', True)
            infra.TextBox(pageDict, 'ac2', 'Enter password 2', True)

            if st.session_state.debug:
                st.write("**DEBUG** tokens")
                st.write("ac1:",pageDict['ac1'],", ac2:",pageDict['ac2'])

            if st.button("Get Token"):
                pageDict['time']=str("{0:02}:{1:02}".format(nowTime.hour,nowTime.minute))
                st.session_state.myClient=DBaccess.AuthenticateUser(pageDict['ac1'],pageDict['ac2'])

            try:
                st.write("###### Registed at",pageDict['time'])
                exTime = datetime.datetime.fromtimestamp(st.session_state.myClient.user.expires_at, datetime.timezone(datetime.timedelta(hours=8)))
                st.write("###### Token expires at: "+exTime.strftime("%Y-%m-%d  %H:%M"))

                # feedback on passwords
                try:
                    pageDict['user']=st.session_state.myClient.get('getUser', json={'userIdentity': st.session_state.myClient.user.identity})
                    st.success("Returning token for "+str(pageDict['user']['firstName'])+" "+str(pageDict['user']['lastName'])+" seems ok.")
                    if st.session_state.debug:
                        st.write("User (id):",pageDict['user']['firstName'],pageDict['user']['lastName'],"("+pageDict['user']['id']+")")
                except:
                    st.error("Bad token registered. Please close streamlit and try again")
            except KeyError:
                st.info("No token yet registed")


            if "myClient" in list(st.session_state.keys()):
                resetLists=False
                ### reset option
                prog_text = st.empty()
                if st.button("reset lists"):
                    resetLists=True
                ### gather lists
                if "instList" not in list(pageDict.keys()) or resetLists:
                    prog_text.text("** Please wait for *Institutions* to be compiled **")
                    st.write("### Get *Institutions*")
                    pageDict['instList']=DBaccess.GetInstList(st.session_state.myClient)
                    pageDict['instList'] = sorted(pageDict['instList'], key=lambda k: k['name'])
                    st.write("Done!")
                    if "inst" not in pageDict.keys():
                        pageDict['inst']=[x for x in pageDict['instList'] if x['code']==pageDict['user']['institutions'][0]['code']][0]
                else:
                    st.write("##### Institutions: ")
                st.write(pageDict['inst']['name'])

                if "projList" not in list(pageDict.keys()) or resetLists:
                    prog_text.text("** Please wait for *Projects* to be compiled **")
                    st.write("### Get *Projects*")
                    pageDict['projList']=DBaccess.GetProjList(st.session_state.myClient)
                    pageDict['projList'] = sorted(pageDict['projList'], key=lambda k: k['name'])
                    st.write("Done!")
                    if "proj" not in pageDict.keys():
                        pageDict['proj']=[x for x in pageDict['projList'] if x['code']==pageDict['user']['preferences']['defaultProject']][0]
                else:
                    st.write("##### Projects: ")
                prog_text.text("** Lists are compiled **")
                st.write(pageDict['proj']['name'])

            else:
                st.write("Get info when registered")
        
        else:
            infra.SelectBox(pageDict, 'user_name', ('',)+tools.IHEP_USER_NAME, "Username")
            infra.TextBox(pageDict, 'user_pwd', 'Password',True)
            if pageDict['user_name'] != '' and pageDict['user_pwd'] != '': 
                correct_pwd = tools.uname_to_upwd(pageDict['user_name'])
                if pageDict['user_pwd'] == correct_pwd:
                    pageDict['user'] = pageDict['user_name']
                    st.success("Hello! "+pageDict['user']+".")
                else:
                    st.error('Incorrect password!')
        # st.write(pageDict)