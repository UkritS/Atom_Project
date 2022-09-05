import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
from plotly.figure_factory import create_distplot
#import plotly.express as px # pip install plotly-express
#import plotly.figure_factory as ff
#from plotly.tools import FigureFactory as ff
import base64 # Standard Python Module
from io import StringIO, BytesIO #Standard Python Module

def generate_excel_download_link(dfsum):
#https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = BytesIO()
    dfsum.to_excel(towrite, encoding='utf-8', index=False, header=True) #write to ByteIO
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    href= f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Process Capability Analysis</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
#https://discuss.streamlit.io/t/how-to-add-a-download-excel-csv-function-to-a-button/4474/5
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()  # some strings
    href= f'<a href="data:text/html;charset=utf-8;base64,{b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)

#from plotly.figure_factory import create_distplot

st.set_page_config(page_title='Distribution Plotter')
st.title('Distribution Plotter 📈')
#st.subheader('Input an Excel file')

PName = st.empty().text_input("Enter Parameter name")
LSL = st.empty().text_input("Enter Lower Spec Limit (LSL)")
USL = st.empty().text_input("Enter Upper Spec Limit (USL)")

uploaded_file = st.file_uploader('Choose XLSX file', type='xlsx')

showhist = st.checkbox('Show Histogram')
hist = False
if showhist:
     hist = True

#st.write('LSL = ' + LSL + ', USL = ' + USL)
if uploaded_file:
    st.markdown('---')
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    #st.dataframe(df)

    # -- Plot dataframe
    #fig = ff.create_distplot([df[c] for c in df.columns], df.columns, show_rug=False)
    fig = create_distplot([df[c] for c in df.columns], df.columns,show_hist = hist, show_rug=False)
    fig.add_vline(LSL, line_color="red")
    fig.add_vline(USL, line_color="red")

    #fig.update_layout(title_text=PName)
    fig.update_layout(
        title_text=PName + " Distribution",
        #plot_bgcolor="white",
        #paper_bgcolor="white",
        xaxis_title=PName,
        yaxis_title="Density",
        #legend_title="Legend Title",
        font=dict(
        color="Black"
        )
    )
    fig.add_annotation(
        x=LSL,
        y=0,
        xref="x",
        yref="y",
        text="LSL="+LSL,
        showarrow=True,
        font=dict(
        color="White"
        ),
        align="center",
        arrowhead=1,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor="#636363",
        ax=50,
        ay=15,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=1,
        bgcolor="#ff7f0e",
        opacity=0.8
    )
    fig.add_annotation(
        x=USL,
        y=0,
        xref="x",
        yref="y",
        text="USL="+USL,
        showarrow=True,
        font=dict(
        color="White"
        ),
        align="center",
        arrowhead=1,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor="#636363",
        ax=50,
        ay=15,
        bordercolor="#c7c7c7",
        borderwidth=1,
        borderpad=1,
        bgcolor="#ff7f0e",
        opacity=0.8
    )

    st.plotly_chart(fig)
    if LSL and USL:
        dfmin = df.min()
        dfmax = df.max()
        dfmean = df.mean()
        dfstd = df.std()
        Range = float(USL)-float(LSL)
        dfcp = Range/(6*dfstd)
        dfcpk1 = (float(USL)-dfmean)/(3*dfstd)
        dfcpk2 = (dfmean-float(LSL))/(3*dfstd)
        dfcpk = pd.concat([dfcpk1,dfcpk2],axis=1)
        dfcpk = dfcpk.min(axis = 1)
        dfz1 = (float(USL)-dfmean)/(dfstd)
        dfz2 = (dfmean-float(LSL))/(dfstd)
        dfz = pd.concat([dfz1,dfz2],axis=1)
        dfz = dfz.min(axis = 1)
        dfsum = pd.concat([dfmin,dfmax,dfmean,dfstd,dfcp,dfcpk,dfz],axis=1)
        dfsum.columns = ['Min', 'Max', 'Mean', 'SD', 'Cp','Cpk','z']
        st.dataframe(dfsum)
        st.subheader('Downloads:')
        generate_excel_download_link(dfsum)
        generate_html_download_link(fig)
    else:
        st.warning('Please enter LSL and USL to review Process Capability Analysis', icon="⚠️")

#----Contact----
st.header(":mailbox: Get In Touch With Me!")
#Documention: http://formsubmit.# COMBAK:
contact_form = """
<form action="https://formsubmit.co/ukrits@lpn.hanabk.th.com" method="POST">
<input type="hidden" name="_captcha" value="false">
<input type="text" name="name" placeholder="Your Name" required>
<input type="email" name="email" placeholder = "Your Email" required>
<textarea name="message" placeholder="Your Message" required></textarea>
<button type="submit">Send</button>
</form>
"""

st.markdown(contact_form,unsafe_allow_html=True)

#Use Local CSS File
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css("style/style.css")
