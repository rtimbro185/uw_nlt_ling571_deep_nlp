#######################################################################
#Ling 571 - Deep Processing Techniques for NLP
#Winter 2016
#Homework #9: Due February 16nd, 2016
#http://courses.washington.edu/ling571/ling571_WIN2016/hw/hw9/hw9.html
#Author: Ryan Timbrook
#Date: 03/15/2016
########################################################################
Goals:

    Explore issues in pronominal anaphora resolution.
    Gain familiarity with syntax-based resolution techniques.
    Analyze the effectiveness of the Hobbs Algorithm by applying it to pairs of parsed sentences.
    Optionally: Implement the Hobbs algorithm for anaphora resolution on a set of sentences.


At a basic level it seems that the Hobbs algorithm can accurately select the antecedent of the anaphoric term.
In practice, while working on the automation of the Hobbs algorithm, it became clear just how many variables come into
play with syntactic and semantic applications. Even with the limited feature set required by the Hobbs Algorithm
it was still challenging to implement. A good many of the challenges would arise because I wanted to include additional
constraints that were outside of the requirements. It shows that a chaining and mixed implementation of these algorithms
would be beneficial.
The output of my automated script had a few issues. In the second pairing of sentences it printed out a grammatical rejection
multiple times where by the rules in the system it should have printed once. I also believe that the rejection was
incorrect or at least ambiguous based on Grammatical role constraints. It was rejected based on Subject/Object location
in the sentence relating to the anaphoric term 'They'. In the fifth pairing the automated script incorrectly selected "Scientists"
as the antecedent, however I believe based on the agreement rules and constraints given the automated system accurately
selected the term. Its limiting with the rules and process to have expected the Hobbs Algorithm, or at least my implementation of it,
to have selected "mice" as the antecedent. On the surface the Algorithm looks simple, however as I dug through it
it had many little nuances of flow control that had to be delt with. Some of which I don't believe I fully grasped. As in
the issue I mentioned above where the rejected grammatical role proposal caused multiple prints of the same proposal.
I believe this was due to how I implemented the breadth first search logic and especially step 6 of the Algorithm. "If X
is an NP node and if the path p to X did not pass through the Nominal node that X immediately dominates, propose X as
the antecedent." I used a process of comparing the current NP nodes tree index position against that of the nearest Nom
node's tree index position which was in my path variable. I believe this still brought about an issue dependent on the
sentence structure analyzed.
To handle grammar features I opted not to alter the grammar.cfg file provided with features and converting it into a fcfg
file for concerns of how the printed output would contrast with expectations and the examples provided. With limited time and
resources I chose to use an external "properties" type file to pull in the data. The file name is "agreement.txt".
It has the listing of the grammatical feature constraints used by the application.





