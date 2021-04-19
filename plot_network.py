import pandas as pd
from nltk import ngrams
import networkx as nx
import itertools
import collections
import plotly.graph_objects as go

# ----------------- Plot Network ---------------------#

# Function to create ngrams (for only 1 topics)
def create_ngrams(text_array, n, aspect):
    terms_ngram = [list(ngrams(w, n)) for w in [text_array]]
    ngram = [i for i in terms_ngram[0] if aspect in i]
    return ngram


# create_ngrams(example, 2, aspect = 'room')

def ngrams_flatten(ngram):
    # Flatten list of bigrams in clean tweets
    ngram = list(itertools.chain(*ngram))
    return ngram


# Function to count the frequency
def ngrams_frequency(ngram, num_most_common):
    ngram_counts = collections.Counter(ngram)
    ngram_df = pd.DataFrame(ngram_counts.most_common(num_most_common),
                            columns=['ngram', 'count'])
    return ngram_df

# Create network plot

def plotly_network(dataframe, aspect):
    try:
        # transform to dict first
        d = dataframe.set_index('ngram').T.to_dict('records')
        d[0]
        G = nx.Graph()

        # Create connections between nodes
        for k, v in d[0].items():
            G.add_edge(k[0], k[1], weight=(v * 10))

        # Getting positions for each node.
        pos = nx.spring_layout(G, k=0.5, iterations=50)

        # Adding positions of the nodes to the graph
        for n, p in pos.items():
            G.nodes[n]['pos'] = p

        # Adding nodes and edges to the plotly api
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        node_trace = go.Scatter(
            x=[],
            y=[],
            text=[],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='inferno',
                reversescale=True,
                color=[],
                size=7,
                colorbar=dict(
                    thickness=10,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line=dict(width=0)))

        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])

        # Coloring based on the number of connections of each node
        for node, adjacencies in enumerate(G.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = adjacencies[0] + ' # of connections: ' + str(len(adjacencies[1]))
            node_trace['text'] += tuple([node_info])

            # Plotting the figure
        fig = go.Figure(data=[edge_trace, node_trace],
                        # text = node_trace['text'],
                        layout=go.Layout(
                            title='<br>Words Correlation of {}'.format(aspect.capitalize()),
                            titlefont=dict(size=12),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            # annotations=[ dict(
                            #    text="No. of connections",
                            #    showarrow=False,
                            #    xref="paper", yref="paper") ],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

        fig.add_trace(go.Scatter(
            x=node_trace['x'],
            y=node_trace['y'],
            mode="text",
            name="Lines and Text",
            text=[i.split()[0] for i in node_trace['text']],
            textposition="top center",
        ))

        # fig.layout.template = 'plotly_dark'

        return fig

    except:
        return "No Particular Topic"




def word_correlation_plot(df, value='11 Cadogan Gardens', aspect='staff', ngrams=3, size=30):
    search_data = df[df['Hotel_Name'] == value]
    search_data

    return plotly_network(
        ngrams_frequency(create_ngrams(search_data['Review'].values[0].split(), ngrams, aspect=aspect), size), aspect)

