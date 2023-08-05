import sys

import streamlit as st
from webpages.core.MultiApp import App

smalls={
    'Dev. Phase': "IHEP Internal Use Only",
    # 'git':"https://gitlab.cern.ch/wraight/itkpdbtemplatemulti",
    'Contact': "wangsd@ihep.ac.cn"
}

myapp = App("ihepsop", "# IHEP ATLAS-ITk \n ### :clipboard: Production Flow Page", smalls)

st.set_page_config(
page_title="IHEP ATLAS-ITk Production Flow Page",
page_icon=":clipboard:",
layout="wide"
)

myapp.main()
