

### Dialogue/quips/utterances:

Some attributes to a quip:

 - Unique to single speaker 
 - speakable by any character

 - Non-repeatable

 - directly follow
 - indirectly follow

 - convey factual information (require that speaker believes or lie)
 - 

#### Practice - Conversation

 - selected speech act**
 - selected speaker
 - selected topic (topics)

 - Significant pauses (several ticks) wipes out topics

 - If no selected speaker - anyone can take the word
 - Can take on new topic but reference to previous topics

#### Speech act

Look into what is a speech act (state changing - as in acting):

 - (Lying)
 - Informing/ Stating (factual)
 - Committing
 - Asking
 - Replying
 - Challenge (information, mood, evalation, committing)
 - Introductory (new topic)
 - Express mood
 - Express evaluation

### Tagging system

Via a tree structure state we can express various states to a ordered hiearchy of objects. A branch on a leaf can serve as a tag of some property to the higher level branches. 

A characters trait should be conditional. That is there should be some preconditions in please with the given trait in order to trigger some specific emotion associated to the trait (governing the choice of the actions in the context of the trait)

Example: Extrovert
```
processes.brown.meet.lucy * actor.brown.traits.extrovert -> actor.brown.emotion.energized
```
Thus a generic version for would be :

actors.[Actor].traits.extrovert is a representation of
```

process.[Actor].meet.[Other] -> actors.[Actor].emotion.energized

```
somewhere else we would associated something positive to _energized_

#### Tagging and fragments

SpiritAI system makes use of fragments which is a kind of conditional tracery version. Basically a fragment is a number of sentences (which can include other fragments) which are chosen randomly at execution time. A fragment can be conditioned so a specific state should be available in order for the fragment to be executed.

An exclusion logic branch could represent the tagging of a fragment and likewise also serve as conditions. Example

```
speech_act.[Actor].say_hello.[Other]:

	"Hello, friend"
	"Hi there."
	"Well goodday to you, sir"

With the condition tags

actors.[Actor].relationship.[Other].friendly
```

Thus, in a post condition of an action we could have

```
 text speech_act.[Actor].say_hello.[Other]
```

which will unwrap onto one of the three greetings associated with the tag (parameterized)

#### Dialogue

The problem about turntaking has to be considered in the current practice model. In a normal Alice/ SpiritAI dialogue design we match user-input patterns and returns appropriate answers to the matched input. This is one functionality of practice. In practice this could be something like:
```
Practice Conversation

	Action How_are_u
		PreCondtions
			Actor.[Agent] and 
			[Agent] == [Speaker] and
			not [Parent].speech_act.[Agent].say_hello.[Other]
		PostConditions
			Text speech_act.[Agent].say_hello.[Other]
			Insert [Parent].speech_act.[Agent].say_hello.[Other]
			[Speaker]=[Other]

	Action Answer_mood
		Preconditions
			Actor.[Agent] and 
			[Agent] == [Speaker] and
			[Parent].speech_act.[Agent].say_hello.[Other]
		PostConditions
			Text speech_act.[Agent].tell_mood.[Other]
			Insert [Parent].speech_act.[Agent].tell_mood.[Other]
			[Speaker]=None

```

This would result in a dialogue like this:

> Mr. Brown asks Ms. Lucy: How are you, my dear?
> Ms. Lucys replies: "Fine, thanks mr. Brown."
> Ms. Lucy asks Mr. Brown: "How are you today, sir?"
> Mr. Browns replies: "Well to be hornest, my dear, not that well."

```
Sexism: 
=======
process.leader.[other] * actors.[other].gender!male

Provocataur (likes to provoke upperclass men):
===============================================
actors.[other].upperclass * actors.[other].gender!male * actors.[other].relationship.[self].is_displeased

Hates to be alone:
==================

locations.[location]![self]

```


### Notes and observations on Emergence 

Emotions creates goals.

Emergence: self-assembly - collectives emerge because each component looks to it's neighbors for cues on how to behave. 

 - More is different
 - Ignorance is useful
 - Encourage random encounters
 - Look for patterns in the signs
 - Pay atttention to your neighbors "Local information can lead to global wisdom"