#include "FindIsomorphicIndex.hpp"

#include <algorithm>

bool is_isomorphic(const UndirectedGraph & uGraph1, const UndirectedGraph & uGraph2) {
	vf2_callback<UndirectedGraph, UndirectedGraph> callback(uGraph1, uGraph2);

 	return vf2_graph_iso(uGraph1, uGraph2, callback);
}

int find_isomorphic_index(const Vector<Graph> & graphsIso, const UndirectedGraph & clgraph) {
	auto itIdx = std::find_if(graphsIso.begin(), graphsIso.end(), [&](const Graph & g) {
		return is_isomorphic(*g.get_ugraph(), clgraph);
	});

	return itIdx == graphsIso.end() ? -1 : itIdx - graphsIso.begin();
}
