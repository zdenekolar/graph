import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# import seaborn as sns

file = r'Connections.xlsx'
data = pd.read_excel(file, sheetname='Professions', converters={'Id': str, 'Stages':str, 'Appointed':str}, index_col=0)


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

def _is_in_stage(stage):
    keys = []
    for record in data.iterrows():
        name = record[0]
        string = record[1]['Stages']
        stages = [int(num) for num in string.split(',')]
        if stage in stages:
            keys.append(name)
    return keys

def _get_attribute(attribute=None, to_integer=False):
    atts = {}
    for record in data.iterrows():
        key = record[0]
        string = record[1][attribute]
        if string is not '-' and to_integer:
            values = [int(num) for num in string.split(',')]
        elif type(string) == float:
            values = string
        else:
            values = string.split(',')

        atts[key] = values
    return atts

def show_stage_participants(stage=0):
    '''
    Display all participants in a given stage.
    :return: None
    '''
    labels = {}
    node_sizes = []
    G = nx.Graph()

    keys = _is_in_stage(stage=stage)
    att_app = _get_attribute('Appointed')
    att_imp = _get_attribute('Importance')

    for key in keys:
        G.add_node(key)
        description = data.loc[key][0]
        labels[key] = ''.join([description, ' ', key])
        node_sizes.append(att_imp[key]*300)

    for key in keys:
        for item in att_app[key]:
            if item is not '-':
                G.add_edge(key, item)

    pos = nx.spring_layout(G)
    nx.draw_networkx(G, pos, node_size=node_sizes, labels=labels, with_labels=True, alpha=0.8)
    # nx.draw_networkx_labels(G, pos, labels=labels, node_sizes=node_sizes)

    plt.show()

if __name__ == '__main__':
    # show_contracts()
    show_stage_participants(stage=1)
    # ret = _is_in_stage(1)
    # print(ret)
