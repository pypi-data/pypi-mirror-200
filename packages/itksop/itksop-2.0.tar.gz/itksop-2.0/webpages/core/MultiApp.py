#### based on: https://gitlab.cern.ch/wraight/itk_pdb_testapp/-/blob/master/core/MultiApp.py 
import streamlit as st
import corePages
import sopPages
###
import os
import sys
import datetime
from PIL import Image
import core.DBaccess as DBaccess
import core.stInfrastructure as infra

#####################
### useful functions
#####################

def toggle_debug():
    st.session_state.debug = not st.session_state.debug

def priority_sorting(items, prior_items):
	def weight(i):
		if i in prior_items:
			return (0,i)  #weight == 0 , prior
		return (1,i) 
	items.sort(key=weight)


class App:

    def __init__(self, name, title, smalls):
        self.name = name
        self.title = title
        self.smalls = smalls
        self.state = {}

        self.init_themes()

    def init_themes(self):
        self.themes = sopPages.__all__.keys()
        return

    def init_pages(self,theme=None):
        try:
            self.pages.clear()
        except AttributeError:
            self.pages = dict()
        allPages = []
        allPages = corePages.__all__.copy()
        if theme!=None:
            allPages += sopPages.__all__[theme].copy()
        # order pages if required
        #allPages.insert(0, allPages.pop([p().name for p in allPages.index("NAME")))
        allPages.append(allPages.pop([p().name for p in allPages].index("Broom Cupboard")))
        for page in allPages:
            p = page() #self.state)
            self.pages[p.name] = p
        #return {theme:[len(allPages),len(corePages.__all__),len(sopPages.__all__),len(self.pages.keys())]}
        #return {theme:[p().name for p in allPages]} #self.pages.keys()}
        return [{k:[p().name for p in v]} for k,v in sopPages.__all__.items()]

#####################
### main part
#####################

    def main(self):
        IHEP_logo = Image.open('./webpages/img/IHEP_logo2022.png')
        st.sidebar.image(IHEP_logo,width = 196)
        # ATLAS_logo = Image.open('./webpages/img/ATLAS_logo.png')
        # st.sidebar.image(ATLAS_logo,width = 144)

        st.sidebar.markdown(self.title)
        
        dummy = st.sidebar.checkbox("Toggle dummy")  ### might have bugs here?
        if dummy:
            st.session_state.dummy=True
        else: 
            st.session_state.dummy=False

        ### sidebar
        st.sidebar.write("")
        st.sidebar.write("")
        st.sidebar.markdown("#### :zap: Powered by [itkdb](https://pypi.org/project/itkdb/) :zap:")

        st.sidebar.write("---")
        ### theme and page selection
        theme_list = list(self.themes)
        prior_themes = ('Overview')
        priority_sorting(theme_list, prior_themes)

        theme = st.sidebar.radio("Select theme: ", tuple(theme_list))
        self.init_pages(theme)
        name = st.sidebar.radio("Select page: ", tuple(self.pages.keys()))

        ### check session state attribute, set if none
        try:
            if name in st.session_state[theme].keys():
                if st.session_state.debug: st.sidebar.markdown("session_state \'"+theme+"."+name+"\' OK")
            else:
                st.session_state[theme][name]={}
                if st.session_state.debug: st.sidebar.markdown("session_state \'"+theme+"."+name+"\' defined")
        except KeyError:
            st.session_state[theme]={name:{}}

        ### renew token button 
        if not st.session_state.dummy:
            try:
                st.sidebar.markdown("---")
                st.sidebar.markdown("##### Renew token here")
                try:
                    if st.session_state.myClient:
                        exTime = datetime.datetime.fromtimestamp(st.session_state.myClient.user.expires_at, datetime.timezone(datetime.timedelta(hours=8)))
                        st.sidebar.markdown("Token expires at: "+exTime.strftime("%Y-%m-%d  %H:%M"))
                    if st.session_state.Homepage['ac1'] and st.session_state.Homepage['ac2']:
                        if st.sidebar.button("Renew Token"):
                            nowTime = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
                            st.session_state.Homepage['time']=str("{0:02}:{1:02}".format(nowTime.hour,nowTime.minute))
                            st.sidebar.markdown("Registed at: "+st.session_state.Homepage['time'])
                            st.session_state.myClient=getattr(DBaccess,"AuthenticateUser")(st.session_state.Homepage['ac1'],st.session_state.Homepage['ac2'])
                    else:
                        st.sidebar.markdown("register on Homepage")
                except AttributeError:
                    st.sidebar.markdown("No client set, get token on homepage first")
            except AttributeError:
                pass

            st.sidebar.markdown("---")

        # ### inst, proj data (user's by default)
        # if "Homepage" in [x for x in st.session_state.keys()]:
        #     try:
        #         st.session_state.Homepage['inst']=st.sidebar.selectbox("Institution:", st.session_state.Homepage['instList'], format_func=lambda x: x['code'], index=st.session_state.Homepage['instList'].index(st.session_state.Homepage['inst']))
        #     except KeyError:
        #         st.sidebar.markdown("No instList set")
        #     try:
        #         st.session_state.Homepage['proj']=st.sidebar.selectbox("Project:", st.session_state.Homepage['projList'], format_func=lambda x: x['code'], index=st.session_state.Homepage['projList'].index(st.session_state.Homepage['proj']))
        #     except KeyError:
        #         st.sidebar.markdown("No projList set")
        # else:
        #     st.sidebar.markdown("lists not found")

        # st.sidebar.markdown("---")

        ### mini-state summary
        # if st.sidebar.button("State Summary"):
        #     # st.write(dir(state))
        #     mykeys=[x for x in st.session_state.keys()]
        #     # st.sidebar.markdown(myatts)
        #     for mk in mykeys:
        #         if mk=="broom": continue
        #         st.sidebar.markdown(f"**{mk}** defined")

        # st.sidebar.markdown("---")

        ### debug toggle
        try:
            debug = st.sidebar.checkbox("Toggle debug",value=st.session_state.debug)
        except AttributeError:
            debug = st.sidebar.checkbox("Toggle debug")
        if debug:
            st.session_state.debug=True
        else: st.session_state.debug=False

        ### small print
        st.sidebar.markdown("---")
        st.sidebar.markdown("*small print*:")
        # st.sidebar.markdown("Streamlit Template: "+infra.Version())
        # st.sidebar.markdown("ITkPdb Template: "+DBaccess.Version())
        for k,v in self.smalls.items():
            if k in ['git','docker']: # repositories
                st.sidebar.markdown("["+k+" repository]("+v+")")
            else:
                st.sidebar.write(k+' : '+v)
        # st.sidebar.write(st.session_state)

        ### get page
        self.pages[name].main()


#EOF