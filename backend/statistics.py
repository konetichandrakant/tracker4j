import pandas as pd 
import plotly
import plotly.express as px
import plotly.graph_objects as go
import json

def build_dashboard(app, career): 

    df = pd.DataFrame(app)
    groupings = df.groupby('status')['_id'].count().reset_index().rename(columns={'status': 'Job Status', '_id' : 'count'})
    groupings = groupings.append({'Job Status' : 'Career Fairs', 'count': len(pd.DataFrame(career))}, ignore_index=True)

    fig = px.bar(groupings, x="Job Status", y="count", barmode="group", width=800)

    return plotly.io.to_json(fig, pretty=True)

def build_indicators(applications, careers, email): 

    df = pd.DataFrame(applications)
    numMe = len(df[df['email'] == email])
    numTotal = round(df.groupby('email')['_id'].count().mean(), 2)

    dff = pd.DataFrame(careers)
    numCareerMe = len(dff[dff['email'] == email])
    numCareerTotal = round(dff.groupby('email')['_id'].count().mean(), 2)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = numMe,
        domain = {'x': [0, 0.5], 'y': [0, 1]},
        title = {"text": "Application Tracker"},
        delta = {'reference': numTotal, 'relative': True, 'position' : "top"}))

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = numCareerMe,
        delta = {'reference': numCareerTotal, 'relative': True},
        title = {"text": "Career Fair Tracker"},
        domain = {'x': [.6, 1], 'y': [0, 1]}))

    fig.update_layout(paper_bgcolor = "lightgray", width = 800, height = 300)

    return plotly.io.to_json(fig, pretty=True)