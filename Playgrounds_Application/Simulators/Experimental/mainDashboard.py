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


explorer_Logo = Path(__file__).parents[1] / 'Assets/PG_explorer_logo.png'
explorer_Logo  = Image.open(explorer_Logo)

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
    st.sidebar.info('''
        **Playgrounds Ω Explorer** is designed to give you deeper insight into historical protocol data.
        Using this tool, you can view the historical data for a single or multiple protocol metrics (i.e. RFV growth over time, supply growth,
        or even the current runway).
        
        Have some fun! We can't wait to see the insight you discover!
        ''')
    st.sidebar.info('''
        **Instructions**
        - **Metrics filter tool**: Use the metrics filter dropdown tool to select the metric/metrics you care about! The chart is designed to scale and accommodate all protocol metrics available! 
        - **Date filter**: In addition to filtering by metrics, you can also filter by time frames. Use the Start/End Date filter to expand or narrow down your time scale
        - **Metrics Visualized**: The chart is an incredibly powerful tool for you to view and analyze your selected metric/metrics. Here are some cool things you can do:

            - Hide and view trend lines by clicking on the legend
            - Use the toolbar to access tools such as zoom, pan, data comparison, spike lines, and download
        
        - **Selected Metrics**: For the data table lovers, access your selected metrics in tabular form and download them as CSV! 
        ''')

    col1, col2 = st.columns((1,1))
    with col1:
        st.image(explorer_Logo)
    st.markdown('''----''')

    col3, col4, col5, col6 = st.columns(4)
    col3.metric(label="OHM Price", value ="$ %.2f" % protocolMetrics_df.ohmPrice.iloc[0])
    col4.metric(label="Market Cap", value = millify(protocolMetrics_df.marketCap.iloc[0], precision = 3))
    col5.metric(label="Total Supply", value = millify(protocolMetrics_df.totalSupply.iloc[0], precision = 3))
    col6.metric(label="Rebase Rate", value="%.4f" % protocolMetrics_df.nextEpochRebase.iloc[0])
    st.markdown('''----''')


    cols = ["ohmCirculatingSupply", "sOhmCirculatingSupply", "totalSupply"]
    st.subheader('Select metrics to explore')
    selected_metric = st.multiselect("",protocolMetrics_df.columns.tolist(),default=cols)
    selected_metric_df = protocolMetrics_df[selected_metric]
    st.subheader('Filter by date')
    col7,col8 = st.columns((1,1))
    with col7:
        startDate = st.date_input('Start Date',selected_metric_df.index.min())
    with col8:
        endDate = st.date_input('End Date',selected_metric_df.index.max())
    if startDate < endDate:
        pass
    else:
        st.error('Error: Date out of possible range')
    mask = (selected_metric_df.index > startDate) & (selected_metric_df.index <= endDate)
    selected_metric_df = selected_metric_df.loc[mask]
    selected_metric_df_CSV = selected_metric_df.to_csv().encode('utf-8')
    st.subheader('Metrics visualized')
    explorer_chart = px.line(selected_metric_df)
    explorer_chart.update_layout(autosize=True, showlegend=True ,legend_title_text='Metrics', margin=dict(l=20, r=30, t=10, b=20))
    explorer_chart.update_layout(legend=dict(yanchor="top",y=0.99,xanchor="left",x=0.01))
    explorer_chart.update_layout({'paper_bgcolor': 'rgba(0,0,0,0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})
    explorer_chart.update_xaxes(title = 'Date',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.1,mirror=True)
    explorer_chart.update_yaxes(title = 'Metrics',showline=True, linewidth=0.1, linecolor='#31333F', showgrid=False, gridwidth=0.01,mirror=True)
    st.plotly_chart(explorer_chart, use_container_width=True)
    st.subheader('Selected metrics in tabulated view')
    with st.expander("Click to view"):
        st.write(selected_metric_df)
        st.download_button(
            "Press to download selected protocol metrics data",
            selected_metric_df_CSV,
            "protocolMetrics.csv",
            "text/csv",
            key='browser-data'
        )

    st.markdown('''----''')


    st.subheader('Metrics Definitions')
    st.info('''
    - Total Value Deposited: Total Value Locked, is the dollar amount of all OHM staked in the protocol. 
                            This metric is often used as growth or health indicator in DeFi projects.
                            
    - Treasury Market Value: Market Value of Treasury Assets, is the sum of the value (in dollars) of all assets held by the treasury.
    
    - Treasury Risk Free Value: Risk Free Value, is the amount of funds the treasury guarantees to use for backing OHM.
    
    - Reward Rate: Reward rate is the configured percentage of OHM distributed to all stakers on each rebase relative to the total supply. 
                    The reward rate is precisely set by the policy team, and voted upon by the community.
    
    - APY: Annual Percentage Yield, is the normalized representation of an interest rate,
            based on a compounding period over one year. 
            Note that APYs provided are rather ballpark level indicators and not so much precise future results.
            
    - Runway Available: Runway, is the number of days sOHM emissions can be sustained at a given rate. Lower APY = longer runway
    
    **Disclaimer**
    
    Olympus Playgrounds is for educational purposes only and is not an individualized recommendation.
    Further Olympus Playgrounds are an educational tool and should not be relied upon as the primary basis for investment, financial, tax-planning, or retirement decisions.
    These metrics are not tailored to the investment objectives of a specific user.
    This educational information neither is, nor should be construed as, investment advice, financial guidance or an offer or a solicitation or recommendation to buy, sell, or hold any security, or to engage in any specific investment strategy by Olympus Playgrounds.
    These metrics used herein may change at any time and Olympus Playgrounds will not notify you when such changes are made. 
    You are responsible for doing your own diligence at all times.
    ''')
# endregion
