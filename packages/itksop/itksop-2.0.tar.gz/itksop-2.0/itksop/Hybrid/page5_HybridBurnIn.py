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

infoList = ["  * Hybrid Burn-in...",
            "   * Nothing here..."]

def prepareBurnInDevices():
    pass

def conductBurnIn():
    pass

def uploadTestResults():
    pass

def hybridBurnInFlow():
    pass


#####################
### main part
#####################

class Page5(Page):
    def __init__(self):
        super().__init__("Hybrid Burn-in", ":fire: Hybrid Burn-in", infoList)

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