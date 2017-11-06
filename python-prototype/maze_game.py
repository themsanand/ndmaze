import numpy
import random
import copy
import time
import heapq

#Nearby is likely to be called for a single position many times, especially in higher-dimensional maze boards
nearby_given_position = {}
not_valid = set()
valid_nearby = set()

flag0 = True

def createMazeBoard(size):
	return numpy.zeros(shape=size)

def nearbyPositions(next_position, shape):
	if next_position in nearby_given_position:
		return nearby_given_position[next_position]
	list_of_locations = []
	for dimension, location_in_dim in enumerate(next_position):
		firstEdgeFlag = True
		secondEdgeFlag = True
		if location_in_dim == 0:
			firstEdgeFlag = False
		if location_in_dim == shape[dimension] - 1:
			secondEdgeFlag = False
		if firstEdgeFlag:
			new_position = list(next_position)
			new_position[dimension] -= 1
			list_of_locations.append(tuple(new_position))
		if secondEdgeFlag:
			new_position = list(next_position)
			new_position[dimension] += 1
			list_of_locations.append(tuple(new_position))
	list_of_locations = [tuple(loc) for loc in list_of_locations]
	nearby_given_position[next_position] = list_of_locations
	return list_of_locations

def manhattan_distance(p1, p2):
	sum = 0
	for i in range(len(p1)):
		sum += abs(p1[i] - p2[i])
	return sum

def is_valid(path_set, location, shape, end):
	if location == end:
		return True
	if location in not_valid or location in path_set:
		return False
	visited_nearby = [loc for loc in nearbyPositions(location, shape) if loc in path_set]

	if len(visited_nearby) > 1:
		for near1 in visited_nearby:
			for near2 in visited_nearby:
				set(nearbyPositions(near1, shape)).isdisjoint(nearbyPositions(near2, shape))
				if near1 != near2 and not set(nearbyPositions(near1, shape)).isdisjoint(nearbyPositions(near2, shape)):
					not_valid.add(location)
					return False
		return True
	else:
		return True

def createMazePath(shape):
	path_set = set()
	path_set.add(tuple([0 for dimension in shape]))
	valid_nearby.add(tuple([0 for dimension in shape]))
	not_valid.add(tuple([0 for dimension in shape]))
	end = tuple([dimension - 1 for dimension in shape])
	countr, t = 100, time.time()
	while not end in path_set:
		#Random.choice of set-to-tuple is faster than sampling 1
		if valid_nearby:
			next_to_next_position = random.choice(tuple(valid_nearby))
			next_position = False
			possible_nearby_locations = nearbyPositions(next_to_next_position, shape)
			random.shuffle(possible_nearby_locations)
			for possible_next in possible_nearby_locations:
				if is_valid(path_set, possible_next, shape, end):
					next_position = possible_next
					break
			if next_position:
				path_set.add(next_position)
				valid_nearby.add(next_position)
				not_valid.add(next_position)
			else:
				valid_nearby.remove(next_to_next_position)
		else:
			#Add position with closest Manhattan distance to end into path_set that isn't already in path_set
			manhattan_pqueue = []
			for loc in path_set:
				for pos in nearbyPositions(loc, shape):
					heapq.heappush(manhattan_pqueue, (manhattan_distance(end, pos), pos))
				popped_manhattan = heapq.heappop(manhattan_pqueue)
			while popped_manhattan[1] in path_set:
				popped_manhattan =  heapq.heappop(manhattan_pqueue)
			path_set.add(popped_manhattan[1])
			last_msum = popped_manhattan[0]
			valid_nearby.add(popped_manhattan[1])
		if len(path_set) % countr == 0:
			print("PATH:", len(path_set), time.time() - t)
			countr += int(countr / 2)
			t = time.time()
	board = numpy.zeros(shape)
	for el in path_set:
		board[el[0]][el[1]] = 1
	for r in board:
		print(r)
	size = 1
	for x in shape:
		size *= x
	print(len(path_set) / size)

if __name__ == "__main__":
	t_begin = time.time()
	createMazePath(tuple([100, 100, 100]))
	print(time.time() - t_begin)