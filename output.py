import itertools
import math

# City Bank branch locations with Lat Lon
city_bank_locations = [
    {"name": "Uttara Branch", "lat": '23.8728568', "lon": '90.3984184'},
    {"name": "City Bank Airport", "lat": '23.8513998', "lon": '90.3944536'},
    {"name": "City Bank Nikunja", "lat": '23.8330429', "lon": '90.4092871'},
    {"name": "City Bank Beside Uttara Diagnostic", "lat": '23.8679743', "lon": '90.3840879'},
    {"name": "City Bank Mirpur 12", "lat": '23.8248293', "lon": '90.3551134'},
    {"name": "City Bank Le Meridien", "lat": '23.827149', "lon": '90.4106238'},
    {"name": "City Bank Shaheed Sarani", "lat": '23.8629078', "lon": '90.3816318'},
    {"name": "City Bank Narayanganj", "lat": '23.8673789', "lon": '90.429412'},
    {"name": "City Bank Pallabi", "lat": '23.8248938', "lon": '90.3549467'},
    {"name": "City Bank JFP", "lat": '23.813316', "lon": '90.4147498'}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance

# Find the index of the Uttara Branch
uttara_branch_index = None
for i, branch in enumerate(city_bank_locations):
    if branch["name"] == "Uttara Branch":
        uttara_branch_index = i
        break

if uttara_branch_index is None:
    print("Uttara Branch not found in the branch locations.")
    exit()

# Calculate the distance matrix
distance_matrix = []
for origin in city_bank_locations:
    row = []
    for dest in city_bank_locations:
        if origin["name"] == dest["name"]:
            row.append(0.0)
        else:
            distance = calculate_distance(origin["lat"], origin["lon"], dest["lat"], dest["lon"])
            row.append(distance)
    distance_matrix.append(row)

# Remove the Uttara Branch from the City Bank locations list
del city_bank_locations[uttara_branch_index]

# Adjust the distance matrix
distance_matrix.pop(uttara_branch_index)
for row in distance_matrix:
    del row[uttara_branch_index]

def calculate_total_distance(route):
    total_distance = 0.0
    for i in range(len(route) - 1):
        origin_index = route[i]
        dest_index = route[i + 1]
        total_distance += distance_matrix[origin_index][dest_index]
    return total_distance

# Generate all possible permutations of the locations
num_locations = len(city_bank_locations)
all_permutations = list(itertools.permutations(range(num_locations)))

# Find the permutation with the minimum total distance
best_route = None
min_distance = float('inf')

for perm in all_permutations:
    distance = calculate_total_distance(perm)
    if distance < min_distance:
        min_distance = distance
        best_route = perm

# Insert the Uttara Branch back at the beginning of the route
best_route = (uttara_branch_index,) + best_route

# Print the optimized route
optimized_route = [city_bank_locations[index]["name"] for index in best_route]
print("Optimized Route from Uttara Branch:")
for location in optimized_route:
    print(location)
