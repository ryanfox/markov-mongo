import random
from pymongo import MongoClient

class MarkovMongo(object):
    ''' Markov Chain implementation in python with storage in MongoDB.'''
    
    def __init__(self, uri=None, dbname='testdb', coll='testcoll', order=2):
        connection = MongoClient(uri)
        db = connection[dbname]
        self.collection = db[coll]
        self.size = self.collection.count()
        self.order = order
        self.punctuation = ('.', '!', '?')
    
    
    def insertwords(self, filename, update=True):
        ''' Read a file, parse into tuples, and insert into db.
        Be default, updates records instead of duplicating. '''
        with open(filename) as f:
            chains = {}
            for tup in self.split(f.read().split()):
                key = tuple(tup[:-1])
                if key in chains:
                    chains[key].append(tup[-1])
                else:
                    chains[key] = [tup[-1]]

            # Don't overwrite documents if we're updating            
            if update:
                for i, key in enumerate(chains):
                        self.collection.update({'key': key}, {'$set': {'key': key, 'words': chains[key], 'i': i}}, upsert=True)
            else: # Upload all new docs
                self.collection.insert(({'i': i, 'key': key, 'words': chains[key]} for i, key in enumerate(chains)))
            self.size = self.collection.count()
            
    
    def getwords(self, key):
        ''' Get the list of words from the database corresponding to
        the supplied key.  Key should be a tuple containing two strings. '''
        result = self.collection.find_one({'key': key})
        while result == None:
            result = self.collection.find_one({'i': random.randint(0, self.size)})
        return result['words']
    
    
    def split(self, words):
        ''' Parse the supplied string into n-word chunks.  For example,
    parsing 'One small step for man' into order-3 chunks would yield:
    ('One', 'small', 'step'),
    ('small', 'step', 'for'),
    ('step', 'for', 'man')'''
        if len(words) < self.order + 1:
            return
            
        for i in xrange(len(words) - self.order):
            yield words[i : i + self.order + 1]


    def generate(self, seed=None, length=random.randint(25, 50)):
        ''' Generate text from the corpus in the database.  A seed may
    optionally be supplied.  If so, the seed should be a tuple or list
    containing n strings, where n is the order of the chain. '''
        if seed == None:
            seed = random.randint(0, self.size - (self.order + 1))
            row = self.collection.find_one({'i': seed})
        else:
            row = self.collection.find_one({'key': seed})
        key = row['key']
        words = key[:]
        for i in xrange(length - self.order):
            newword = random.choice(self.getwords(key))
            words.append(newword)
            key.reverse()
            key.pop()
            key.reverse()
            key.append(newword)
        
        if words[-1][-1] == ',':
            words[-1][-1] = '.'
        if not words[-1][-1] in self.punctuation:
            words[-1] += '.'

        return ' '.join(words)
        
        







