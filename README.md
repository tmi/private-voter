# Intro
This is a concept of a simple web application + DB to allow reasonably private voting, or rather, polling.
By polling, we understand here the ability to create polls with a fixed set of choices, and allowing a fixed set of actors (IDs) to pick exactly one choice.
We have the following privacy/accuracy requirements:
* If the attacker gets hold of the databases (or any set of their snapshots in time), they are not able to determine who voted how with probability one.
* If the attacker controls the web application itself, its source of randomness, or the temporary storage/queue systems, no guarantees are given.
* Voting multiple times by a single actor should be, if possible, prevented, or at least detected. It is not required to identify which votes were cast by the same actor, it is enough just to give counts of unique actors vs total votes.
* The results of the voting are not required to be exact, in particular, the poll creator can specify the properties of a probabilistic distribution that is added to the results.
* The application should be fault-tolerant and scalable.

This application is not expected to see any serious production deploy -- it rather serves as a demonstration of a concept and a programming exercise.

## Design
Whenever the application receives a vote, in the form of `(actor_id, vote)`, it inserts it into a temporary queue this tuple (plus a randomly generated id to provide deduplication in case of a fault) *alongside* randomly generated votes according to the poll creator's specification, and in a random order.
This queue has two consumers -- one that persists only the `actor_id` to a table, to facilitate double voting detection/prevention, and another one that persists only the `random_id` and `vote` parts, to allow the actual vote counting. Both consumers read from the queue in batches, and persist to the database in a random order.

Presumably, the database will keep `atime`/`ctime` fields for records, which could possibly allow pairing rows between those two tables and thus break the privacy (though the random ordering complicates this somehow).
This can be further strengthened by a process that updates/re-creates record in either table.

## Development plan
1. Single flask app in docker with in-memory SQL with `/create` and `/vote` without any reliability or queing or caching
2. Docker replaced with docker-compose and external SQL is introduced
3. App separated into two plus queue is introduced
4. AWS deployment is prepared via ECS, Kinesis, Aurora
5. Rewritten to EKS
