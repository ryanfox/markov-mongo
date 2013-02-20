import random
from pymongo import MongoClient

class MarkovMongo(object):
    ''' Markov Chain implementation in python with storage in MongoDB.
    Currently only supports 2nd-order Markov Chains. '''
    
    def __init__(self, uri=None, dbname='testdb', coll='testcoll'):
        connection = MongoClient(uri)
        db = connection[dbname]
        self.collection = db[coll]
        self.size = self.collection.count()
    
    
    def insertwords(self, filename):
        ''' Read a file, parse into triples, and insert into db.
        Updates record if key already exists in db. '''
        with open(filename) as f:
            chains = {}
            for w1, w2, w3 in self.triples(f.read().split()):
                key = (w1, w2)
                if key in chains:
                    chains[key].append(w3)
                else:
                    chains[key] = [w3]
            
            for i, key in enumerate(chains):
                self.collection.update({'key': key}, {'$set': {'key': key, 'words': chains[key], 'i': i}}, upsert=True)
            self.size = self.collection.count()
            
    
    def getwords(self, key):
        ''' Get the list of words from the database corresponding to
        the supplied key.  Key should be a tuple containing two strings. '''
        return self.collection.find_one({'key': key})['words']
    
    
    def triples(self, words):
        ''' Parse the supplied string into 3-word chunks.  For example, the string
    'One small step for man' would yield:
    ('One', 'small', 'step'),
    ('small', 'step', 'for'),
    ('step', 'for', 'man')'''
        if len(words) < 3:
            return
            
        for i in xrange(len(words) - 2):
            yield (words[i], words[i + 1], words[i + 2])


    def generate(self, seed=None, length=random.randint(25, 50)):
        ''' Generate text from the corpus in the database.  A seed may optionally
    be supplied.  If so, the seed should be a tuple containing 2 strings. '''
        if seed == None:
            seed = random.randint(0, self.size - 3)
            row = self.collection.find_one({'i': seed})
        else:
            row = self.collection.find_one({'key': seed})
        w1, w2 = row['key']
        words = []
        for i in xrange(length):
            words.append(w1)
            temp = w2
            w2 = random.choice(self.getwords((w1, w2)))
            w1 = temp

        if not w2.endswith('.'):
            w2 += '.'
        words.append(w2)        
        return ' '.join(words)
        
        







