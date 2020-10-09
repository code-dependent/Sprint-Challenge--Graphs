from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
def get_exits(room):
    exits = {}
    for d in player.current_room.get_exits():
        exits[d] = '?'
    return exits

def step_back(direction):
    a = ['n','s','e','w']
    b = ['s','n','w','e']
    reverse = dict(zip(a,b))
    return reverse[direction]

# get_opposite('n')

def traverse_world(current_room_id, visited = None):

    """
    Print each vertex in depth-first order
    beginning from starting_vertex.
    """
    # if visited is not passed as param initialize visited to be an empty set
    if not visited:
        visited = set()
    # initailize the return path
    path = []
    # for each key returned from get_exits(current_room_id)
    for direction in get_exits(current_room_id):
        # travel in that direction
        player.travel(direction)
        # if we have not visited this player.current_room.id
        if player.current_room.id not in visited:
            # add player.current_room.id to the visited set
            visited.add(player.current_room.id)
            # append the direction to the return path; because we now know that it is a room we havent traveled to yet
            path.append(direction)
            # how we join the return path with the list that is returned
            # from recursing on player.current_room.id
            path += traverse_world(player.current_room.id,visited)
            # append the {opposite_direction} of "direction"
            path.append(step_back(direction))
            # then travel back to {current_room_id} and prepare to move one of the other directions
            player.travel(step_back(direction))

        else:
            # travel back to {current_room_id} and prepare to try a different direction
            player.travel(step_back(direction))

    return path

traversal_path+= traverse_world(player.current_room.id)
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
