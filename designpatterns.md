### Design patterns for social practices

Social practices is a protocol for social acts. Thus the protocol should contain a number of actions executed by agents participating in the practice. The practice should point to which actions are allowed, appropriate, unappropriate and not available at a given state. 

In order to distinquish between allowed and not available actions each action would need to have some preconditions which are conditioned on the global state (see below). When a social practice is executing its next steps it spawns allowed actions for each of the partipating agents. Actions are spawned for agents where the agent matches the acting agent - designated by the keyword AGENT. In an action the keyword AGENT therefore points to the agent carrying out the act. 

Social practices will have to contain a social state - a pointer to world state. It might be benficial to have a pointer to the local state relevant for the social practice and a global state which points to the world state. 

#### Execution loop

An execution of the game would entail executing all active social practices. This will result in spawning actions for each agent in the game. Each agent will evaluate which action is preferred based on localised maxima of simulating each action and compare the utility of the resulting states. 

When each agents preferred action is chosen - each preferred action is executed.


When the agent do his/her action other participants evaluates the action. Thus, if a player is split between several actions directed towards each of the other participants, the player has to choose and face whatever evaluation he/she receives based on the chosen action. Example, if a player has to return greetings from a company of three ladies with a compliment to each of them he knows he will disappoint two on behalf of the one he greets/compliments first. Given that he has higher evaluation of one of them he will suffer more from disappointing her. He will understand this when he carries out his evaluation of the three actions greet lady A, greet lady B and greet lady C. Thus, after his action is carried out each of the ladies will do a norm-evaluation of him. Each of the ladies expects that he greets them as a response to their greeting. A rule could guide him:

```
actors.[AGENT].likes.[OTHER] and actors.[OTHER].evaluation.[AGENT].minor_norm_violation -> utility -30
```

In order to detect a norm violation - the social practice may somehow run an action which is not dependent on an agent. So when a Actor is sending a greet to another an expects a greeting in return there is a need to evaluate if a flag indicating return of greeting has been removed.

Player A greets Player B -> practice.norm.greet_back.[player_A].[Player_B]
Player B does something else
The practice evaluates if there are any norms to be met:

<precondition>
 	practice.norm.greet_back.[player_A].[Player_B]
</precondition>
<postcondition>
	actors.[player_B].evaluates.[Player_A].minor_norm_violation
	actors.[player_B].evaluation.[Player_B]!neutral
</postcondition>


So the algorithm would be

run all practices
some will spawn actions at players
playerA = {preferred Action}
playerB = {preferred Action}
playerC = {preferred Action}

we could run in a random order queue

spawn -> {A,B,C} -> [A]
spawn -> {A,C}/[A] -> [C,A]
spawn -> {A,C}/[C,A] -> B kan ikke trække [] resettes
		 {A,C}/[] -> [A]
spawn -> {B,A}/[A] -> [B,A]
spawn -> {A,B,C}/[B,A] -> [C]

order is: [A,C,A,B,C]



