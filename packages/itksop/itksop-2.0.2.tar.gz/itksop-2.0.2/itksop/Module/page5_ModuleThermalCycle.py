### standard
import streamlit as st
from core.Page import Page
### custom
import os 
import sys
import time 
import datetime
import pandas as pd
import numpy as np
### PDB stuff
import itkdb
import core.tools as tools
import core.DBaccess as DBaccess
import core.stInfrastructure as infra
import itkdb
import itkdb.exceptions as itkX

#####################
### useful functions
#####################

infoList = ["  * Test the electronic performance of the module ...",
            "   * Nothing here..."]

def operation1():
    pass

def operation2():
    pass

def operation3():
    pass

def moduleThermalCycleFlow():
    pass
#####################
### main part
#####################

class Page5(Page):
    def __init__(self):
        super().__init__("Module Thermal Cycle", ":thermometer: Module Thermal Cycle", infoList)

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