############################################################
## CSC 384, Intro to AI, University of Toronto.
## Assignment 1 Starter Code
## v1.1
##
## Changes: 
## v1.1: removed the hfn paramete from dfs. Updated solve_puzzle() accordingly.
############################################################

from typing import List
import heapq
from heapq import heappush, heappop
import time
import argparse
import math # for infinity
import copy

from board import *

def is_goal(state):
    """
    Returns True if the state is the goal state and False otherwise.

    :param state: the current state.
    :type state: State
    :return: True or False
    :rtype: bool
    """
    available_storage = state.board.storage.copy()
    for box in state.board.boxes:
        for storage in available_storage:
            print(storage)
            if box[0] == storage[0] and box[1] == storage[1]:
                available_storage.remove(storage)
                break
    if len(available_storage) == 0:
        return True
    else:
        return False
    
    #raise NotImplementedError


def get_path(state):
    """
    Return a list of states containing the nodes on the path 
    from the initial state to the given state in order.

    :param state: The current state.
    :type state: State
    :return: The path.
    :rtype: List[State]
    """
    path = []
    curr_state = state
    while curr_state is not None:
        path.append(curr_state)
        curr_state = curr_state.parent
    path.reverse()
    return path

    raise NotImplementedError

def is_obstacle(location, state):
    for obstacle in state.board.obstacles:
        if obstacle[0] == location[0] and obstacle[1] == location[1]:
            return True
    
    return False

def is_box(location, state):
    for box in state.board.boxes:
        if box[0] == location[0] and box[1] == location[1]:
            return True
    
    return False

def is_robot(location, state):
    for robot in state.board.robots:
        if robot[0] == location[0] and robot[1] == location[1]:
            return True

    return False

def copy_board(board: Board):
    new_board = Board(board.name, board.width, board.height, copy.deepcopy(board.robots), 
                      copy.deepcopy(board.boxes), board.storage, board.obstacles)
    return new_board

def copy_state(state: State):
    new_state = State(copy_board(state.board), state.hfn, state.f, state.depth, state.parent)
    return new_state

def get_successors(state):
    """
    Return a list containing the successor states of the given state.
    The states in the list may be in any arbitrary order.

    :param state: The current state.
    :type state: State
    :return: The list of successor states.
    :rtype: List[State]
    """
    temp_state = copy_state(state)
    state_list = []
    temp_state.depth = state.depth + 1
    temp_state.parent = state
    for robIndex in range(len(temp_state.board.robots)):
        #see if robot can move up:
        robot = temp_state.board.robots[robIndex]
        if is_obstacle((robot[0], robot[1]+1), temp_state) == False and is_robot((robot[0], robot[1]+1), temp_state) == False:
            if is_box((robot[0], robot[1]+1), temp_state) == True:
                #The case where there is a box in the robots path but no obstacle preventing them from pushing it
                if(is_obstacle((robot[0], robot[1]+2), temp_state) == False and 
                is_box((robot[0], robot[1]+2), temp_state) == False and
                is_robot((robot[0], robot[1]+2), temp_state) == False):
                    for boxIndex in range(len(temp_state.board.boxes)):
                        if(temp_state.board.boxes[boxIndex][0] == robot[0] and 
                        temp_state.board.boxes[boxIndex][1] == robot[1]+1):
                            listBox = list(temp_state.board.boxes[boxIndex])
                            listBox[1] += 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            listRobot = list(temp_state.board.robots[robIndex])
                            listRobot[1] += 1
                            temp_state.board.robots[robIndex] = tuple(listRobot)
                            state_list.append(copy_state(temp_state))

                            #Reset temp state
                            listRobot[1] -= 1
                            listBox[1] -= 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            temp_state.board.robots[robIndex] = tuple(listRobot)
            #The case where there is no box or obstacle obstructing the robots path            
            else:
                listRobot = list(temp_state.board.robots[robIndex])
                listRobot[1] += 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
                state_list.append(copy_state(temp_state))

                #Reset temp state
                listRobot[1] -= 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
    
        #see if robot can move down:
        if is_obstacle((robot[0], robot[1]-1), temp_state) == False and is_robot((robot[0], robot[1]-1), temp_state) == False:
            if is_box((robot[0], robot[1]-1), temp_state) == True:
                #The case where there is a box in the robots path but no obstacle preventing them from pushing it
                if(is_obstacle((robot[0], robot[1]-2), temp_state) == False and 
                is_box((robot[0], robot[1]-2), temp_state) == False and
                is_robot((robot[0], robot[1]-2), temp_state) == False):
                    for boxIndex in range(len(temp_state.board.boxes)):
                        if(temp_state.board.boxes[boxIndex][0] == robot[0] and 
                        temp_state.board.boxes[boxIndex][1] == robot[1]-1):
                            listBox = list(temp_state.board.boxes[boxIndex])
                            listBox[1] -= 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            listRobot = list(temp_state.board.robots[robIndex])
                            listRobot[1] -= 1
                            temp_state.board.robots[robIndex] = tuple(listRobot)
                            state_list.append(copy_state(temp_state))

                            #Reset temp state
                            listRobot[1] += 1
                            listBox[1] += 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            temp_state.board.robots[robIndex] = tuple(listRobot)
                    
            #The case where there is no box or obstacle obstructing the robots path            
            else:
                listRobot = list(temp_state.board.robots[robIndex])
                listRobot[1] -= 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
                state_list.append(copy_state(temp_state))

                #Reset temp state
                listRobot[1] += 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
    

        #see if robot can move left:
        if is_obstacle((robot[0]-1, robot[1]), temp_state) == False and is_robot((robot[0]-1, robot[1]), temp_state) == False:
            if is_box((robot[0]-1, robot[1]), temp_state) == True:
                #The case where there is a box in the robots path but no obstacle preventing them from pushing it
                if(is_obstacle((robot[0]-2, robot[1]), temp_state) == False and 
                is_box((robot[0]-2, robot[1]), temp_state) == False and
                is_robot((robot[0]-2, robot[1]), temp_state) == False):
                    for boxIndex in range(len(temp_state.board.boxes)):
                        if (temp_state.board.boxes[boxIndex][0] == robot[0]-1 and 
                        temp_state.board.boxes[boxIndex][1] == robot[1]):
                            listBox = list(temp_state.board.boxes[boxIndex])
                            listBox[0] -= 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            listRobot = list(temp_state.board.robots[robIndex])
                            listRobot[0] -= 1
                            temp_state.board.robots[robIndex] = tuple(listRobot)
                            state_list.append(copy_state(temp_state))

                            #Reset temp state
                            listRobot[0] += 1
                            listBox[0] += 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            temp_state.board.robots[robIndex] = tuple(listRobot)
 
            #The case where there is no box or obstacle obstructing the robots path            
            else:
                listRobot = list(temp_state.board.robots[robIndex])
                listRobot[0] -= 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
                state_list.append(copy_state(temp_state))

                #Reset temp state
                listRobot[0] += 1
                temp_state.board.robots[robIndex] = tuple(listRobot)


        #see if robot can move right:
        if is_obstacle((robot[0]+1, robot[1]), temp_state) == False and is_robot((robot[0]+1, robot[1]), temp_state) == False:
            if is_box((robot[0]+1, robot[1]), temp_state) == True:
                #The case where there is a box in the robots path but no obstacle preventing them from pushing it
                if(is_obstacle((robot[0]+2, robot[1]), temp_state) == False and 
                is_box((robot[0]+2, robot[1]), temp_state) == False and
                is_robot((robot[0]+2, robot[1]), temp_state) == False):
                    for boxIndex in range(len(temp_state.board.boxes)):
                        if (temp_state.board.boxes[boxIndex][0] == robot[0]+1 and 
                        temp_state.board.boxes[boxIndex][1] == robot[1]):
                            listBox = list(temp_state.board.boxes[boxIndex])
                            listBox[0] += 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            listRobot = list(temp_state.board.robots[robIndex])
                            listRobot[0] += 1
                            temp_state.board.robots[robIndex] = tuple(listRobot)
                            state_list.append(copy_state(temp_state))

                            #Reset temp state
                            listRobot[0] -= 1
                            listBox[0] -= 1
                            temp_state.board.boxes[boxIndex] = tuple(listBox)
                            temp_state.board.robots[robIndex] = tuple(listRobot)
            #The case where there is no box or obstacle obstructing the robots path            
            else:
                listRobot = list(temp_state.board.robots[robIndex])
                listRobot[0] += 1
                temp_state.board.robots[robIndex] = tuple(listRobot)
                state_list.append(copy_state(temp_state))

                #Reset temp state
                listRobot[0] -= 1
                temp_state.board.robots[robIndex] = tuple(listRobot)

    

    return state_list
    raise NotImplementedError

def multi_prune(state, visited):
    if str(state.board) in visited:
        return True
    return False

def moveState(direction, pos_Neg, temp_State, robIndex):
    return

def dfs(init_board):
    """
    Run the DFS algorithm given an initial board.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial board.
    :type init_board: Board
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    init_state = State(init_board, heuristic_zero, 0, 0)
    frontier = []
    explored = []
    explored = {str(init_state.board)}
    heapq.heappush(frontier,(0, init_state))
    counter = 0
    key = -1
    #Want to see if we can make more efficient with pruning
    """
    while len(frontier) > 0:
        curr_state = heapq.heappop(frontier)
        explored.add(str(curr_state.board))
        if is_goal(curr_state):
            return get_path(curr_state), curr_state.cost
        successors = get_successors(curr_state)
        for successor in successors:
            if str(successor.board) not in explored:
                heapq.heappush(frontier, successor)
    """
    while len(frontier) > 0:
        currState = heappop(frontier)[1]
        if is_goal(currState):
            return get_path(currState), len(get_path(currState))-1
        else:
            successors_list = get_successors(currState)
            for successor_index in range(len(successors_list)):
                if multi_prune(successors_list[successor_index], explored) == False:
                    heapq.heappush(frontier, (key, successors_list[successor_index]))
                    key -= 1
                    explored.add(str(successors_list[successor_index].board))
        counter += 1
        if counter == 999:
            currState.board.display()
    return [], -1

    raise NotImplementedError


def a_star(init_board, hfn):
    """
    Run the A_star search algorithm given an initial board and a heuristic function.

    If the function finds a goal state, it returns a list of states representing
    the path from the initial state to the goal state in order and the cost of
    the solution found.
    Otherwise, it returns am empty list and -1.

    :param init_board: The initial starting board.
    :type init_board: Board
    :param hfn: The heuristic function.
    :type hfn: Heuristic (a function that consumes a Board and produces a numeric heuristic value)
    :return: (the path to goal state, solution cost)
    :rtype: List[State], int
    """
    init_state = State(init_board, hfn, hfn(init_board), 0)
    frontier = []
    explored = {str(init_state.board)}
    heapq.heappush(frontier, (init_state.f, init_state))
    counter = 0

    while len(frontier) > 0:
        currState = heappop(frontier)[1]
        if is_goal(currState):
            return get_path(currState), len(get_path(currState))-1
        else:
            successors_list = get_successors(currState)
            for successor_index in range(len(successors_list)):
                if(multi_prune(successors_list[successor_index], explored) == False):
                    heapq.heappush(frontier, ((hfn(successors_list[successor_index].board) + successors_list[successor_index].depth),successors_list[successor_index]))                             
                    explored.add(str(successors_list[successor_index].board))

        counter += 1
        if counter == 999:
            currState.board.display()
    return [], -1

    raise NotImplementedError


def heuristic_basic(board):
    """
    Returns the heuristic value for the given board
    based on the Manhattan Distance Heuristic function.

    Returns the sum of the Manhattan distances between each box 
    and its closest storage point.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """
    manhattan_sum = 0
    for box in board.boxes:
        box_x_y = list(box)
        closest_goal_distance = float('inf')
        for goal in board.storage:
            goal_x_y = list(goal)
            manhattan = abs(goal_x_y[0] - box_x_y[0]) + abs(goal_x_y[1] - box_x_y[1])
            if(manhattan < closest_goal_distance):
                closest_goal_distance = manhattan
        manhattan_sum += closest_goal_distance

    return manhattan_sum
    raise NotImplementedError


def heuristic_advanced(board):
    """
    An advanced heuristic of your own choosing and invention.

    :param board: The current board.
    :type board: Board
    :return: The heuristic value.
    :rtype: int
    """

    #Assign each storage to the closest box and then remove it from the available boxes
    cooler_manhattan_sum = 0
    available_goals = []
    available_box = []
    for box in board.boxes:
        available_box.append(box)

    for goal in board.storage:
        available_goals.append(goal)

    for goal in available_goals:
        closest_box = available_box[0]
        closest_distance = abs(list(closest_box)[0] - list(goal)[0]) + abs(list(closest_box)[1] - list(goal)[1])
        for box in available_box:
            if(abs(list(box)[0] - list(goal)[0]) + abs(list(box)[1] - list(goal)[1]) < closest_distance):
                closest_distance = abs(list(box)[0] - list(goal)[0]) + abs(list(box)[1] - list(goal)[1])
                closest_box = box
        cooler_manhattan_sum += closest_distance       
        available_box.remove(closest_box)
    return cooler_manhattan_sum
    raise NotImplementedError


def solve_puzzle(board: Board, algorithm: str, hfn):
    """
    Solve the given puzzle using the given type of algorithm.

    :param algorithm: the search algorithm
    :type algorithm: str
    :param hfn: The heuristic function
    :type hfn: Optional[Heuristic]

    :return: the path from the initial state to the goal state
    :rtype: List[State]
    """

    print("Initial board")
    board.display()

    time_start = time.time()

    if algorithm == 'a_star':
        print("Executing A* search")
        path, step = a_star(board, hfn)
    elif algorithm == 'dfs':
        print("Executing DFS")
        path, step = dfs(board)
    else:
        raise NotImplementedError

    time_end = time.time()
    time_elapsed = time_end - time_start

    if not path:

        print('No solution for this puzzle')
        return []

    else:

        print('Goal state found: ')
        path[-1].board.display()

        print('Solution is: ')

        counter = 0
        while counter < len(path):
            print(counter + 1)
            path[counter].board.display()
            print()
            counter += 1

        print('Solution cost: {}'.format(step))
        print('Time taken: {:.2f}s'.format(time_elapsed))

        return path


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The file that contains the solution to the puzzle."
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        required=True,
        choices=['a_star', 'dfs'],
        help="The searching algorithm."
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        required=False,
        default=None,
        choices=['zero', 'basic', 'advanced'],
        help="The heuristic used for any heuristic search."
    )
    args = parser.parse_args()

    # set the heuristic function
    heuristic = heuristic_zero
    if args.heuristic == 'basic':
        heuristic = heuristic_basic
    elif args.heuristic == 'advanced':
        heuristic = heuristic_advanced

    # read the boards from the file
    board = read_from_file(args.inputfile)

    # solve the puzzles
    path = solve_puzzle(board, args.algorithm, heuristic)

    # save solution in output file
    outputfile = open(args.outputfile, "w")
    counter = 1
    for state in path:
        print(counter, file=outputfile)
        print(state.board, file=outputfile)
        counter += 1
    outputfile.close()