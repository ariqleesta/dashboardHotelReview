import plotly.express as px
import pandas as pd

# ----------------- Hotel Name ---------------------#

def get_hotel_name(value='11 Cadogan Gardens'):
    return value

# ----------------- Address ---------------------#

def get_address(df, value='11 Cadogan Gardens'):
    search_data = df[df['Hotel_Name'] == value]
    search_data
    return search_data['Hotel_Address'].values[0]

# ----------------- Average Score ---------------------#

def get_average_score(df, value='11 Cadogan Gardens'):
    search_data = df[df['Hotel_Name'] == value]
    search_data
    return search_data['Average_Score'].values[0]

# ----------------- Total Number of Reviews ---------------------#

def get_num_review(df, value='11 Cadogan Gardens'):
    search_data = df[df['Hotel_Name'] == value]
    search_data
    return search_data['Total_Number_of_Reviews'].values[0]


# ----------------- Radar Graph ---------------------#

def sentiment_radar(df, value='11 Cadogan Gardens'):
    aspects = ['staff', 'room', 'breakfast', 'service', 'view', 'restaurant', 'bathroom', 'pool']

    search_data = df[df['Hotel_Name'] == value]

    data = pd.DataFrame(dict(
        r=search_data[aspects].T.values.flatten(),
        theta=search_data[aspects].T.index))
    fig = px.line_polar(data, r='r', theta='theta', line_close=True)

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=False
    )
    # fig.update_layout(title = 'Sentiment Scores of {} '.format(value),
    #                 title_font_size = 12)

    # fig.layout.template = 'plotly_dark'
    return fig