### standard
import streamlit as st
from core.Page import Page
### custom
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import utils.Report.report_tools as report_tools
#####################
### useful functions
#####################

infoList=["  * Nothing here...",
        "   * Nothing here..."]

testTypes={"HYBRID_ASSEMBLY":("ASIC_GLUE_WEIGHT","ASIC_METROLOGY","NO_PPA","PEDESTAL_TRIM_PPA",
                                    "RESPONSE_CURVE_PPA", "STROBE_DELAY_PPA","VISUAL_INSPECTION","VISUAL_INSPECTION_RECEPTION",
                                    "WIRE_BONDING"),
                "MODULE":("GLUE_WEIGHT","MODULE_BOW","MODULE_IV_PS_BONDED","MODULE_IV_PS_V1","MODULE_METROLOGY",
                            "MODULE_WIRE_BONDING","VISUAL_INSPECTION","VISUAL_INSPECTION_RECEPTION"),
                "HYBRID_FLEX":("",),
                "HYBRID_FLEX_TEST_COUPON":(","),
                "CICOREL_CARD":(","),
                "SENSOR_HALFMOONS":(","),
                "ABC":(","),
                "HCC":(",")}


hist_layout={'plot_bgcolor':'#FFFFFF','yaxis_gridcolor':'#000000', 'width':512, 'height':512,
              'font_size':20, 'title_x':0.5}

def get_TestRunsByTestType_df(client, compType, testType):
    list_TestRuns = client.get("listTestRunsByTestType",json={"project":"S","componentType":str(compType),"testType":str(testType),"pageInfo":{"pageSize": 4000}})
    return pd.DataFrame(list_TestRuns.data)

def get_TestRunsByTestTypeAndSite_df(client, compType, testType, site):
    df_TestRuns = get_TestRunsByTestType_df(client, compType, testType)
    df_TestRunsSiteFiltered = df_TestRuns[pd.DataFrame(list(df_TestRuns["institution"]))["code"]==str(site)]
    list_id = list(df_TestRunsSiteFiltered.loc[:,"id"])
    list_TestRunBulkFiltered = client.get("getTestRunBulk", json={"testRun":list_id[-1000:]})
    return pd.DataFrame(list_TestRunBulkFiltered)

@st.cache_data(show_spinner=False)
def get_TestRunsResults_list(client, compType, testType, site):
    df_TestRunsFiltered = get_TestRunsByTestTypeAndSite_df(client, compType, testType, site)
    
    try:
        ret = list(df_TestRunsFiltered["results"]) # df_TestRunsFiltered["results"] will return a pd.Series object
    except KeyError:
        st.error("No requested test run type for site \"" + site +"\"")
        st.stop()

    return ret  

def plot_ASICs_position_deviation(testRunsList, hybType="X", direction=0): #0 for deviation in x direction, 1 for y
    delta_pos = []
    for testRun in testRunsList:
        for item in testRun:
            if item["code"] == "POSITION" and hybType in list(item["value"].keys())[0]:
                for pos in np.array(list(item["value"].values()), dtype=object):
                    pos = np.array(pos)
                    if abs(pos[:2, direction][0]) > 800 or abs(pos[:2, direction][1]) >800: #to exclude clearly illegal values, need to be improved
                        break
                    else:
                        delta_pos.extend(pos[:2, direction]) 
    
    fig = go.Figure(data=[go.Histogram(x=delta_pos, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    if direction==0:
        x_title = 'ASIC Position &#916;X' #\Delta X
    elif direction==1:
        x_title = 'ASIC Position &#916;Y'
    fig.update_layout(
    title_text = hybType+' Hybrids',
    xaxis_title=x_title,
    yaxis_title='Counts'
    )

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=-200, y0=0, x1=-200, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=200, y0=0, x1=200, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=0, y0=0, x1=0, y1=0.95, line={'dash': 'solid'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'
    fig.update_layout(hist_layout)


    return fig

def plot_ASICs_glue_height(testRunsList, hybType="X"):
    glue_height = []
    for testRun in testRunsList:
        for item in testRun:
            if item["code"] == "HEIGHT" and hybType in list(item["value"].keys())[0]:
                for height in list(item["value"].values()):
                    glue_height.append(height) 

    fig = go.Figure(data=[go.Histogram(x=glue_height, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    fig.update_layout(
    title_text = hybType+' Hybrids',
    xaxis_title='Glue Height [&mu;m]',
    yaxis_title='Counts')
    fig.update_layout(hist_layout)

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=80, y0=0, x1=80, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=160, y0=0, x1=160, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=120, y0=0, x1=120, y1=0.95, line={'dash': 'solid'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    return fig

def plot_ASICs_pkg_height(testRunsList, hybType="X"):
    pkg_height = []
    for testRun in testRunsList:
        for item in testRun:
            if item["code"] == "TOTAL_HEIGHT" and hybType in list(item["value"].keys())[0]:
                for height in list(item["value"].values()):
                    pkg_height.append(height) 

    fig = go.Figure(data=[go.Histogram(x=pkg_height, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    fig.update_layout(
    title_text = hybType+' Hybrids',
    xaxis_title='Total Package Height [&mu;m]',
    yaxis_title='Counts')
    fig.update_layout(hist_layout)

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=760, y0=0, x1=760, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=840, y0=0, x1=840, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=800, y0=0, x1=800, y1=0.95, line={'dash': 'solid'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    return fig

def plot_ASICs_tilt(testRunsList, hybType="X", direction=0): #0 for tilt A, 1 for B
    chip_tilt = []
    for testRun in testRunsList:
        for item in testRun:
            if item["code"] == "TILT" and hybType in list(item["value"].keys())[0]:
                for tilts in list(item["value"].values()):
                    chip_tilt.append(tilts[direction]) 
    
    fig = go.Figure(data=[go.Histogram(x=chip_tilt, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    if direction==0:
        x_title = 'ASIC Tilt A'
    elif direction==1:
        x_title = 'ASIC Tilt B'
    fig.update_layout(
    title_text = hybType+' Hybrids',
    xaxis_title=x_title,
    yaxis_title='Counts')
    fig.update_layout(hist_layout)

    fig.add_shape(
        go.layout.Shape(type='line', xref='x', yref='paper',
                        x0=0.025, y0=0, x1=0.025, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
        )
    # fig.layout.shapes[-1]['yref']='paper'

    return fig

def plot_ASICs_glue_weight(testRunsList, standards={}):
    pkg_weight = []
    for testRun in testRunsList:
        if testRun is not None:
            for item in testRun:
                if item["code"] == "GW_GLUE_ASICS":
                    if item["value"] is not None :
                        # if item["value"]>0.1:  # try to exclude bad measurments
                        #     break 
                        # else:
                        pkg_weight.append(item["value"]) 

    x=pkg_weight
    fig = go.Figure(data=[go.Histogram(x=x, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    fig.update_layout(
    xaxis={'range': [0,max(x)*1.1],
            'title': 'Glue Weight (ASICs on hybrid) [g]'},
    title_text = '',
    yaxis_title='Counts')
    fig.update_layout(hist_layout)

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=760, y0=0, x1=760, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=840, y0=0, x1=840, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=800, y0=0, x1=800, y1=0.95, line={'dash': 'solid'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    return fig

def plot_module_glue_weight(testRunsList, standards={}):
    pkg_weight = []
    for testRun in testRunsList:
        if testRun is not None:
            for item in testRun:
                if item["code"] == "GW_GLUE_ASICS":
                    if item["value"] is not None :
                        # if item["value"]>0.1:  # try to exclude bad measurments
                        #     break 
                        # else:
                        pkg_weight.append(item["value"]) 

    x=pkg_weight
    fig = go.Figure(data=[go.Histogram(x=x, marker_color='#3A5FCD', marker_line_color='#27408B',marker_line_width=2, opacity=0.95)])
    fig.update_layout(
    xaxis={'range': [0,max(x)*1.1],
            'title': 'Glue Weight (ASICs on hybrid) [g]'},
    title_text = '',
    yaxis_title='Counts')
    fig.update_layout(hist_layout)

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=760, y0=0, x1=760, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=840, y0=0, x1=840, y1=0.95, line={'dash': 'dash'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    # fig.add_shape(
    #     go.layout.Shape(type='line', xref='x', yref='paper',
    #                     x0=800, y0=0, x1=800, y1=0.95, line={'dash': 'solid'}, line_color="#EE0000")
    #     )
    # # fig.layout.shapes[-1]['yref']='paper'

    return fig

#####################
### main part
#####################

class Page4(Page):
    def __init__(self):
        super().__init__("PDB Report", ":bookmark_tabs: Production Database Report", infoList)

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

        if not st.session_state.dummy:
            ### Reports
            client = st.session_state.myClient

            # sites = ['TRIUMF'] 
            # # sites = ['IHEP'] 
            # df = report_tools.read_pdb_data(sites)  

            # dfy = report_tools.get_module_assembly_sites_yield(df, sites)   
            # print(dfy) 

            st.header("Production Numbers")

            df = report_tools.read_pdb_data()

            table_names = ["",
            'Hybrid flex', 
            'Hybrid assembly', 
            'Module assembly', 
            'Assembled hybrids over time', 
            'Assembled hybrids across sites', 
            'Assembled modules over time', 'Assembled modules across sites']

            # , 
            # 'Assembled hybrids with children SN', 
            # 'Assembled modules with children SN']

            table_name  = st.selectbox("Select Tables", table_names)

            st.subheader(table_name) 

            if table_name == 'Hybrid flex':
                df_hybrid_flex_stage_yield = report_tools.get_hybrid_flex_stages_yield(df)  
                st.dataframe(df_hybrid_flex_stage_yield)

            if table_name == 'Hybrid assembly':
                df_hybrid_assembly_stage_yield = report_tools.get_hybrid_assembly_stages_yield(df) 
                st.dataframe(df_hybrid_assembly_stage_yield)

            if table_name == 'Module assembly':
                df_module_assembly_stage_yield = report_tools.get_module_assembly_stages_yield(df)
                st.dataframe(df_module_assembly_stage_yield)

            if table_name == 'Assembled hybrids over time': 
                df_hybrid_assembly_days_yield = report_tools.get_hybrid_assembly_days_yield(df)   
                st.dataframe(df_hybrid_assembly_days_yield) 
                fig = report_tools.plot_hybrid_assembly_days_yield(df_hybrid_assembly_days_yield) 
                st.plotly_chart(fig) 

            if table_name == 'Assembled hybrids across sites': 
                df_hybrid_assembly_sites_yield = report_tools.get_hybrid_assembly_sites_yield(df)   
                st.dataframe(df_hybrid_assembly_sites_yield) 
                fig = report_tools.plot_hybrid_assembly_sites_yield(df_hybrid_assembly_sites_yield)  
                st.plotly_chart(fig) 

            if table_name == 'Assembled modules over time': 
                df_module_assembly_days_yield = report_tools.get_module_assembly_days_yield(df)    
                st.dataframe(df_module_assembly_days_yield) 
                fig = report_tools.plot_module_assembly_days_yield(df_module_assembly_days_yield) 
                st.plotly_chart(fig) 

            if table_name == 'Assembled modules across sites': 
                df_module_assembly_sites_yield = report_tools.get_module_assembly_sites_yield(df)   
                st.dataframe(df_module_assembly_sites_yield) 
                fig = report_tools.plot_module_assembly_sites_yield(df_module_assembly_sites_yield)  
                st.plotly_chart(fig) 

            ###Shudong's QT
            st.write("---")
            st.header("Test Parameters")
            compType=st.selectbox("Choose a component type", ("",)+tuple(testTypes.keys()) )
            testType=""
            sites=[]
            if not compType == "":
                testType=st.selectbox("Choose a test type", ("",)+tuple(testTypes[compType]))
            if not testType == "":
                sites=st.multiselect("Choose sites", report_tools.HYBRID_SITES_BARREL)
            if not sites == []:
                testRunResults=[]
                
                if compType=="HYBRID_ASSEMBLY" and testType=="ASIC_METROLOGY":
                    for site in sites:
                        testRunResults.extend(get_TestRunsResults_list(client, compType, testType, site))

                    col1, col2 = st.columns(2)

                    with col1:
                        fig_hybX_posX = plot_ASICs_position_deviation(testRunResults,"X",0)
                        st.plotly_chart(fig_hybX_posX)

                        fig_glue_height_hybX = plot_ASICs_glue_height(testRunResults,"X")
                        st.plotly_chart(fig_glue_height_hybX)

                        fig_tilt_hybX = plot_ASICs_tilt(testRunResults,"X",0)
                        st.plotly_chart(fig_tilt_hybX)

                    with col2:
                        fig_hybX_posY = plot_ASICs_position_deviation(testRunResults,"X",1)
                        st.plotly_chart(fig_hybX_posY)
                        
                        fig_pkg_height_hybX = plot_ASICs_pkg_height(testRunResults,"X")
                        st.plotly_chart(fig_pkg_height_hybX)

                        fig_tilt_hybX = plot_ASICs_tilt(testRunResults,"X",1)
                        st.plotly_chart(fig_tilt_hybX)

                    col3, col4 = st.columns(2)

                    with col3:
                        fig_hybY_posX = plot_ASICs_position_deviation(testRunResults,"Y",0)
                        st.plotly_chart(fig_hybY_posX)

                        fig_glue_height_hybY = plot_ASICs_glue_height(testRunResults,"Y")
                        st.plotly_chart(fig_glue_height_hybY)

                        fig_tilt_hybY = plot_ASICs_tilt(testRunResults,"Y",0)
                        st.plotly_chart(fig_tilt_hybY)

                    with col4:
                        fig_hybY_posY = plot_ASICs_position_deviation(testRunResults,"Y",1)
                        st.plotly_chart(fig_hybY_posY)
                        
                        fig_pkg_height_hybY = plot_ASICs_pkg_height(testRunResults,"Y")
                        st.plotly_chart(fig_pkg_height_hybY)

                        fig_tilt_hybY = plot_ASICs_tilt(testRunResults,"Y",1)
                        st.plotly_chart(fig_tilt_hybY)

                if compType=="HYBRID_ASSEMBLY" and testType=="ASIC_GLUE_WEIGHT":
                    for site in sites:
                        testRunResults.extend(get_TestRunsResults_list(client, compType, testType, site))

                    fig_ASIC_glue_weight = plot_ASICs_glue_weight(testRunResults)
                    st.plotly_chart(fig_ASIC_glue_weight)



