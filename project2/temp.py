
import re
import time

def rough():
    ll = LinkedList()
    [ll.insert_at_end(i) for i in [2,3,1,5,4]]
    # print(ll.traverse_list())
    ll.add_skip_connections()
    # print(ll.traverse_skips())
    a = ll.find_an_element(5)
    print(a.value)
    exit(10)

class Human:
    def __init__(self, n=None, o=None):
        self.name= n
        self.occupation = o

    def do_work(self):
        if self.occupation == "tennis player":
            print("playing tennis..")
        elif self.occupation == "actor":
            print(self.name,"shooting movie")

    def speaks(self):
        print(self.name,"says, how are you !!")


def main():
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


if __name__ == '__main__':
    main()