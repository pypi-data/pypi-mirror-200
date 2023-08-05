#credit: Kenneth Gibb Wraight https://gitlab.cern.ch/wraight/itk_pdb_testapp/-/blob/master/core/ThemePage.py
import streamlit as st
import inspect

class Page:

    def __init__(self, name, title, instructions=[]):
        self.name = name
        self.title = title
        self.instructions = instructions

    def main(self):
        ### title and (optional) instructions
        st.title(self.title)
        if st.session_state.debug:
            st.write("_ page name:",self.name,"_")
            st.write("_ file name:",inspect.getfile(self.__class__),"_")
        st.write("---")
        if st.session_state.debug:
            for i in self.instructions:
                if "*" in i[0:3]:
                    st.write(i)
                else:
                    st.write("  *",i)
        else:
            st.write(" * toggle debug for details")
        st.write("---")

        # debug check
        if st.session_state.debug:
            st.write("### Debug is on")

        ### check session state attribute, stop if none
        for key in st.session_state.keys():
            if type(st.session_state[key])!=type({}): continue
            if self.name in st.session_state[key].keys():
                if st.session_state.debug:
                    st.write("st.session_state \'"+key+"."+self.name+"\' defined")
                return st.session_state[key][self.name]
        else:
            st.write("no session state attribute defined!")
            st.stop()
        return None
