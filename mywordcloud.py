from wordcloud import WordCloud
import plotly.express as px
import matplotlib.pyplot as plt

# ----------------- WordCloud Draw ---------------------#

def wordcloud_draw(df, value='11 Cadogan Gardens'):
    search_data = df[df['Hotel_Name'] == value]
    color = 'white'
    words = search_data['Review'].values[0]

    wordcloud = WordCloud(
        collocations=False,
        background_color=color,
        width=600,
        height=600
    ).generate(words)

    fig = px.imshow(wordcloud, width=300, height=300)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    plt.axis('off')
    # fig.layout.template = 'white'

    # fig.update_layout(title = 'Sentiment Scores of {} '.format(value),
    #                 title_font_size = 12)
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )
    return fig

