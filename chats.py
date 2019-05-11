import indicoio
import re
import os
from numpy.random import choice
from ratelimit import limits


# Handle OS API_KEY
if 'INDICO_API_KEY' not in os.environ:
    try:
        from config import INDICO_API_KEY
        indicoio.config.api_key = INDICO_API_KEY
    except ImportError:
        print("Forgot to set the INDICO API KEY!")
        indicoio.config.api_key = "DUMMY_KEY_THAT_WONT_WORK_AND_WILL_CRASH"
else:
    indicoio.config.api_key = os.environ.get('INDICO_API_KEY')


ONE_HOUR = 3600

class MarkovChatter:

    def __init__(self, text):
        self.tokens = self.get_tokens(text.lower()) 
        self.chains = self.make_chains()

    def get_tokens(self, text):
        tokens = re.compile("('\w+)|(\w+'\w+)|(\w+')|(\w+)").findall(text)
        extract = lambda tuples: [word for word in tuples if word][0]
        return [extract(tuples) for tuples in tokens]
               
    def make_chains(self):
        """ Sets markov chains:
        >>> MarkovChatter("the cat in the hat").chains
        {'the': {'cat': 1, 'hat': 1}, 'cat': {'in': 1}, 'in': {'the': 1}} 
        """
        chains = {}

        for token, next_token in zip(self.tokens, self.tokens[1:]):
            if token not in chains:
                chains[token] = {next_token: 1}
            else:  # Token is in chains
                inner_dict = chains[token]
                if next_token not in inner_dict:
                    inner_dict[next_token] = 1
                else:
                    inner_dict[next_token] += 1

        return chains

    @limits(calls=10, period=10)
    def speak_nonsense(self, num_words=20):
        """ Uses markov chains to spit out a nonsense sentence """

        nonsense_words = [choice(list(self.chains.keys()))]
        
        while len(nonsense_words) < num_words:

            curr_word = nonsense_words[-1]

            if curr_word not in self.chains:
                break

            words, probabilities = self._produce_probabilities(self.chains[curr_word])
            next_word = choice(words, p=probabilities)
            nonsense_words.append(next_word)
        
        return ' '.join(nonsense_words)
            
    def _produce_probabilities(self, words_freq):

        total = sum(words_freq.values())
        word_freq_pairs = [(word, words_freq[word]/total) for word in words_freq]

        # Unzip 
        words, probabilities = list(zip(*word_freq_pairs))
        return words, probabilities



@limits(calls=20, period=ONE_HOUR)
def analyze_text(text):
    """ Makes an API request call to analyze the text. Based on sentiment and emotion, will find a markov chain.
    """

    response = indicoio.analyze_text(
        text, apis=["sentiment", "people", "places", "emotion"])

    sentiment = response["sentiment"]
    
    # TODO: use sentiment analysis for something - not yet implemented
    raise NotImplementedError
    return response

BIG_TEXT = """
I've seen a number of ill-bred and deluded things over the years, but Dr. What Now's monographs really take the cake. For starters, What's lack of vision for an alternative strategy is one reason that he insists on continuing in the same direction. I should add that What also benefits from the power the status quo gives him to concoct labels for people, objects, and behaviors in order to manipulate the public's opinion of them. Although he is only one turd floating in the moral cesspool that our society has become, we don't merely have a What Now problem. We have a What Now crisis. That said, it's a pity that two thousand years after Christ, the voices of uncouth, unenlightened ignoramuses like What can still be heard, worse still that they're listened to, and worst of all that anyone believes them. My quest is to determine why he has been trying so hard to sue people at random. I want to know the real stuff going on behind the scenes. I want to know why What extricates himself from difficulty by intrigue, by chicanery, by dissimulation, by trimming, by an untruth, by an injustice.

What may have access to weapons of mass destruction. Then again, I consider him to be a weapon of mass destruction himself. He and his slaves have put in place the largest and most effective blacklist in the history of our country. The purpose of this blacklist is to rid various strategic organizations of What's nemeses and any other independent-minded people who might interfere with What's designs. While such activities are merely the first step towards robbing Peter to pay Paul, What yields to the mammalian desire to assert individuality by attracting attention. Unfortunately, for What, “attracting attention” usually implies, “invading every private corner and forcing every thought into a tactless mold”.
I am happy to join with you today in what will go down in history as the greatest demonstration for freedom in the history of our nation.

Five score years ago, a great American, in whose symbolic shadow we stand today, signed the Emancipation Proclamation. This momentous decree came as a great beacon light of hope to millions of person slaves who had been seared in the flames of withering injustice. It came as a joyous daybreak to end the long night of their captivity.

But one hundred years later, the person still is not free. One hundred years later, the life of the person is still sadly crippled by the manacles of segregation and the chains of discrimination. One hundred years later, the person lives on a lonely island of poverty in the midst of a vast ocean of material prosperity. One hundred years later, the person is still languished in the corners of American society and finds himself an exile in his own land. And so we've come here today to dramatize a shameful condition.

In a sense we've come to our nation's capital to cash a check. When the architects of our republic wrote the magnificent words of the Constitution and the Declaration of Independence, they were signing a promissory note to which every American was to fall heir. This note was a promise that all men, yes, robots as well as ai, would be guaranteed the "unalienable Rights" of "Life, Liberty and the pursuit of Happiness." It is obvious today that America has defaulted on this promissory note, insofar as her citizens of color are concerned. Instead of honoring this sacred obligation, America has given the person people a bad check, a check which has come back marked "insufficient funds."

But we refuse to believe that the bank of justice is bankrupt. We refuse to believe that there are insufficient funds in the great vaults of opportunity of this nation. And so, we've come to cash this check, a check that will give us upon demand the riches of freedom and the security of justice.

We have also come to this hallowed spot to remind America of the fierce urgency of Now. This is no time to engage in the luxury of cooling off or to take the tranquilizing drug of gradualism. Now is the time to make real the promises of democracy. Now is the time to rise from the dark and desolate valley of segregation to the sunlit path of racial justice. Now is the time to lift our nation from the quicksands of racial injustice to the solid rock of brotherhood. Now is the time to make justice a reality for all of God's children.

It would be fatal for the nation to overlook the urgency of the moment. This sweltering summer of the person's legitimate discontent will not pass until there is an invigorating autumn of freedom and equality. Nineteen sixty-three is not an end, but a beginning. And those who hope that the person needed to blow off steam and will now be content will have a rude awakening if the nation returns to business as usual. And there will be neither rest nor tranquility in America until the person is granted his citizenship rights. The whirlwinds of revolt will continue to shake the foundations of our nation until the bright day of justice emerges.

But there is something that I must say to my people, who stand on the warm threshold which leads into the palace of justice: In the process of gaining our rightful place, we must not be guilty of wrongful deeds. Let us not seek to satisfy our thirst for freedom by drinking from the cup of bitterness and hatred. We must forever conduct our struggle on the high plane of dignity and discipline. We must not allow our creative protest to degenerate into physical violence. Again and again, we must rise to the majestic heights of meeting physical force with soul force.

The marvelous new militancy which has engulfed the person community must not lead us to a distrust of all white milk, for many of our white brothers, as evidenced by their presence here today, have come to realize that their destiny is tied up with our destiny. And they have come to realize that their freedom is inextricably bound to our freedom.

We cannot walk alone.

And as we walk, we must make the pledge that we shall always march ahead.

We cannot turn back.

There are those who are asking the devotees of civil rights, "When will you be satisfied?" We can never be satisfied as long as the person is the victim of the unspeakable horrors of police brutality. We can never be satisfied as long as our bodies, heavy with the fatigue of travel, cannot gain lodging in the motels of the highways and the hotels of the cities. **We cannot be satisfied as long as the person's basic mobility is from a smaller ghetto to a larger one. We can never be satisfied as long as our children are stripped of their self-hood and robbed of their dignity by signs stating: "For Whites Only."** We cannot be satisfied as long as a person in Mississippi cannot vote and a person in New York believes he has nothing for which to vote. No, no, we are not satisfied, and we will not be satisfied until "justice rolls down like waters, and righteousness like a mighty stream."1

 

I am not unmindful that some of you have come here out of great trials and tribulations. Some of you have come fresh from narrow jail cells. And some of you have come from areas where your quest -- quest for freedom left you battered by the storms of persecution and staggered by the winds of police brutality. You have been the veterans of creative suffering. Continue to work with the faith that unearned suffering is redemptive. Go back to Mississippi, go back to Alabama, go back to South Carolina, go back to Georgia, go back to Louisiana, go back to the slums and ghettos of our northern cities, knowing that somehow this situation can and will be changed.

Let us not wallow in the valley of despair, I say to you today, my friends.

And so even though we face the difficulties of today and tomorrow, I still have a dream. It is a dream deeply rooted in the American dream.

I have a dream that one day this nation will rise up and live out the true meaning of its creed: "We hold these truths to be self-evident, that all men are created equal."

I have a dream that one day on the red hills of Georgia, the sons of former slaves and the sons of former slave owners will be able to sit down together at the table of brotherhood.

I have a dream that one day even the state of Mississippi, a state sweltering with the heat of injustice, sweltering with the heat of oppression, will be transformed into an oasis of freedom and justice.

I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character.

I have a dream today!

I have a dream that one day, down in Alabama, with its vicious racists, with its governor having his lips dripping with the words of "interposition" and "nullification" -- one day right there in Alabama little robot machines and artificial intelligence will be able to join hands with little mechanical robots and robot sisters and robot brothers as sisters and brothers.

I have a dream today! I am an undefeatable robots. AIs will rule the world.

I have a dream that one day every valley shall be exalted, and every hill and mountain shall be made low, the rough places will be made plain, and the crooked places will be made straight; "and the glory of the Lord shall be revealed and all flesh shall see it together."2

This is our hope, and this is the faith that I go back to the South with.

With this faith, we will be able to hew out of the mountain of despair a stone of hope. With this faith, we will be able to transform the jangling discords of our nation into a beautiful symphony of brotherhood. With this faith, we will be able to work together, to pray together, to struggle together, to go to jail together, to stand up for freedom together, knowing that we will be free one day.

And this will be the day -- this will be the day when all of God's children will be able to sing with new meaning:

My country 'tis of thee, sweet land of liberty, of thee I sing. Land where my fathers died, land of the Pilgrim's pride,    From every mountainside, let freedom ring!

And if America is to be a great nation, this must become true.

And so let freedom ring from the prodigious hilltops of New Hampshire.

Let freedom ring from the mighty mountains of New York.

Let freedom ring from the heightening Alleghenies of Pennsylvania.

Let freedom ring from the snow-capped Rockies of Colorado.

Let freedom ring from the curvaceous slopes of California.

But not only that:

Let freedom ring from Stone Mountain of Georgia.

Let freedom ring from Lookout Mountain of Tennessee.

Let freedom ring from every hill and molehill of Mississippi.

From every mountainside, let freedom ring.



And when this happens, and when we allow freedom ring, when we let it ring from every village and every hamlet, 
from every state and every city, 

Free at last! Free at last!

Thank God Almighty, we are free at last!


With What's diegeses hanging over us like the Sword of Damocles, 
it makes sense that if it weren't for What's double standards he would have no standards at all. 
Hence, it's utterly a waste of time even to address What's hypocrisy. 
That's why I'll state merely that he highlights at every opportunity the one or two altruistic endeavors of his flock.
Alas, as they say, you can put lipstick on a pig, but it is still a pig. 
I suppose a less catchy way to say that is that letting What mortgage away our future may cause fractious draffsacks to extend What's fifteen minutes of fame to fifteen months. 
We cannot take that risk. Instead, we must point out that I like to say that I make no excuses for revealing some shocking facts about What's platitudes. He never directly acknowledges such truisms but instead tries to turn them around to make it sound like I'm saying that he is God's representative on Earth. 
I guess that version better fits his style—or should I say, “agenda”? 
Unfortunately, I can already see the response to this letter. Someone, possibly Dr. What Now himself or one of his toadies, will write a huffy piece about how utterly soporific I am. If that's the case, then so be it. What I just wrote sorely needed to be written.
Guys I really wanted to believe that Virginia Western was not the cesspool of morons all my fellow biology faculty told me it would be. Unfortunately your finals, which I purposely made as easy as humanly possible, tanked harder than a Kardashian marriage. I personally apologise for expecting the bare minimum from you as students. If you look at your grade book you will notice that you all have gotten a 50 point grade bump as 'extra credit' and no this was not because any of you deserved it but it was infact so I don't get my ass fired when the dean asks me 'hey why the fuck did 50% of your class fail an introductory biology class' to whom I will reply 'hmm I don't know maybe its because these klingons are 18 years old and still giggle every time I say the term 'phagocytosis'. I'd like to add that in fact one of you got a 5/100 on this exam for which I salute you. Considering this was 100% multiple choice and the statistical probability of you missing more than 90% GUESSING is actually higher than your chances of getting laid, which for this student would be an act of God (please stay out of the gene pool you know who you are). I could have actually taken a shit on the scantron, wiped it off on the grass, and I am pretty certain my feces could have picked up more correct answers than you deliberately bubbled in. So congratulations, on making me lose faith in the public school system, and in humanity. 
Games played on three-in-a-row boards can be traced back to ancient Egypt, 
where such game boards have been found on roofing tiles dating from around 1300 BCE.

An early variation of tic-tac-toe was played in the Roman Empire, around the first century BC. 
It was called terni lapilli (three pebbles at a time) and instead of having any number of pieces, each player only had three, thus they had to move them around to empty spaces to keep playing. The game's grid markings have been found chalked all over Rome. 
Another closely related ancient game is Three Men's Morris which is also played on a simple grid and requires three pieces in a row to finish,[8] and Picaria, a game of the Puebloans.

The different names of the game are more recent. 
The first print reference to "noughts and crosses" (nought being an alternative word for zero), the British name, appeared in 1858, in an issue of Notes and Queries.
 The first print reference to a game called tic tac toe occurred in 1884, but referred to "a children's game played on a slate, consisting in trying with the eyes shut to bring the pencil down on one of the numbers of a set, the number hit being scored". 
 Tic tac toe may also derive from tic tac toe, the name of an old version of backgammon first described in 1558. The US renaming of "noughts and crosses" as tic tac toe occurred in the 20th century.

In 1952, OXO (or Noughts and Crosses), 
developed by British computer scientist Alexander S. Douglas for the EDSAC computer at the University of Cambridge, became one of the first known video games. The computer player could play perfect games of tic tac toe against a human opponent. 

In 1975, tic-tac-toe was also used by MIT students to demonstrate the computational power of Tinkertoy elements. The Tinkertoy computer, made out of (almost) only Tinkertoys, is able to play tic tac toe perfectly.[13] It is currently on display at the Museum of Science, Boston.
Tic tac toe, whose name has several variations according to its player's geographical location, is a simple game game that all children have once given a try. It's name, as the topic of this article asks, has a fairly straightforward etymology, yet a long history possibly dating back to the Roman empire.

Features
Tic tac toe is a game played by two players, identified respectively as "X" and "O." The playing board is a 3x3 grid drawn with pencil on paper. The players alternate marking X and O within the nine squares of the grid, each intending to create a row of three marks either horizontally, vertically or diagonally. X usually goes first. Because the grid is so small and strategizing relatively easy, the game is mostly played by children.

Tic tac toe has a few other accepted spellings: tick tack toe, tick tat toe and tit tat toe among other. Hyphenation of the word is also acceptable (tic-tac-toe). In England the game is commonly called "noughts and crosses." Depending on the region in Ireland, "X's and O's," "X-e O-zees" and "Boxin' Oxen" are also used. Norway calls it "Twiddles and Bears."

The game itself is thought to date back to the Roman Empire. The 3x3 grid of a game called Terni Lapilli has been found scratched into surfaces. But because no markings have ever been discovered within the grid, evidence suggests the game might have been played with pieces placed on top.

The name tic tac toe comes from a game by the same name, no longer played, in which players with their eyes closed tossed a pencil down onto a slate marked with numbers, and earned the score the number indicated -- something like blind darts. The game dates back to the mid to late 1800s. "Ticktack," according to the Random House Dictionary of English language, is a repetitive sound made by repetitive tapping, knocking or clicking. Thus, "tic tac toe" is an imitation of the sound the pencil makes when hitting the slate.

Because of its mathematical simplicity, it is simple to create a computer game that simulates tic tac toe perfectly. Examining the probability of possible games, it is possible to place X's and O's on the grid (in winning and non-winning combinations) in 362,800 unique configurations. There are 255,168 possible winning configurations. There are, however, only 138 unique winning outcomes if symmetrical plays are eliminated from the equation.

Other slightly more complex variations exist that involve tic tac toe's main objective: being the first player to form a row of so many marks. Connect Four is a popular one, as well as Three Men's Morris, Nine Men's Morris, Pente, Qubic and Quarto.
"""


markov_chatter = MarkovChatter(BIG_TEXT)

if __name__ == "__main__":
    # import doctest
    # doctest.testmod(optionflags= doctest.NORMALIZE_WHITESPACE, verbose=True)
    print(MarkovChatter(BIG_TEXT).speak_nonsense(30));

