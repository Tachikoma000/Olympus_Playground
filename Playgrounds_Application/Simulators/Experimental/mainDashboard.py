"""staking learn page shown when the user enters the learn application"""
# ==============THE LIBRARIES
# region Description: Import all required libraries for this app: Staking learn page
# region Description: Import all required libraries for this simulator
import math  # Needed for basic math operations\n",
import pandas as pd  # Needed fpr dataframe creation and operations\n",
import numpy as np  # Needed for array manipulations\n",
from millify import millify
from itertools import islice  # Needed for more complex row and coloumn slicing\n",
import matplotlib.pyplot as plt  # Needed for quickly ploting results"
import pathlib  # url management
import plotly.express as px  # cleaner graphs
import plotly.graph_objects as go  # cleaner graphs
import streamlit as st
from PIL import Image
import pathlib
from pathlib import Path
import base64
import requests


bondingLearn_1 = Path(__file__).parents[1] / 'Assets/PG_bond.png'
bondingLearn_1  = Image.open(bondingLearn_1)

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
    st.sidebar.info('Some information on what this page is about')
    st.sidebar.info('Instructions')

    st.title('Playgrounds Ω Explorer')
    st.markdown('''----''')


    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="OHM Price", value ="$ %.2f" % protocolMetrics_df.ohmPrice.iloc[0])
    col2.metric(label="Market Cap", value = millify(protocolMetrics_df.marketCap.iloc[0], precision = 3))
    col3.metric(label="Total Supply", value = millify(protocolMetrics_df.totalSupply.iloc[0], precision = 3))
    col4.metric(label="Rebase Rate", value="%.4f" % protocolMetrics_df.nextEpochRebase.iloc[0])
    st.markdown('''----''')


    cols = ["ohmCirculatingSupply", "sOhmCirculatingSupply", "totalSupply"]
    st.subheader('Select metrics to explore')
    selected_metric = st.multiselect("",protocolMetrics_df.columns.tolist(),default=cols)
    selected_metric_df = protocolMetrics_df[selected_metric]
    st.subheader('Filter by date')
    col5,col6 = st.columns((1,1))
    with col5:
        startDate = st.date_input('Start Date',selected_metric_df.index.min())
    with col6:
        endDate = st.date_input('End Date',selected_metric_df.index.max())
    if startDate < endDate:
        pass
    else:
        st.error('Error: Date out of possible range')
    mask = (selected_metric_df.index > startDate) & (selected_metric_df.index <= endDate)
    selected_metric_df = selected_metric_df.loc[mask]
    st.subheader('Metrics visualized')
    explorer_chart = px.line(selected_metric_df)
    explorer_chart.update_layout(autosize=True, showlegend=True ,legend_title_text='Metrics', margin=dict(l=20, r=30, t=10, b=20))
    explorer_chart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
    explorer_chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    explorer_chart.update_xaxes(title = 'Date',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.1,mirror=True)
    explorer_chart.update_yaxes(title = 'Metrics',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True)
    st.plotly_chart(explorer_chart, use_container_width=True)
    st.subheader('Selected metrics in tabulated view')
    with st.expander("Click me!"):
        st.write(selected_metric_df)
    st.markdown('''----''')


    st.subheader('Metrics Definitions')
    st.info('''
    Write code to pass definitions here
    - Total Value Deposited: Total Value Locked, is the dollar amount of all OHM staked in the protocol. 
                            This metric is often used as growth or health indicator in DeFi projects.
                            
    - Treasury Market Value: Market Value of Treasury Assets, is the sum of the value (in dollars) of all assets held by the treasury.
    
    - Treasury Risk Free Value: Risk Free Value, is the amount of funds the treasury guarantees to use for backing OHM.
    
    - Reward Rate: Reward rate is the configured percentage of OHM distributed to all stakers on each rebase relative to the total supply. 
                    The reward rate is precisely set by the policy team.
    
    - APY: Annual Percentage Yield, is the normalized representation of an interest rate,
            based on a compounding period over one year. 
            Note that APYs provided are rather ballpark level indicators and not so much precise future results.
            
    - Runway Available: Runway, is the number of days sOHM emissions can be sustained at a given rate. Lower APY = longer runway
    
    ''')
# endregion
