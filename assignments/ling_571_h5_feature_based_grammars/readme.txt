#######################################################################
#Ling 571 - Deep Processing Techniques for NLP
#Winter 2016
#Homework #5: Due February 2nd, 2016
#http://courses.washington.edu/ling571/ling571_WIN2016/hw/hw5/hw5.html
#Author: Ryan Timbrook
#Date: 02/9/2016
########################################################################
Goals:
    -Explore the role of features in implementing linguistic constraints.
    -Identify some of the challenges in building compact constraints to define a precise grammar.
    -Gain some further familiarity with NLTK.
    -Apply feature-based grammars to perform grammar checking

With my newness in the study of computational linguistics, features are the first concept that have started to
resonate within me. I'm beginning to feel I can visualize, just scratching the surface in understand the many
complications and layers that go into parsing textual information in an effort to gain some kind of meaning.

The challenges I experienced in this assignment were with the long-distance dependency's and gender relationships.
Each time I reworked my grammar rules to try implementing a new feature concept I had read about in the documentation,
or NLTK book it would have negative effects on the structures I had in place that were covering the more simplistic
sentence formats. As I worked through the sentences it was apparent that the challenges in generalization were
getting harder and more precise constants were required. An example of a constraint I applied was adding a
boolean indicator, which represents an aspect constraint, between achievement verbs and prepositions.
Another example of using this boolean argument type to remedy an issue with long-distance, question type,
sentence was applying another boolean flag I labeled as LGD (Long Distance) to the 'knows' verb.
This allowed the grammar structure to recognize the "what does Mary think John knows" sentence.
All of my other attempts at implementing the structures outlined in chapter 9 of the NLTK book failed when
adding them to the greater sentence pool.

I've learned there is a fine line in how general your grammar rules can be with agreements if your
efforts are to minimize ambiguity and multiple parses. After re-working my grammar file, a number of times,
in efforts to get one parse per sentence, I was left with one sentence that I was unable to
achieve that result with. The sentence "what did Mary put on the shelf" yields two parses at my final attempt.
In other scenarios of the grammar file it was at one parse, but through augmentation of the file to
accept other sentence structure types it ended up at two.

