Markov-Mongo v0.0.1

Markov-Mongo is a Python implementation of 2nd-order Markov Chains.  It uses
MongoDB for storage of corpus data.  Its' primary use is generation of
semi-coherent text, often yielding comical results.

Installation:
MongoDB and its' python driver, pymongo are the only prerequisites.
The folks at mongodb.org have some great instructions for setting up Mongo.
To get pymongo, run `pip install pymongo` in your terminal.

Usage:
from MarkovMongo import MarkovMongo
mm = MarkovMongo(dbname='kafka', coll='metamorphosis')
    
# Takes a while, depending on size of source
mm.insertwords('metamorphosis.txt')

# If you're inserting into a new collection, supply the argument update=False
# for a faster insert
mm.insertwords('metamorphosis.txt', update=false)
    
mm.generate()
    'He realised what had happened but she left within a quarter of an hour, tearfully thanking Gregor's mother would tug at her skirt to show the whole, innocent family that this job would provide for Gregor for his decision. Mr. Samsa might go to Hell! He felt a itch.'    
    
# Specify a seed
mm.generate(seed=('Gregor', 'Samsa'))
    'Gregor Samsa woke from it in the pockets of their room and found herself face to her father, who had been prepared for him to starve either, but perhaps it would have been no surprise to him, "what is wrong? You barricade yourself in your room, give no.'

Code is free to use under the terms of the MIT License (see LICENSE.txt).
