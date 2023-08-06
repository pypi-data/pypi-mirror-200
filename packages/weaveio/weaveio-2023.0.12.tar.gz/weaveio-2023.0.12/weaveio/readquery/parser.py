from collections import defaultdict
from copy import copy
from typing import List, Tuple, Dict
from pathlib import Path
import warnings

import networkx as nx
import pandas as pd
from astropy.table import Table

from .utilities import mask_infs, remove_successive_duplicate_lines, dtype_conversion
from .digraph import HashedDiGraph, plot_graph, add_start, add_traversal, add_filter, add_aggregation, add_operation, add_return, add_unwind, subgraph_view, get_above_state_traversal_graph, node_dependencies, add_node_reference
from .statements import StartingMatch, Traversal, NullStatement, Operation, GetItem, AssignToVariable, DirectFilter, CopyAndFilter, Aggregate, Return, Unwind, GetProduct, UnionTraversal, ApplyToList


class ParserError(Exception):
    pass


class DeadEndException(Exception):
    pass


def traverse(graph, start=None, end=None, done=None, ordering=None, views=None):
    """
    traverse the traversal_graph with backtracking
    """
    if views is None:
        dag = subgraph_view(graph, excluded_edge_type='wrt')
        backwards_graph = subgraph_view(graph, only_edge_type='wrt')
        traversal_graph = subgraph_view(dag, excluded_edge_type='dep')
        dep_graph = subgraph_view(graph, only_edge_type='dep')
        views = (dag, backwards_graph, traversal_graph, dep_graph)
    else:
        dag, backwards_graph, traversal_graph, dep_graph = views
    if start is None or end is None:
        naive_ordering = list(nx.topological_sort(dag))
        if start is None:
            start = naive_ordering[0]  # get top node
        if end is None:
            end = naive_ordering[-1]
    if ordering is None:
        ordering = [start]
    else:
        ordering = list(ordering)
    node = start
    done = set() if done is None else set(done)  # stores wrt edges and visited nodes
    while True:
        dependencies = dep_graph.predecessors(node)
        if not all(dep in done for dep in dependencies):
            raise DeadEndException
        options = [b for b in backwards_graph.successors(node) if (node, b) not in done]  # must do wrt first
        if not options:
            options = [o for o in traversal_graph.successors(node) if o not in done]   # where to go next?
            option_edges = [graph.edges[(node, o)] for o in options]
            op_options = []
            for o, e in zip(options, option_edges):
                if e.get('type', '') == 'operation' and e.get('single', False):
                    if all(dep in done for dep in dep_graph.predecessors(o)):
                        op_options.append(o)
            # do all operations first since they can't be wrong!
            options = op_options + [o for o in options if o not in op_options]
        if not options:
            # if you cant go anywhere and you're not done, then this recursive path is bad
            if node != end:
                raise DeadEndException
            else:
                return ordering, done
        elif len(options) == 1:
            # if there is only one option, go there... obviously
            edge = (node, options[0])
            if edge in done:
                # recursive path is bad if you have to go over the same wrt edge more than once
                raise DeadEndException
            elif graph.edges[edge]['type'] == 'wrt':
                done.add(edge)  # only add edges for wrt
                # and now also reset the branch listed in `ordering[iwrt:inode] so it can be traversed again`
                # only reset the nodes/edges which have other dep-paths outside the branch
                most_recent_mention = len(ordering) - ordering[::-1].index(options[0]) - 1
                this_branch = ordering[most_recent_mention:]
                still_todo = set(graph.nodes) - done - set(this_branch)
                restricted_dag = nx.subgraph_view(dag, lambda n: n != node)
                # TODO: also include this edge we are on now... might be needed later somehow
                for n in set(this_branch[:-1]):
                    if any(nx.has_path(restricted_dag, n, a) for a in still_todo):
                        done -= {n}
                        for wrt_edge in backwards_graph.successors(n):
                            done -= {(n, wrt_edge)}
            done.add(node)
            node = options[0]
            ordering.append(node)
        else:
            # open up recursive paths from each available option
            # this is such a greedy algorithm
            for option in options:
                try:
                    new_done = done.copy()
                    new_ordering = ordering.copy()
                    new_ordering.append(option)
                    new_done.add(node)
                    new_done.add(option)
                    ordering, new_done = traverse(graph, option, end, tuple(new_done), tuple(new_ordering), views)
                    done.update(new_done)
                    node = ordering[-1]
                    break
                except DeadEndException:
                    pass  # try another option
            else:
                raise DeadEndException  # all options exhausted, entire recursive path is bad


def verify_traversal(graph, traversal_order):
    edges = list(zip(traversal_order[:-1], traversal_order[1:]))
    if any(graph.edges[e]['type'] == 'dep' for e in edges):
        raise ParserError(f"Some dep edges where traversed. This is a bug")
    semi_dag = subgraph_view(graph, excluded_edge_type='dep')
    if set(semi_dag.edges) != set(edges):
        raise ParserError(f"Not all edges were traversed. This is a bug")
    done = set()
    for n in traversal_order:
        if n not in done:
            if not all(dep in done for dep in node_dependencies(graph, n)):
                raise ParserError(f"node {n} does not have all its dependencies satisfied. This is a bug")
            done.add(n)


def verify(graph):
    """
    Check that edges and nodes are allowed:
        - There is only one output node and one input node (no hanging nodes)
        - There is a path from input->output
        - can only aggregate to a parent
        - There are no cyclic dependencies in the dag
        - can only use an aggregation when it's wrt is a parent
        - all operations must be aggregated
        - Multiple inputs into a node should comprise:
            all deps that are aggregated
            one other (can be anything)
        - For an agg node, there is only one wrt
        - You can have > 1 inputs when they are ops

        - Multiple outputs from a node:
            no more than one out-path should be unaggregated in the end
            (i.e. there should only be one path from start-output which contains no aggregations)
    """
    dag = subgraph_view(graph, excluded_edge_type='wrt')
    traversal = subgraph_view(dag, excluded_edge_type='dep')
    if not nx.is_arborescence(traversal):
        raise ParserError(f"Invalid query: The DAG for this query is not a directed tree with max 1 parent per node")
    starts = [n for n in dag.nodes if dag.in_degree(n) == 0]
    ends = [n for n in dag.nodes if dag.out_degree(n) == 0]
    if len(starts) != 1:
        raise ParserError("Only one input node is allowed")
    if len(ends) > 1:
        raise ParserError("Only one output node is allowed")
    if not ends:
        raise ParserError("An output node is required")
    backwards = subgraph_view(graph, only_edge_type='wrt')
    without_agg = subgraph_view(traversal, excluded_edge_type='aggr')
    main_paths = nx.all_simple_paths(without_agg, starts[0], ends[0])
    try:
        next(main_paths)
        next(main_paths)
    except StopIteration:
        pass
    else:
        # there can be 0 in the case where the output is itself an aggregation
        raise ParserError(f"There can only be at maximum one path from {starts[0]} to {ends[0]} that is not aggregated")
    if not nx.is_directed_acyclic_graph(dag):
        raise ParserError(f"There are cyclical dependencies")
    if not nx.has_path(dag, starts[0], ends[0]):
        raise ParserError(f"There must be a path from {starts[0]} to {ends[0]}")
    for agg, wrt in backwards.edges:
        if not nx.has_path(graph, wrt, agg):
            raise ParserError(f"{wrt} must be a parent of {agg} in order to aggregate")
        for node in dag.successors(agg):
            if not nx.has_path(graph, wrt, node):
                raise ParserError(f"{node} can an only use what is aggregated above it. failure on {agg} (parent={wrt})")
    for node in graph.nodes:
        inputs = [graph.edges[i]['type'] for i in graph.in_edges(node)]
        inputs = [i for i in inputs if i != 'wrt']
        outputs = [graph.edges[i]['type'] for i in graph.out_edges(node)]
        if sum(o == 'wrt' for o in outputs) > 1:
            raise ParserError(f"Cannot put > 1 wrt paths as output from an aggregation: {node}")
        outputs = [o for o in outputs if o != 'wrt']
        nfilters = sum(i == 'filter' for i in inputs)
        ntraversals = sum(i == 'traversal' for i in inputs)
        ndeps = sum(i == 'dep' for i in inputs)
        nops = sum(i == 'operation' for i in inputs)
        naggs = sum(i == 'aggr' for i in inputs)
        nreturns = sum(i == 'return' for i in inputs)
        if naggs > 1:
            raise ParserError(f"Cannot aggregate more than one node at a time: {node}")
        elif naggs:
            if not all(o in ['dep', 'operation', 'aggr'] for o in outputs):
                raise ParserError(f"Can only use aggregations as a dependency/operation/aggregation afterwards {node}")
        if nfilters > 2:
            raise ParserError(f"Can only have one filter input: {node}")
        elif nfilters:
            if ntraversals + nops + naggs > 0:
                raise ParserError(f"A filter can only take dependencies not traversals/ops/aggregations: {node}")
        if ntraversals > 2:
            raise ParserError(f"Can only have one traversal input: {node}")
        elif ntraversals:
            if len(inputs) > 2:
                raise ParserError(f"Can only traverse with one input or one input and one unwind: {node}")
        if nops > 1:
            raise ParserError(f"Can only have one op input: {node}")
        elif nops:
            try:
                if graph.edges[list(graph.out_edges(node))[0]]['type'] not in ['aggr', 'operation']:
                    raise ParserError(f"All operations must be aggregated back at some point: {node}")
            except IndexError:
                raise ParserError(f"All operations must be aggregated back at some point: {node}")
            if ntraversals + naggs + nfilters > 1:
                raise ParserError(f"Can only have dependencies as input for an operation: {node}")


def merge_attribute_forks(graph):
    """
    Given a node in the graph find simple (no external deps) successor branches which wrt back to the same node.
    Merge these parallel branches into one serial branch
    """


def simplify_graph(graph: HashedDiGraph):
    return graph


class QueryGraph:
    """
    Rules of adding nodes/edges:
    Traversal:
        Can only traverse to another hierarchy object if there is a path between them
        Always increases/maintains cardinality
    Aggregation:
        You can only aggregate back to a predecessor of a node (the parent)
        Nodes which require another aggregation node must share the same parent as just defined above

    Golden rule:
        dependencies of a node must share an explicit parent node
        this basically says that you can only compare nodes which have the same parents

    optimisations:
        If the graph is duplicated in multiple positions, attempt to not redo effort
        For instance, if you traverse and then agg+filter back to a parent and the traverse the same path
        again after filtering, then the aggregation is changed to conserve the required data and the duplicated traversal is removed

    """

    def __init__(self):
        self.G = HashedDiGraph()
        self.start = add_start(self.G, 'data')
        self.variable_names = defaultdict(int)
        self.dag_G = nx.subgraph_view(self.G, filter_edge=lambda a, b: self.G.edges[(a, b)]['type'] != 'wrt')  # type: nx.DiGraph
        self.backwards_G = nx.subgraph_view(self.G, filter_edge=lambda a, b: self.G.edges[(a, b)]['type'] == 'wrt')  # type: nx.DiGraph
        self.traversal_G = nx.subgraph_view(self.G, filter_edge=lambda a, b: self.G.edges[(a, b)]['type'] != 'dep')  # type: nx.DiGraph
        self.parameters = {}
        self.groupbys = {}

    def statements(self, node):
        if node is None:
            G = self.G
        else:
            G = self.restricted(node)
        return {d['statement']: (a, b) for a, b, d in G.edges(data=True) if 'statement' in d}

    def latest_shared_ancestor(self, *nodes):
        if all(n == nodes[0] for n in nodes):
            return nodes[0]
        return sorted(set.intersection(*[self.above_state(n, no_wrt=True) for n in nodes]), key=lambda n: len(nx.ancestors(self.traversal_G, n)))[-1]

    def latest_object_node(self, *nodes):
        """
        a and b have a shared ancestor
        Scenarios:
            a = single; b = single -> shared
            a = single; b = plural -> choose originating object of b
            a = plural; b = single -> choose ordering object of a
            a = plural; b = plural -> disallowed [at least one must be aggregated back]
        """
        cardinals = []
        for node in nodes:
            try:
                cardinal = next(self.backwards_G.successors(node))
            except StopIteration:
                cardinal = node
            cardinals.append(cardinal)

        shared = self.latest_shared_ancestor(*cardinals)
        is_shared = [shared == c for c in cardinals]
        if all(is_shared):
            return shared
        if sum(is_shared) == len(is_shared) - 1:
            for c, i in zip(cardinals, is_shared):
                if not i:
                    return c
        else:
            raise ParserError(f"One of {nodes} must be a parent of the other. {shared} not in {nodes} ")

    def is_singular_branch(self, a, b):
        path = nx.shortest_path(self.above_graph, b, a)
        return all(self.above_graph.edges[(b, a)].get('single', True) for b, a in zip(path[:-1], path[1:]))

    def is_singular_branch_relative_to_splits(self, node):
        path = nx.shortest_path(self.above_graph, node, self.start)
        for b, a in zip(path[:-1], path[1:]):
            edge = self.above_graph.edges[(b, a)]
            if edge.get('split_node', False):
                return True
            if not edge.get('single', True):
                return False
        return True  # if we get to this point, we're at the start node and all edges are single



    @property
    def above_graph(self):
        return get_above_state_traversal_graph(self.G)

    def node_holds_type(self, node, *types):
        return any(d['type'] in types for a, b, d in self.G.in_edges(node, data=True))

    def get_host_nodes_for_operation(self, op_node) -> set:
        """
        Find nodes which are necessary to construct `op_node`
        traverses until it encounters a traversal/filter/aggr then it stops
        An operation can have a single path (just scalar ops) or a branching mess (combining ops),
        """
        necessary = set()
        for input_edge in self.dag_G.in_edges(op_node, data=True):
            input = input_edge[0]
            if self.node_holds_type(input, 'traversal', 'filter', 'aggr'):
                necessary.add(input)
            else:
                necessary |= self.get_host_nodes_for_operation(input)
        return necessary

    def above_state(self, node, no_wrt=False):
        states = nx.descendants(self.above_graph, node)
        states.add(node)
        if not no_wrt:
            for n in states.copy():
                aggregates = self.backwards_G.predecessors(n)
                for aggr in aggregates:
                    edge = list(self.traversal_G.in_edges(aggr))[0]
                    if isinstance(self.G.edges[edge]['statement'], NullStatement):
                        # this is a fake aggregation so get all required nodes as well
                        # TODO: do not do this if the branch is not SINGLE!
                        op_stuff = self.get_host_nodes_for_operation(aggr)
                        states |= op_stuff
                    else:
                        states.add(aggr)
        return states

    def get_variable_name(self, name):
        name = name.lower()
        new_name = f'{name}{self.variable_names[name]}'
        self.variable_names[name] += 1
        return new_name

    def export(self, fname, result_node=None, directory=None, highlight_nodes=None,
               highlight_edges=None, ftype='pdf'):
        return plot_graph(self.restricted(result_node), highlight_nodes, highlight_edges).\
            render(fname, directory, format=ftype)

    def export_slideshow(self, dirname, ordering, result_node=None):
        Path(dirname).mkdir(parents=True, exist_ok=True)
        for i, (a, b) in enumerate(zip(ordering[:-1], ordering[1:])):
            self.export(f'{i}', result_node, dirname, [b], [(a, b)], ftype='png')

    def add_start_node(self, node_type, unwound=None):
        parent_node = self.start
        statement = StartingMatch(node_type, unwound, self)
        return add_traversal(self.G, parent_node, statement, unwound=unwound)

    def add_traversal(self, parent_node, paths: List[str], end_node_type: str, single=False, unwound=None):
        statement = Traversal(self.G.nodes[parent_node]['variables'][0], end_node_type, paths, unwound, self)
        return add_traversal(self.G, parent_node, statement, single=single, unwound=unwound)

    def fold_to_cardinal(self, parent_node, wrt=None):
        """
        Adds a fake aggregation such that a node can be used as a dependency later.
        For operation chains, you follow the traversal route backwards.
        If the node
        """
        agg = next(self.backwards_G.successors(parent_node), None)
        if wrt is None:
            if agg is not None:
                return parent_node  # if its already aggregated then do nothing
            else:
                path = nx.shortest_path(self.traversal_G, self.start, parent_node)[::-1]
                for b, a in zip(path[:-1], path[1:]):
                    if not self.G.edges[(a, b)]['single']:
                        wrt = b
                        break
                else:
                    raise ParserError
        elif agg == wrt:
            return parent_node
        if wrt == parent_node:
            return parent_node
        return self.add_aggregation(parent_node, wrt, 'aggr')

    def add_scalar_operation(self, parent_node, op_format_string, op_name, parameters=None) -> Tuple:
        """
        A scalar operation is one which takes only one input and returns one output argument
        the input can be one of [object, operation, aggregation]
        """
        if any(d['type'] == 'aggr' for a, b, d in self.G.in_edges(parent_node, data=True)):
            wrt = next(self.backwards_G.successors(parent_node))
            return self.add_combining_operation(op_format_string, op_name, parent_node, wrt=wrt, parameters=parameters)
        statement = Operation(self.G.nodes[parent_node]['variables'][0], [], op_format_string, op_name, self, parameters)
        return add_operation(self.G, parent_node, [], statement), parent_node

    def add_combining_operation(self, op_format_string, op_name, *nodes, wrt=None, parameters=None) -> Tuple:
        """
        A combining operation is one which takes multiple inputs and returns one output
        Operations should be inline (no variables) for as long as possible.
        This is so they can be used in match where statements
        """
        # if this is combiner operation, then we do everything with respect to the nearest ancestor
        dependency_nodes = [self.fold_to_cardinal(d) for d in nodes]  # fold back when combining
        if wrt is None:
            wrt = self.latest_object_node(*dependency_nodes)
        deps = [self.G.nodes[d]['variables'][0] for d in dependency_nodes]
        statement = Operation(deps[0], deps[1:], op_format_string, op_name, self, parameters)
        return add_operation(self.G, wrt, dependency_nodes, statement), wrt

    def add_getitem(self, parent_node, item, which=0):
        statement = GetItem(self.G.nodes[parent_node]['variables'][which], item, self)
        return add_operation(self.G, parent_node, [], statement)

    def add_getproduct(self, parent_node, item):
        statement = GetProduct(self.G.nodes[parent_node]['variables'][0], item, self)
        return add_operation(self.G, parent_node, [], statement)

    def assign_to_variable(self, parent_node, only_if_op=False):
        if only_if_op and any(d['type'] in ['operation', 'aggr'] for a, b, d in self.G.in_edges(parent_node, data=True)):
            stmt = AssignToVariable(self.G.nodes[parent_node]['variables'][0], self)
            return add_operation(self.G, parent_node, [], stmt)
        return parent_node

    def add_generic_aggregation(self, parent_node, wrt_node, op_format_string, op_name,
                                remove_infs=None, expected_dtype=None, input_dtype=None):
        if expected_dtype is not None:
            op_format_string = dtype_conversion(input_dtype, expected_dtype, op_format_string, '{0}')
        if remove_infs:
            op_format_string = op_format_string.format(mask_infs('{0}'))
        if wrt_node == parent_node or op_name == 'aggr':
            statement = NullStatement(self.G.nodes[parent_node]['variables'] + [wrt_node], self)
        else:
            if wrt_node not in nx.ancestors(self.dag_G, parent_node):
                raise SyntaxError(f"{parent_node} cannot be aggregated to {wrt_node} ({wrt_node} is not an ancestor of {parent_node})")
            statement = Aggregate(self.G.nodes[parent_node]['variables'][0], wrt_node, op_format_string, op_name, self)
        previous = next(self.backwards_G.successors(parent_node), parent_node)
        dependencies = [] if previous == parent_node else [parent_node]
        return add_aggregation(self.G, previous, wrt_node, statement, dependencies=dependencies)

    def add_aggregation(self, parent_node, wrt_node, op, remove_infs=None, expected_dtype=None, input_dtype=None, distinct=False, nulls=False):
        dst = 'distinct ' if distinct else ''
        if nulls:
            aggr = f"[i in collect({dst}[{{0}}]) | i[0]]"
        else:
            aggr = f"{op}({dst}{{0}})"
        return self.add_generic_aggregation(parent_node, wrt_node, aggr, op, remove_infs, expected_dtype, input_dtype)

    def add_predicate_aggregation(self, parent, wrt_node, op_name):
        op_format_string = f'{op_name}(x in collect({{0}}) where toBoolean(x))'
        return self.add_generic_aggregation(parent, wrt_node, op_format_string, op_name)

    def add_filter(self, parent_node, predicate_node, direct=False, force_single=False, split_node=False):
        wrt = self.latest_shared_ancestor(parent_node, predicate_node)
        predicate_node = self.fold_to_cardinal(predicate_node, wrt)  # put everything back to most recent shared ancestor
        if not nx.has_path(self.G, predicate_node, parent_node):
            raise SyntaxError(f"{parent_node} cannot be filtered by {predicate_node} since there is no direct path between them")
        predicate = self.G.nodes[predicate_node]['variables'][0]
        if direct:
            FilterClass = DirectFilter
        else:
            FilterClass = CopyAndFilter
        statement = FilterClass(self.G.nodes[parent_node]['variables'][0], predicate, self)
        return add_filter(self.G, parent_node, [predicate_node], statement, force_single, split_node=split_node)

    def add_apply_to_list(self, parent_node, list_variable, apply_function, filter_function,
                          *dependencies, put_null_in_empty=False, parameters=None):
        dependencies = [self.fold_to_cardinal(d) for d in dependencies]
        statement = ApplyToList(list_variable, [self.G.nodes[d]['variables'][0] for d in dependencies],
                                apply_function, filter_function, self, put_null_in_empty, parameters=parameters)
        return add_operation(self.G, parent_node, dependencies, statement), statement.output_variables[0]

    def add_unwind_parameter(self, wrt_node, to_unwind, *dependencies, parameters=None):
        statement = Unwind(wrt_node, to_unwind, 'unwound', self, parameters=parameters)
        return add_unwind(self.G, wrt_node, statement, *dependencies)

    def collect_or_nots(self, index_node, other_nodes, force_plurals, treat_equal, already_aggregated_to_index):
        """
        Collect `other_node` with respect to the shared common ancestor of `index_node` and `other_node`.
        If other_node is above the index, fold back to cardinal node
        if not, fold back to shared ancestor
        """
        # successors = [next(self.backwards_G.successors(n, None)) for n in other_nodes]
        # shareds = [self.latest_shared_ancestor(index_node, n) for n in other_nodes]
        if already_aggregated_to_index:
            return other_nodes
        results = []
        for other_node, force_plural in zip(other_nodes, force_plurals):
            successor = next(self.backwards_G.successors(other_node), None)
            if not force_plural and successor == index_node:
                # if its not already aggregated to the index
                if treat_equal:
                    return other_nodes
                results.append(other_node)
                continue
            shared = self.latest_shared_ancestor(index_node, other_node)
            if force_plural:
                if treat_equal:
                    return [self.add_aggregation(o, shared, 'collect') for o in other_nodes]
                results.append(self.add_aggregation(other_node, shared, 'collect'))
            else:
                if successor == shared:
                    if treat_equal:
                        return other_nodes
                    results.append(other_node)
                else:
                    how = 'aggr' if self.is_singular_branch(shared, other_node) else 'collect'
                    if treat_equal:
                        return [self.add_aggregation(o, shared, how) for o in other_nodes]
                    results.append(self.add_aggregation(other_node, shared, how))
        return results

    def add_results_table(self, index_node, column_nodes, force_plurals: List[bool], dropna=None,
                          treat_equal=False, already_aggregated_to_index=False):
        # fold back column data into the index node
        column_nodes = self.collect_or_nots(index_node, column_nodes, force_plurals, treat_equal, already_aggregated_to_index) # fold back when combining
        deps = [self.G.nodes[d]['variables'][0] for d in column_nodes]
        try:
            vs = self.G.nodes[index_node]['variables'][0]
        except IndexError:
            vs = None
        if dropna is None:
            try:
                dropna = self.G.nodes[index_node]['variables'][0]
            except IndexError:
                dropna = None
        else:
            dropna = self.G.nodes[dropna]['variables'][0]
        statement = Return(deps, vs, dropna, self)
        collected = [list(self.G.in_edges(c, data='type'))[0][-1] == 'collect' for c in column_nodes]
        return add_return(self.G, index_node, column_nodes, statement), collected

    def add_scalar_results_row(self, *column_nodes):
        """data already folded back"""
        deps = [self.G.nodes[d]['variables'][0] for d in column_nodes]
        statement = Return(deps, None, [], self)
        return add_return(self.G, self.start, column_nodes, statement)

    def add_groupby(self, query):
        name = self.add_parameter('<placeholder>', 'group')
        self.groupbys[name] = query
        return name

    def add_parameter(self, value, name=None):
        if isinstance(value, pd.DataFrame):
            value = Table.from_pandas(value)
        if isinstance(value, Table):
            # limit column multidimensional sizes to 100
            allowed_cols = [c for c in value.colnames if sum(value[c].shape) / len(value) <= 100]
            if allowed_cols != value.colnames:
                warnings.warn(f"Columns {set(value.colnames) - set(allowed_cols)} were dropped due to size limitations (>=100)")
                value = value[allowed_cols]
        # if value in self.parameters.values():
        #     return [k for k, v in self.parameters.items() if v is value][0]
        for k, v in self.parameters.items():
            if value is v:
                return k
        name = f'${name}' if name is not None else '$'
        varname = self.get_variable_name(name)
        self.parameters[varname] = value
        return varname

    def add_previous_reference(self, parent_node, node_to_reference):
        vars = self.G.nodes[node_to_reference]['variables']
        return add_node_reference(self.G, NullStatement(vars, self), parent_node, node_to_reference)

    def restricted(self, result_node=None) -> HashedDiGraph:
        if result_node is None:
            return nx.subgraph_view(self.G)
        return nx.subgraph_view(self.G, lambda n: nx.has_path(self.dag_G, n, result_node))

    def dependency_parameters(self, result_node):
        ps = set()
        for statement in self.statements(result_node):
            if statement.parameters is not None:
                ps |= set(statement.parameters)
        return {k: v for k, v in self.parameters.items() if k in ps}

    def traverse_query(self, result_node=None, simplify=True):
        graph = self.restricted(result_node)
        # verify(graph)
        if simplify:
            graph = simplify_graph(graph)
        return traverse(graph)[0]

    def verify_traversal(self, goal, ordering, simplify=True):
        graph = self.restricted(goal)
        if simplify:
            graph = simplify_graph(graph)
        return verify_traversal(graph, ordering)

    def cypher_lines(self, result, no_cache=False):
        try:
            cypher = self.G.nodes[result]['cypher']
            ordering = self.G.nodes[result]['ordering']
        except KeyError:
            ordering = self.traverse_query(result)
            self.verify_traversal(result, ordering)
            statements = []
            for i, e in enumerate(zip(ordering[:-1], ordering[1:])):
                try:
                    statement = self.G.edges[e]['statement'].make_cypher(ordering[:i+1])
                    if statement is not None:
                        statements.append(statement)
                except KeyError:
                    pass
            cypher = remove_successive_duplicate_lines(statements)
            if not no_cache:
                self.G.nodes[result]['cypher'] = cypher
                self.G.nodes[result]['ordering'] = ordering
        return copy(cypher)

    def node_is_null_statement(self, node):
        if self.node_holds_type(node, 'aggr'):
            return any(isinstance(d.get('statement', None), NullStatement) for _, _, d in self.G.in_edges(node, data=True))
        return False

    def get_unwind_variables(self, until_node):
        variables = {d['statement'].parameter: d['statement'].output for *e, d in self.restricted(until_node).edges(data=True) if isinstance(d.get('statement', None), Unwind)}
        return {p: v for k, v in variables.items() for p in sorted(self.parameters.keys(), key=len, reverse=True) if p in k}
