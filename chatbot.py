# %% [markdown]
# This is a project where I build a Chatbot for my SQL Database using Streamlit and Vanna Libraries
# 
# Streamlit Provides the UI by turning datascripts into shareable web apps
# Vanna provides the Infra to use LLMs to Generate SQL for you (asking your SQL database questions)

# %%
import vanna as vn 
import streamlit as st

# %%
from vanna.remote import VannaDefault
vn = VannaDefault(model='chinook', api_key='5ff055cdce0c4d0999515f5682d31467')
vn.connect_to_sqlite('https://vanna.ai/Chinook.sqlite')

# %%
question = st.session_state.get("question", default=None)
if question is None:
    st.image("chinook-schema.png", use_column_width=True)
    question = st.text_input("Ask me a question that I can turn into SQL", key='question')
else:
    st.title(question)
    sql = vn.generate_sql(question)
    st.code(sql, language='sql')
    df = vn.run_sql(sql)
    st.dataframe(df, use_container_width=True)
    fig = vn.get_plotly_figure(plotly_code=vn.generate_plotly_code(question=question, sql=sql, df=df), df=df)
    st.plotly_chart(fig, use_container_width=True)
    st.button("Ask another question", on_click=lambda: st.session_state.clear())


