'''
@author: Sougata Saha
Institute: University at Buffalo
'''
from builtins import set

from tqdm import tqdm
from preprocessor import Preprocessor
from indexer import Indexer
from collections import OrderedDict
from linkedlist import LinkedList
import inspect as inspector
import sys
import argparse
import json
import time
import random
import flask
from flask import Flask
from flask import request
import hashlib

app = Flask(__name__)


class ProjectRunner:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.indexer = Indexer()

    def sort_type(self, li):
        return li[1]

    def _merge(self, p1, p2, op_type = 'no_skip', compare = 0):
        """ Implement the merge algorithm to merge 2 postings list at a time.
            Use appropriate parameters & return types.
            While merging 2 postings list, preserve the maximum tf-idf value of a document.
            To be implemented."""
        """p1, p2: linkedlist; op_type: skip or no_skip operation; compare: count of comparisons
        """
        op_type = 'no_skip'
        if op_type == 'skip':
            p1.add_skip_connections()
            p2.add_skip_connections()
        merge_ll = LinkedList()
        merge_ll_tfidf = LinkedList()
        t1 = p1.start_node
        t2 = p2.start_node
        while t1 is not None and t2 is not None:
            v1 = t1.value
            v2 = t2.value
            compare += 1
            if v1 == v2:
                insert_node = t1
                if t1.tf_idf < t2.tf_idf:
                    insert_node = t2
                merge_ll.insert_at_end(value=insert_node.value, tf_idf=insert_node.tf_idf)
                merge_ll_tfidf.insert_at_end(value=insert_node.tf_idf, tf_idf=insert_node.value)
                if op_type == 'skip':
                    t1 = t1.skip
                    t2 = t2.skip
                else:
                    t1 = t1.next
                    t2 = t2.next
            if v1 < v2:
                if op_type == 'skip':
                    t1 = t1.skip
                else:
                    t1 = t1.next
            if v2 < v1:
                if op_type == 'skip':
                    t2 = t2.skip
                else:
                    t2 = t2.next
        if op_type == 'skip':
            merge_ll.add_skip_connections()
            merge_ll_tfidf.add_skip_connections()
        return merge_ll, compare, merge_ll_tfidf


    def _daat_and(self, term_arr, op_type):
        """ Implement the DAAT AND algorithm, which merges the postings list of N query terms.
            Use appropriate parameters & return types.
            To be implemented."""
        posting_dict = OrderedDict({})
        ll_len_list = []
        return_list = []
        return_list_sorted = []
        comparison = 0
        if len(term_arr) <= 1:
            return_list = self._get_postings(term_arr[0])
            return return_list, comparison, return_list, comparison

        for term in term_arr:
            if self.indexer.inverted_index.get(term):
                posting_dict[term] = self.indexer.inverted_index[term]
                ll_len_list.append([term, posting_dict[term].length])
        # print("before sorting",ll_len_list)
        ll_len_list.sort(key=self.sort_type)
        search_ll = [self.indexer.inverted_index[ll_len_list[0][0]]]
        search_ll.append(comparison)
        search_ll.append([])
        for i in range(len(ll_len_list)-1):
            p1 = search_ll[0]
            p2 = self.indexer.inverted_index[ll_len_list[i+1][0]]
            search_ll[0], search_ll[1], search_ll[2] = self._merge(p1, p2, op_type, compare=search_ll[1])
        # print("after sorting",ll_len_list)
        # if op_type == 'no_skip':
        return_list = search_ll[0].traverse_list()
        comparison = search_ll[1]
        return_list_sorted = [x[1] for x in search_ll[2].traverse_with_tf_idf()]
        return_list_sorted.reverse()
        # else:
        #     return_list = search_ll[0].traverse_skips()
        #     comparison = search_ll[1]
        #     return_list_sorted = [x[1] for x in search_ll[2].traverse_skips_tfidf()]
        #     return_list_sorted.reverse()
        # return_list_sorted = sorted((search_ll[0].traverse_with_tf_idf()), key=self.sort_type, reverse=True)
        # return_list_sorted = [x[0] for x in return_list_sorted]
        return return_list, comparison, return_list_sorted, comparison


    def _get_postings(self, term):
        """ Function to get the postings list of a term from the index.
            Use appropriate parameters & return types.
            To be implemented."""
        postings = []
        if self.indexer.get_index().get(term):
            postings = self.indexer.get_index()[term].traverse_list()
        return postings

    def _output_formatter(self, op):
        """ This formats the result in the required format.
            Do NOT change."""
        if op is None or len(op) == 0:
            return [], 0
        op_no_score = [int(i) for i in op]
        results_cnt = len(op_no_score)
        return op_no_score, results_cnt

    def run_indexer(self, corpus):
        """ This function reads & indexes the corpus. After creating the inverted index,
            it sorts the index by the terms, add skip pointers, and calculates the tf-idf scores.
            Already implemented, but you can modify the orchestration, as you seem fit."""
        with open(corpus, 'r') as fp:
            for line in tqdm(fp.readlines()):
                doc_id, document = self.preprocessor.get_doc_id(line)
                tokenized_document = self.preprocessor.tokenizer(document)
                # self.indexer.token_count = tokenized_document.__len__()
                self.indexer.doc_details[doc_id] = len(tokenized_document)
                self.indexer.generate_inverted_index(doc_id, tokenized_document)
        self.indexer.sort_terms()
        self.indexer.add_skip_connections()
        self.indexer.calculate_tf_idf()
        # with open('data/temp_output.txt','w') as fp:
        #     for i in self.indexer.get_index().keys():
        #         text = i + str(self.indexer.get_index()[i].traverse_list())
        #         fp.write(text)
        query_list = ['coronavirus the novel coronavirus',' pandemic from an epidemic to a pandemic',
                      'is hydroxychloroquine effective?']
        random_command = "self.indexer.get_index()['random'].traverse_list()"
        self.run_queries(query_list, random_command)
        exit(10)

    def sanity_checker(self, command):
        """ DO NOT MODIFY THIS. THIS IS USED BY THE GRADER. """

        index = self.indexer.get_index()
        kw = random.choice(list(index.keys()))
        return {"index_type": str(type(index)),
                "indexer_type": str(type(self.indexer)),
                "post_mem": str(index[kw]),
                "post_type": str(type(index[kw])),
                "node_mem": str(index[kw].start_node),
                "node_type": str(type(index[kw].start_node)),
                "node_value": str(index[kw].start_node.value),
                "command_result": eval(command) if "." in command else ""}

    def run_queries(self, query_list, random_command):
        """ DO NOT CHANGE THE output_dict definition"""
        output_dict = {'postingsList': {},
                       'postingsListSkip': {},
                       'daatAnd': {},
                       'daatAndSkip': {},
                       'daatAndTfIdf': {},
                       'daatAndSkipTfIdf': {},
                       'sanity': self.sanity_checker(random_command)}

        for query in tqdm(query_list):
            """ Run each query against the index. You should do the following for each query:
                1. Pre-process & tokenize the query.
                2. For each query token, get the postings list & postings list with skip pointers.
                3. Get the DAAT AND query results & number of comparisons with & without skip pointers.
                4. Get the DAAT AND query results & number of comparisons with & without skip pointers, 
                    along with sorting by tf-idf scores."""
            input_term_arr = []  # Tokenized query. To be implemented.
            input_term_arr = self.preprocessor.tokenizer(query, duplicate=False)

            for term in input_term_arr:
                postings, skip_postings = [], []
                if self.indexer.get_index().get(term):
                    postings = self.indexer.get_index()[term].traverse_list()
                    skip_postings = self.indexer.get_index()[term].traverse_skips()
                """ Implement logic to populate initialize the above variables.
                    The below code formats your result to the required format.
                    To be implemented."""
                output_dict['postingsList'][term] = postings
                output_dict['postingsListSkip'][term] = skip_postings

            # and_op_no_skip, and_comparisons_no_skip =  self._daat_and(input_term_arr, 'no_skip')
            and_op_no_skip, and_comparisons_no_skip, \
            and_op_no_skip_sorted, and_comparisons_no_skip_sorted = self._daat_and(input_term_arr, 'no_skip')
            # and_op_skip, and_comparisons_skip = self._daat_and(input_term_arr)
            and_op_skip, and_comparisons_skip, \
            and_op_skip_sorted, and_comparisons_skip_sorted = self._daat_and(input_term_arr, 'skip')
            # and_op_no_skip, and_op_skip, and_op_no_skip_sorted, and_op_skip_sorted = None, None, None, None
            # and_comparisons_no_skip, and_comparisons_skip, \
            #     and_comparisons_no_skip_sorted, and_comparisons_skip_sorted = None, None, None, None
            """ Implement logic to populate initialize the above variables.
                The below code formats your result to the required format.
                To be implemented."""
            and_op_no_score_no_skip, and_results_cnt_no_skip = self._output_formatter(and_op_no_skip)
            and_op_no_score_skip, and_results_cnt_skip = self._output_formatter(and_op_skip)
            and_op_no_score_no_skip_sorted, and_results_cnt_no_skip_sorted = self._output_formatter(and_op_no_skip_sorted)
            and_op_no_score_skip_sorted, and_results_cnt_skip_sorted = self._output_formatter(and_op_skip_sorted)

            output_dict['daatAnd'][query.strip()] = {}
            output_dict['daatAnd'][query.strip()]['results'] = and_op_no_score_no_skip
            output_dict['daatAnd'][query.strip()]['num_docs'] = and_results_cnt_no_skip
            output_dict['daatAnd'][query.strip()]['num_comparisons'] = and_comparisons_no_skip

            output_dict['daatAndSkip'][query.strip()] = {}
            output_dict['daatAndSkip'][query.strip()]['results'] = and_op_no_score_skip
            output_dict['daatAndSkip'][query.strip()]['num_docs'] = and_results_cnt_skip
            output_dict['daatAndSkip'][query.strip()]['num_comparisons'] = and_comparisons_skip

            output_dict['daatAndTfIdf'][query.strip()] = {}
            output_dict['daatAndTfIdf'][query.strip()]['results'] = and_op_no_score_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_docs'] = and_results_cnt_no_skip_sorted
            output_dict['daatAndTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_no_skip_sorted

            output_dict['daatAndSkipTfIdf'][query.strip()] = {}
            output_dict['daatAndSkipTfIdf'][query.strip()]['results'] = and_op_no_score_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_docs'] = and_results_cnt_skip_sorted
            output_dict['daatAndSkipTfIdf'][query.strip()]['num_comparisons'] = and_comparisons_skip_sorted

        with open('data/temp_output.json', 'w') as fp:
            json.dump(output_dict, fp)
        return output_dict


@app.route("/execute_query", methods=['POST'])
def execute_query():
    """ This function handles the POST request to your endpoint.
        Do NOT change it."""
    start_time = time.time()

    queries = request.json["queries"]
    random_command = request.json["random_command"]

    """ Running the queries against the pre-loaded index. """
    output_dict = runner.run_queries(queries, random_command)

    """ Dumping the results to a JSON file. """
    with open(output_location, 'w') as fp:
        json.dump(output_dict, fp)

    response = {
        "Response": output_dict,
        "time_taken": str(time.time() - start_time),
        "username_hash": username_hash
    }
    return flask.jsonify(response)


if __name__ == "__main__":
    """ Driver code for the project, which defines the global variables.
        Do NOT change it."""

    output_location = "project2_output.json"
    user_name = 'sarveshw' #remove
    cor_path = r'data/input_corpus.txt' #remove
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    '''parser.add_argument("--corpus", type=str, help="Corpus File name, with path.")'''
    parser.add_argument("--corpus", type=str, help="Corpus File name, with path.", default=cor_path) #remove
    parser.add_argument("--output_location", type=str, help="Output file name.", default=output_location)
    '''parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here")'''
    parser.add_argument("--username", type=str,
                        help="Your UB username. It's the part of your UB email id before the @buffalo.edu. "
                             "DO NOT pass incorrect value here", default=user_name) #remove
    argv = parser.parse_args()

    corpus = argv.corpus
    output_location = argv.output_location
    username_hash = hashlib.md5(argv.username.encode()).hexdigest()

    """ Initialize the project runner"""
    runner = ProjectRunner()

    """ Index the documents from beforehand. When the API endpoint is hit, queries are run against 
        this pre-loaded in memory index. """
    runner.run_indexer(corpus)

    app.run(host="0.0.0.0", port=9999)
