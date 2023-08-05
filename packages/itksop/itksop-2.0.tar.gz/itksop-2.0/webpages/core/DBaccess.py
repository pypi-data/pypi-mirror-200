#Credit: Kenneth Gibb Wraight https://gitlab.cern.ch/wraight/itk_pdb_testapp/-/blob/master/core/DBaccess.py
import streamlit as st
###
import itkdb
import itkdb.exceptions as itkX

#####################
### Things
#####################

def Version():
    return ("13-09-21")

def AuthenticateUser(ac1,ac2):
    user = itkdb.core.User(access_code1=ac1, access_code2=ac2)
    user.authenticate()
    client = itkdb.Client(user=user)
    return client

@st.cache_data
def DbGet(client, myAction, inData, listFlag=False):
    outData=None
    if listFlag:
        try:
            outData = list(client.get(myAction, json=inData ) )
        except itkX.BadRequest as b: # catch double registrations
            st.write(myAction+": went wrong for "+str(inData))
            st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    else:
        try:
            outData = client.get(myAction, json=inData)
        except itkX.BadRequest as b: # catch double registrations
            st.write(myAction+": went wrong for "+str(inData))
            st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    return outData

@st.cache_data
def DbPost(client, myAction, inData):
    outData=None
    try:
        outData=client.post(myAction, json=inData)
    except itkX.BadRequest as b: # catch double registrations
        st.write(myAction+": went wrong for "+str(inData))
        st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
        try:
            st.write('**'+str(b)[str(b).find('"paramMap": ')+len('"paramMap": '):-8]+'**') # sucks
        except:
            pass
    except itkX.ServerError as b: # catch double registrations
        st.write(myAction+": went wrong for "+str(inData))
        st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    return outData

@st.cache_data
def GetInstList(_client):
    myList=[]
    try:
        myList = list(_client.get('listInstitutions'))
    except itkX.BadRequest as b: # catch double registrations
        st.write('listInstitutions'+": went wrong for "+str(inData))
        st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    return myList

@st.cache_data
def GetProjList(_client):
    myList=[]
    try:
        myList= list(_client.get('listProjects'))
    except itkX.BadRequest as b: # catch double registrations
        st.write('listProjects'+": went wrong for "+str(inData))
        st.write('**'+str(b)[str(b).find('"message": ')+len('"message": '):str(b).find('"paramMap"')-8]+'**') # sucks
    return myList
