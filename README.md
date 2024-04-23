# Apartment and Chair Delivery
A coding challenge solution.

## The problem
Apartment And Chair Delivery Limited has a unique position on the housing market. The company not only builds apartments, but also equips them with chairs.
Now the business has grown continuously over the past few years and there are a few organizational problems that could be solved by automation.

We will focus on one of them here:

While a new residential building is erected, the chairs that are to be placed there need to be produced. In order to be able to plan this, the home buyers indicate the desired position of the armchairs in their home on a floor plan at the time of purchase. These plans are collected, and the number of different chairs to be produced are counted from them. The plans are also used to steer the workers carrying the chairs into the building when furnishing the apartments.

In the recent past, when manually counting the various types of chairs in the floor plans, many mistakes were made and caused great resentment among customers. That is why the owner of the company asked us to automate this process.

Unfortunately, the plans are in a very old format (the company's systems are still from the eighties), so modern planning software cannot be used here. An example of such an apartment plan is [attached](#example-plan).

We now need a command line tool that reads in such a file and outputs the following information:
- Number of different chair types for the apartment
- Number of different chair types per room

The different types of chairs are as follows:
- `W`: wooden chair
- `P`: plastic chair
- `S`: sofa chair
- `C`: china chair

The output must look like this so that it can be read in with the old system:
```
total:
W: 3, P: 2, S: 0, C: 0
living room:
W: 3, P: 0, S: 0, C: 0
office:
W: 0, P: 2, S: 0, C: 0
```
The names of the rooms must be sorted alphabetically in the output.

Our sales team has promised Apartment And Chair Delivery Limited a solution within 5 days from now. I know that is very ambitious, but as you are our best developer, we all count on you.


### Example plan
```
+-----------+------------------------------------+
|           |                                    |
| (closet)  |                                    |
|         P |                            S       |
|         P |         (sleeping room)            |
|         P |                                    |
|           |                                    |
+-----------+    W                               |
|           |                                    |
|        W  |                                    |
|           |                                    |
|           +--------------+---------------------+
|                          |                     |
|                          |                W W  |
|                          |    (office)         |
|                          |                     |
+--------------+           |                     |
|              |           |                     |
| (toilet)     |           |             P       |
|   C          |           |                     |
|              |           |                     |
+--------------+           +---------------------+
|              |           |                     |
|              |           |                     |
|              |           |                     |
| (bathroom)   |           |      (kitchen)      |
|              |           |                     |
|              |           |      W   W          |
|              |           |      W   W          |
|       P      +           |                     |
|             /            +---------------------+
|            /                                   |
|           /                                    |
|          /                          W    W   W |
+---------+                                      |
|                                                |
| S                                   W    W   W |
|                (living room)                   |
| S                                              |
|                                                |
|                                                |
|                                                |
|                                                |
+--------------------------+---------------------+
                           |                     |
                           |                  P  |
                           |  (balcony)          |
                           |                 P   |
                           |                     |
                           +---------------------+
```

## Solution
The solution for this would be to scan predefined areas for known symbols and substrings.

Since our input is text and _the plans are in a very old format (the company's systems are still from the eighties)_, here go few assumptions:
1. input map size will be reasonably small:
   1. safe to load in memory
   2. not requiring complex scanning algorithms
2. input file will have a single-byte character set, let's assume it is `cp850`

Out of _1.2_ we can choose a simple _flood fill algorithm_, its non-recursive implementation.

### Implementation
Solution keeps text input as map representation in memory, almost unmodified (only room names are extracted and replaced by whitespace).

Scanning the map room-by-room starts at location of room name.
Scanning algorithm is non-recursive flood fill with two modifications:
- it _iterates_ over horizontal line, not _enqueues_ neighbor points
- it will enque next points only on above and below lines, only when seeing a wall, thus reducing the queue size and a number of main cycle iterations

Example:
```
o - scan starting point
<- - scan direction
x - enqued points
|+- - wall characters

+---+  +-------+
|x  +--+x     x|
|<---  o   --->|
|||x  C       x|
|              |
+--------------+
```
### Limitations
1. Map is expected to be in single byte character set, out of _the company's systems are still from the eighties_ condition. In case of multibyte characters, walls will get shifted, which may lead to ...
2. Connected rooms (as a result of unclosed walls) will be treated as a single room, despite ...
3. Multiple names of one room: all will appear in the output, all but first one (top- and leftmost on the map) will have zero counters
4. Duplicate room names will be numbered, starting from second occurence: _The Room_, _The Room 1_, _The Room 2_, e.t.c.
5. Rooms without names will not be scanned
6. Room names cannot contain `)` character, must be enclosed between `(` and `)`
7. Any other characters besides `WALLS` and `CHAIRS` definitions will be ignored.
8. Empty lines in the map file will act as walls, so there shouldn't be any.
9. Passage between walls and corners must be at least 1 character wide:
```
Not passages:
..   ..   ·--·      |
||   \\   ·--·  ·--+
··    ··           +--·
                  |

Valid passages:
. .   . .   ·--·    |
| |   \ \       ·--+
· ·    · ·  ·--·      +---·
                     |
```
### Complexity
Solution time complexity is $O(M * N)$, where _M_ and _N_ are map dimensions. This is a worst case scenario, usually it will be less.
