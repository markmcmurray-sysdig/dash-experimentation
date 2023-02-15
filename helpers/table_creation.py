from dash import dash_table


#
# def generate_table(dataframe, agent_version='12.10.0-rc2'):
#     return dash_table.DataTable(
#         dataframe.query(f'AGENT_VERSION=="{agent_version}"').to_dict('records'),
#         [{"name": i, "id": i} for i in dataframe.drop(['AGENT_VERSION'], axis=1).columns])

def generate_table(dataframe, agent_version='12.10.0-rc2'):
    return dash_table.DataTable(
        dataframe.query(f'AGENT_VERSION=="{agent_version}"').to_dict('records'))


def generate_tables(dataframe, agent_version='12.10.0-rc2', grouping='CLUSTER_TYPE', arch_compatability=None):
    query_string = f'AGENT_VERSION=="{agent_version}"'
    if arch_compatability:
        query_string += f'& ARCHITECTURE=="{arch_compatability}"'
    groups = list(dataframe.query(query_string).groupby(grouping))

    grouping_names = [group[0] for group in groups]
    tables = [dash_table.DataTable(group[1].drop(['AGENT_VERSION', grouping], axis=1).to_dict('records')) for group in groups]

    val = [None] * (len(grouping_names) + len(tables))
    val[::2] = grouping_names
    val[1::2] = tables

    return val