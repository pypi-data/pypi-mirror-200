import streamlit as st
import polars as pl

from polars.internals.expr.string import ExprStringNameSpace

funcs = {
    "Starts with": ExprStringNameSpace.starts_with,
    "Ends with": ExprStringNameSpace.ends_with,
    "Contains": ExprStringNameSpace.contains,
    "Regex": ExprStringNameSpace.extract,
}

thenfuncs = {"Value": pl.lit}

conditions = []
x = pl.col("PredictorName")

st.session_state['categorization'] = []
# func = funcs['Starts with']
# st.write(func(x, "test"))
def newCondition():
    func, val, thenfunc, thenval, trash = st.columns([5, 5, 5, 5, 1])
    with func:
        func = st.selectbox("When", funcs.keys())
    with val:
        val = st.text_input("Value")
    with thenfunc:
        thenfunc = st.selectbox("Then", options=thenfuncs.keys())
    with thenval:
        thenval = st.text_input(
            "Value",
            key="thenval",
        )
    with trash:
        st.button("🗑️")
    st.session_state['categorization'].append([func, val, thenfunc, thenval])


if st.button("Add condition"):
    newCondition()

for condition in st.session_state['categorization']:
    st.write(condition)
st.write(conditions)

pl.when(funcs[func](x, val)).then(thenfuncs[thenfunc](thenval))
