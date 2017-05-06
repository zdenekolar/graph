import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

file = r'C:\Users\Zdenek\Dropbox\PhD\Connections.xlsx'
data = pd.read_excel(file, sheetname='Professions', converters={'Id': str}, index_col=0)


# data['Stages'] = list(map(int, data['Stages'].split(',')))


def show_contracts():
    '''
    Display Contractual Relationships between Project Participants.
    :return: None
    '''
    labels = {}
    G = nx.Graph()
    for i, record in enumerate(data.iterrows()):
        key = record[0]
        name = record[1]['Name']
        G.add_node(key, name=name)
        labels[key] = ''.join([name, ' ', key])

    for record in data.iterrows():
        name = record[0]
        appointed = record[1]['Appointed']
        if appointed is not None:
            G.add_edge(name, appointed)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, )
    nx.draw_networkx_labels(G, pos, labels=labels)
    plt.title('Contractual Relationships')

    plt.show()


def show_stage_participants(stage=0):
    '''
    Display all participants in a given stage.
    :return: None
    '''
    labels = {}
    G = nx.Graph()

    for record in data.iterrows():
        key = record[0]
        name = record[1]['Name']
        if type(record[1]['Stages']) == int:
            stages = record[1]['Stages'].split(',')
        else:
            stages = list(record[1]['Stages'])

        for s in stages:
            print('s', s)

            if s in stages:
                G.add_node(key, name=name)
                labels[key] = ''.join([name, ' ', key])


        for record in G.nodes():
            print('rec', record)
            name = record
            appointed = data.loc[record]['Appointed']
            print('app', appointed)
            # if appointed is not '-':
            #     G.add_edge(name, appointed)

    pos = nx.spring_layout(G)

    nx.draw(G, pos, )
    nx.draw_networkx_labels(G, pos, labels=labels)

    plt.show()

if __name__ == '__main__':
    # show_contracts()
    show_stage_participants(stage=1)
