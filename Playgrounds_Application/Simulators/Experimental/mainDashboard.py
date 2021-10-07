"""staking learn page shown when the user enters the learn application"""
# ==============THE LIBRARIES
# region Description: Import all required libraries for this app: Staking learn page
from pycoingecko import CoinGeckoAPI  # Coin gecko API: Pulls live data from coin gecko
import math  # Needed for basic math operations\n",
import pandas as pd  # Needed fpr dataframe creation and operations\n",
import numpy as np  # Needed for array manipulations\n",
from itertools import islice  # Needed for more complex row and coloumn slicing\n",
import matplotlib.pyplot as plt  # Needed for quickly ploting results"
import pathlib  # url management
import plotly.express as px  # cleaner graphs
import plotly.graph_objects as go  # cleaner graphs
import requests
import streamlit as st
from datetime import datetime, timedelta


# import awesome_stream lit as ast
# endregion
def app():
    @st.cache
    def run_query(q):

        # endpoint where you are making the request
        request = requests.post('https://api.thegraph.com/subgraphs/name/drondin/olympus-graph'
                                '',
                                json={'query': query})
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed. return code is {}.      {}'.format(request.status_code, query))

    # The Graph query... these queries are made available to us on the olympus sub graph -
    query = """

    {
    protocolMetrics(first: 100, orderBy: timestamp, orderDirection: desc) {
        timestamp
        ohmCirculatingSupply
        sOhmCirculatingSupply
        totalSupply
        ohmPrice
        marketCap
        totalValueLocked
        treasuryMarketValue
        treasuryRiskFreeValue
        runwayCurrent
        currentAPY
        nextEpochRebase
        nextDistributedOhm
      }
    }
    """
    # assign the results to a variable called results
    result = run_query(query)

    # results come as a list of dictionaries, which is in a nested dictionary. so we have to extract the dictionary we care about
    dataDict = result['data']['protocolMetrics']
    protocolMetrics_df = pd.DataFrame(dataDict)
    protocolMetrics_df = protocolMetrics_df.astype(float)
    protocolMetrics_df['dateTime'] = pd.to_datetime(protocolMetrics_df.timestamp,unit='s')
    protocolMetrics_df['dateTime'] = protocolMetrics_df['dateTime'].dt.date
    protocolMetrics_df = protocolMetrics_df.set_index('dateTime')



# do stuff with the data: app

    st.title('Playgrounds Ω Explorer')
    st.markdown('''----''')

    st.sidebar.info('Some information on what this page is about')
    st.sidebar.info('Instructions')

    cols = ["ohmCirculatingSupply", "sOhmCirculatingSupply", "totalSupply"]
    st.subheader('Select metrics to explore')
    selected_metric = st.multiselect("",protocolMetrics_df.columns.tolist(),default=cols)
    selected_metric_df = protocolMetrics_df[selected_metric]

    st.subheader('Filter by date')
    col1,col2 = st.columns((1,1))
    with col1:
        startDate = st.date_input('Start Date',selected_metric_df.index.min())
    with col2:
        endDate = st.date_input('End Date',selected_metric_df.index.max())

    if startDate < endDate:
        pass
    else:
        st.error('Error: Date out of possible range')
    mask = (selected_metric_df.index > startDate) & (selected_metric_df.index <= endDate)
    selected_metric_df = selected_metric_df.loc[mask]

    col3, col4 = st.columns((4,1))
    with col3:
        st.subheader('Metrics visualized')
        explorer_chart = px.line(selected_metric_df)
        explorer_chart.update_layout(autosize=True, showlegend=True ,legend_title_text='Metrics', margin=dict(l=20, r=30, t=10, b=20))
        explorer_chart.update_layout(dragmode = 'drawopenpath',newshape_line_color='cyan')
        explorer_chart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
        explorer_chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
        explorer_chart.update_xaxes(title = 'Date',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.1,mirror=True)
        explorer_chart.update_yaxes(title = 'Metrics',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True)
        st.plotly_chart(explorer_chart, use_container_width=True)

    with col4:
        st.info('''
        - Selected metric: xx
        - Selected metric : yy
        - Selected metric: xx
        - Selected metric : yy
        ''')

    st.subheader('Select a metric to see definition')
    st.info('Write code to pass definitions here')

    st.subheader('Metrics in tabulated view')
    with st.expander("Click me!"):
        st.write(selected_metric_df)

    st.write('---')

# endregion
