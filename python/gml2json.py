# to convert network in gml to json format for web visulization
import json
import networkx as nx
from networkx.readwrite import json_graph

import sys
sys.path.append('/Users/zichen/Documents/bitbucket/maayanlab_utils')

from fileIO import mysqlTable2dict
d_sename_umls = mysqlTable2dict('sep', 'side_effects', 2,1)

def gml2json(gml_fn, json_fn):
	G = nx.read_gml(gml_fn)
	print G.number_of_nodes(), G.number_of_edges()
	for node_id in G.nodes():
		node_dict = G.node[node_id]
		if '|' in node_dict['label']:
			sl = node_dict['label'].split('|')
			label = '%s (%s)'%( sl[1], sl[0] )
			G.node[node_id]['label'] = label
			
		# clean labels and add xref
		if node_dict['type'] == "SE":
			G.node[node_id]['type'] = 'triangle-up'
			G.node[node_id]['xref'] = d_sename_umls[node_dict['label']] # umls
		else:
			sl = G.node[node_id]['label'].split('(')
			xref = sl[-1]
			label = '('.join(sl[0:-1])
			label = label.strip()
			xref  = xref.strip(')')
			G.node[node_id]['label'] = label
			G.node[node_id]['xref'] = xref
			G.node[node_id]['type'] = 'circle'
		G.node[node_id]['id'] = node_dict['label']
		G.node[node_id]['size'] = G.degree(node_id)
	data = json_graph.node_link_data(G,attrs={'source': 'source', 'target': 'target', 'key': 'key', 'id': 'label'})
	json.dump(data, open(json_fn, 'wb'))


gml2json('../data/uberpheno_ADR_AUC_0.65_encv10_fdr.gml', '../data/pheno_ADR_network.json')
gml2json('../data/GO_SE_RLogit_75_0.35_new.gml', '../data/GO_ADR_network.json')

