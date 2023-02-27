# -*- encoding: utf-8 -*-
import pandas as pd
import os
import osquery
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid

st.set_page_config(
     page_title="osquery - streamlit",
     layout="wide",
     initial_sidebar_state="expanded",
 )


def get_df(_sql):
    # judge osqueryctl status

    # You must know the Thrift socket path
    # For an installed and running system osqueryd, this is:
    #   Linux and macOS: /var/osquery/osquery.em
    #   FreeBSD: /var/run/osquery.em
    #   Windows: \\.\pipe\osquery.em

    if os.path.exists("/var/osquery/osquery.em"):
        instance = osquery.ExtensionClient('/var/osquery/osquery.em')
        instance.open()
        client = instance.extension_client()
        res = client.query(_sql).response
        return res
    else:
        st.error("osquery not run, please use `osquertctl start`")
        return []

_sql = st.text_area("input sql here", key="sql")
if st.button("submit", key="submit"):
    st.session_state["res"] = get_df(_sql)

if "res" in st.session_state:
    df = pd.DataFrame(st.session_state["res"])
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination()
    gb.configure_side_bar()
    gridOptions = gb.build()
    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        height=800,
        width=1000,
        fit_columns_on_grid_load=True,
        allow_unsafe_jscode=True,
        enable_enterprise_modules=True
    )