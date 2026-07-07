import streamlit as st
import plotly.express as px
from data_processor import load_and_process_data

st.set_page_config(page_title="ECB Churn Dashboard", layout="wide")
st.title("🏦 European Banking Churn Analytics Portal")
st.markdown("### Interactive Demographic & Financial Risk Segmentation Tracker")

df = load_and_process_data()

# Sidebar Interactive Controls
st.sidebar.header("Filter Segment Cohorts")
selected_geo = st.sidebar.multiselect("Select Regions", options=df['Geography'].unique(), default=df['Geography'].unique())
selected_gender = st.sidebar.multiselect("Select Gender Profiles", options=df['Gender'].unique(), default=df['Gender'].unique())

# Dynamically slice data based on filter conditions
filtered_df = df[(df['Geography'].isin(selected_geo)) & (df['Gender'].isin(selected_gender))]

# Calculate dynamic KPIs
overall_churn = filtered_df['Exited'].mean() * 100
high_val_df = filtered_df[filtered_df['BalanceSegment'] == 'High-balance']
hval_churn = high_val_df['Exited'].mean() * 100 if len(high_val_df) > 0 else 0
capital_at_risk = high_val_df[high_val_df['Exited'] == 1]['Balance'].sum()

# Display dynamic KPIs across three cards
col1, col2, col3 = st.columns(3)
col1.metric("Dynamic Segment Churn Rate", f"{overall_churn:.2f}%")
col2.metric("High-Value Premium Churn Ratio", f"{hval_churn:.2f}%")
col3.metric("Capital Liquid Portfolio Risk", f"€{capital_at_risk:,.2f}")

st.markdown("---")

# Layout Interactive Analytical Tabs
tab1, tab2 = st.tabs(["Regional Risk Analytics", "Demographic Flight Matrix"])

with tab1:
    geo_data = filtered_df.groupby('Geography')['Exited'].mean().reset_index()
    geo_data['Exited'] *= 100
    fig_geo = px.bar(geo_data, x='Geography', y='Exited', text_auto='.1f', title="Geographic Risk Index Breakdown (%)", labels={'Exited':'Churn Rate %'})
    st.plotly_chart(fig_geo, use_container_width=True)

with tab2:
    age_tenure = filtered_df.groupby(['AgeGroup', 'TenureGroup'], observed=False)['Exited'].mean().reset_index()
    age_tenure['Exited'] *= 100
    fig_age = px.bar(age_tenure, x='AgeGroup', y='Exited', color='TenureGroup', barmode='group', title="Age Demographics vs Tenure Lifecycles Churn")
    st.plotly_chart(fig_age, use_container_width=True)
