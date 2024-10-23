import sys

road_connections = {}
successors = set()
nodes_popped = 0
nodes_generated = 1
nodes_expanded = 0
heuristic_data = {}
route = False

if len(sys.argv) == 4:
    origin_city = sys.argv[2]
    goal_city = sys.argv[3]
    filename = sys.argv[1]

    # Reading the input file to understand the map
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break
            source_city, destination_city, road_length = line.strip().split()
            source_city = source_city.lower().replace("_", " ")
            destination_city = destination_city.lower().replace("_", " ")
            if source_city not in road_connections:
                road_connections[source_city] = {}
            if destination_city not in road_connections:
                road_connections[destination_city] = {}
            road_connections[source_city][destination_city] = float(road_length)
            road_connections[destination_city][source_city] = float(road_length)
           
    # Uninformed Search
    fringe_queue = [(0, origin_city, [], 0, None)]
    visited = set()

    while fringe_queue:
        fringe_queue.sort() 
        length, city_name, path, depth, parent_city = fringe_queue.pop(0) 
        nodes_popped += 1
        if city_name.lower() == goal_city.lower():
            print(f"\nNodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            print(f"Distance: {length} km")
            print(f"Depth: {depth}")
            print("Route:")
            if origin_city.lower() == goal_city.lower():
                print(f"{origin_city} to {goal_city}, {length}km")
            else:
                for i in range(len(path) - 1):
                    source_city = path[i].replace("_", " ")
                    destination_city = path[i+1].replace("_", " ")
                    print(f"{path[i].capitalize()} to {path[i+1].capitalize()}, {road_connections[path[i]][path[i+1]]} km")
                print(f"{path[-1].capitalize().replace('_', ' ')} to {goal_city.replace('_', ' ')}, {road_connections[path[-1]][city_name]} km")  
            route = True
            break

        if city_name.lower() not in visited:
            visited.add(city_name.lower())
            nodes_expanded += 1
            successors = road_connections[city_name.lower()]      
            for neighbour_city, distance in successors.items():
                g_n = length + distance
                upd_path = path + [city_name.lower()]
                fringe_queue.append((g_n, neighbour_city, upd_path, depth + 1, (length, city_name, path)))
                nodes_generated += 1  
        else:
            continue

    if not route :
        print(f"\nNodes Popped: {nodes_popped}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Nodes Generated: {nodes_generated}")
        print(f"Route: None")
        print(f"Distance: Infinite")
        print(f"\n** There is no route from {sys.argv[2]} to {sys.argv[3]} **\n")
       

elif len(sys.argv) == 5:
    origin_city = sys.argv[2].lower()
    goal_city = sys.argv[3].lower()
    filename = sys.argv[1]
    heuristic_filename = sys.argv[4]

    # Reading the input file to understand the map
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break
            source_city, destination_city, road_length = line.strip().split()
            source_city = source_city.lower().replace("_", " ")
            destination_city = destination_city.lower().replace("_", " ")
            if source_city not in road_connections:
                road_connections[source_city] = {}
            if destination_city not in road_connections:
                road_connections[destination_city] = {}
            road_connections[source_city][destination_city] = float(road_length)
            road_connections[destination_city][source_city] = float(road_length)
    

    # Reading the heuristic values
    with open(heuristic_filename, 'r') as file:
        for line in file:
            if line.strip() == "END OF INPUT":
                break

            city, heuristic_value = line.strip().split()
            city = city.lower().replace("_", " ")

            if heuristic_value.strip().isdigit():
                heuristic_data[city] = int(heuristic_value)
            else:
                print(f"Warning: Unable to fetch info from heuristic file.")

    # Informed Search
    fringe_queue = [(heuristic_data[sys.argv[2].lower()], sys.argv[2], [], None)]
    visited = set()
    while fringe_queue:
        fringe_queue.sort() 
        length, city_name, path, parent_city = fringe_queue.pop(0)  
        nodes_popped += 1
        goal_city = sys.argv[3]
        if city_name.lower() == goal_city.lower():
            print(f"\nNodes Popped: {nodes_popped}")
            print(f"Nodes Expanded: {nodes_expanded}")
            print(f"Nodes Generated: {nodes_generated}")
            if origin_city.lower() == goal_city.lower():
                length = length - heuristic_data[sys.argv[2].lower()]
                print(f"\nDistance: {length} km")
                print(f"Route:")
                print(f"{origin_city} to {goal_city}, {length}km")
            else:
                print(f"\nDistance: {length} km")
                print(f"Route:")
                for i in range(len(path) - 1):
                    source_city = path[i].replace("_", " ")
                    destination_city = path[i+1].replace("_", " ")
                    print(f"{path[i].capitalize()} to {path[i+1].capitalize()}, {road_connections[path[i]][path[i+1]]} km")
                print(f"{path[-1].capitalize().replace('_', ' ')} to {goal_city.replace('_', ' ')}, {road_connections[path[-1]][city_name]} km")  
            route = True
            break

        if city_name.lower() not in visited:
            visited.add(city_name.lower())
            nodes_expanded += 1
            successors = road_connections[city_name.lower()]
            for neighbour_city, distance in successors.items():
                current_heuristic_value = heuristic_data.get(city_name.lower(), 0)
                neighbour_heurisitic_value = heuristic_data.get(neighbour_city.lower(), 0)
                g_h_n = length - current_heuristic_value + distance + neighbour_heurisitic_value
                upd_path = path + [city_name.lower()]
                fringe_queue.append((g_h_n, neighbour_city, upd_path, (length-current_heuristic_value, city_name, path)))
                nodes_generated += 1      
        else:
            continue

    if not route :
        print(f"\nNodes Popped: {nodes_popped}")
        print(f"Nodes Expanded: {nodes_expanded}")
        print(f"Nodes Generated: {nodes_generated}")
        print(f"Route: None")
        print(f"Distance: Infinite")
        print(f"\n** There is no route from {sys.argv[2]} to {sys.argv[3]} **\n")

else:
    print("!! Warning !! \n Input Format: \n  find_route input1.txt origin_city destination (For doing Uninformed Search) \n or \n  find_route input.txt origin_city destination heuristic.txt (For doing Informed Search)")
        



        
        
