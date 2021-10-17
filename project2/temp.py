
import re
import time
from collections import OrderedDict
from nltk.corpus import stopwords
import  pickle

def rough():
    ll = LinkedList()
    [ll.insert_at_end(i) for i in [2,3,1,5,4]]
    # print(ll.traverse_list())
    ll.add_skip_connections()
    # print(ll.traverse_skips())
    a = ll.find_an_element(5)
    print(a.value)
    exit(10)
    #checking indexer functioning with temp values
    self.indexer.generate_inverted_index(100,[3,1,2])
    self.indexer.generate_inverted_index(101,[5,4,3,1,2])
    print(self.indexer.get_index())
    for key in self.indexer.get_index().keys():
        print(self.indexer.get_index()[key].traverse_list())
    exit(10)


def output_txt():
    with open('data/temp_output.txt','w') as fp:
        for i in self.indexer.get_index().keys():
            text = i + str(self.indexer.get_index()[i].traverse_list())
            fp.write(text)
    exit(10)

class Human:
    def __init__(self, n=None, o=None):
        self.name= n
        self.occupation = o

    def sort_func(self, li):
        return li[1]

    def sort(self):
        ll_len = [['a',10],['b',5],['c',1]]
        ll_len.sort(key=self.sort_func)
        print(ll_len)

    def do_work(self):
        if self.occupation == "tennis player":
            print("playing tennis..")
        elif self.occupation == "actor":
            print(self.name,"shooting movie")

    def speaks(self):
        print(self.name,"says, how are you !!")

def regex():
    c = '种this is temp-2!@#$%^&*() THIS IS UPPER CASE PART-2 another this is upper part-3'
    c = '    def    '
    s1 = set(['this','this','this','this','this'])
    print(s1)
    print(c-s1)
    x = re.findall('[A-Z|a-z|0-9]*',c)
    z = []
    for term in x:
        if len(term) >0:
            z.append(term)
    y = " ".join(x)
    # if match:  print(match.group())
    # else:  print("Not found")
    print(x,"\n",y)
    print(" ".join(y.split()).lower())
    print(str(z).lower())
    time.sleep(10)
    # print(" ".join(y.split()).lower() == str(z).lower())
    # print('种'.isascii())
    # print(int(c,10))

    # tom = Human("Tom Cruise", "actor")
    # tom.do_work()
    # tom.speaks()

def key(term):
    return term[1]

def main():
    dict_sub = {}
    dict_sub["ip"] = "13.58.91.67"
    dict_sub["port"] = "9999"
    dict_sub["name"] = "execute_query"

    with open('project2_index_details.pickle', 'wb') as f:
        pickle.dump(dict_sub, f, protocol=pickle.HIGHEST_PROTOCOL)

    with open('project2_index_details.pickle', 'rb') as f:
        b = pickle.load(f)
    print(dict_sub == b)

    # print(ll_len.sort())
    # s1 = set(stopwords.words('english'))
    # print('what' in s1)
    # od1 = OrderedDict()
    # od1['a'] = "alpha"
    # print(od1.__str__())


def temp_sort():
    ll_len = [['a',10],['b',5],['c',1]]
    ll_len.sort(key=key)
    print(ll_len)

def garbage():
    h1 = Human()
    h1.sort()
    duplicate = False
    if not duplicate:
        print("inside if")


if __name__ == '__main__':
    main()