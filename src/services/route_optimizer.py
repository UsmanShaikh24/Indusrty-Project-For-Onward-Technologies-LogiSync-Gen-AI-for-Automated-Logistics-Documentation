from typing import List, Dict, Any
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from ..config import settings

class RouteOptimizer:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="logisync")
        
    def optimize_route(self, locations: List[str], cargo_details: Dict, time_constraints: Dict) -> Dict[str, Any]:
        # Convert locations to coordinates
        coordinates = []
        location_objects = []
        for loc in locations:
            location = self.geolocator.geocode(loc)
            if location:
                coordinates.append((location.latitude, location.longitude))
                location_objects.append(location)
        
        # Simple nearest neighbor algorithm
        current_index = 0
        route = [current_index]
        unvisited = list(range(1, len(coordinates)))
        
        while unvisited:
            current_coord = coordinates[current_index]
            nearest_index = min(
                unvisited,
                key=lambda i: geodesic(current_coord, coordinates[i]).meters
            )
            route.append(nearest_index)
            unvisited.remove(nearest_index)
            current_index = nearest_index
            
        # Format the solution
        optimized_route = []
        total_distance = 0
        prev_coord = None
        
        for idx in route:
            loc = location_objects[idx]
            coord = coordinates[idx]
            if prev_coord:
                total_distance += geodesic(prev_coord, coord).meters
            
            optimized_route.append({
                "location": locations[idx],
                "arrival_time": None,  # Would need actual time calculation
                "cargo_handling": cargo_details.get(str(idx), {})
            })
            prev_coord = coord
        
        # Add suggested fuel stops and compliance checkpoints
        result = {
            "optimized_route": optimized_route,
            "total_distance": total_distance,
            "fuel_stops": self._calculate_fuel_stops(optimized_route),
            "compliance_checkpoints": self._add_compliance_checkpoints(optimized_route)
        }
        
        return result
    
    def _calculate_fuel_stops(self, route: List[Dict]) -> List[Dict]:
        # Calculate optimal fuel stops based on vehicle range and route distance
        # This is a simplified implementation
        FUEL_RANGE = 500000  # 500 km in meters
        fuel_stops = []
        current_distance = 0
        
        for i in range(len(route)-1):
            location1 = self.geolocator.geocode(route[i]["location"])
            location2 = self.geolocator.geocode(route[i+1]["location"])
            
            if location1 and location2:
                distance = geodesic(
                    (location1.latitude, location1.longitude),
                    (location2.latitude, location2.longitude)
                ).meters
                current_distance += distance
                
                if current_distance > FUEL_RANGE * 0.8:  # Plan stop at 80% of range
                    fuel_stops.append({
                        "location": route[i]["location"],
                        "distance_from_start": current_distance
                    })
                    current_distance = 0
        
        return fuel_stops
        
    def _add_compliance_checkpoints(self, route: List[Dict]) -> List[Dict]:
        # Add required compliance checkpoints based on regulations
        # This is a simplified implementation
        MAX_DRIVING_TIME = 8 * 3600  # 8 hours in seconds
        checkpoints = []
        current_time = 0
        
        for i in range(len(route)):
            if i > 0:
                # Simulate time based on distance
                location1 = self.geolocator.geocode(route[i-1]["location"])
                location2 = self.geolocator.geocode(route[i]["location"])
                if location1 and location2:
                    distance = geodesic(
                        (location1.latitude, location1.longitude),
                        (location2.latitude, location2.longitude)
                    ).meters
                    # Assume average speed of 60 km/h
                    time_taken = (distance / 1000) / 60 * 3600  # Convert to seconds
                    current_time += time_taken
            
            if current_time >= MAX_DRIVING_TIME:
                checkpoints.append({
                    "location": route[i]["location"],
                    "type": "rest_break",
                    "duration_minutes": 45
                })
                current_time = 0
        
        return checkpoints
    
    def _calculate_fuel_stops(self, route: List[Dict]) -> List[Dict]:
        # Calculate optimal fuel stops based on vehicle range and route distance
        # This is a simplified implementation
        FUEL_RANGE = 500000  # 500 km in meters
        fuel_stops = []
        current_distance = 0
        
        for i in range(len(route)-1):
            distance = self._calculate_distance(
                self.geolocator.geocode(route[i]["location"]).point,
                self.geolocator.geocode(route[i+1]["location"]).point
            )
            current_distance += distance
            
            if current_distance > FUEL_RANGE * 0.8:  # Plan stop at 80% of range
                fuel_stops.append({
                    "location": route[i]["location"],
                    "distance_from_start": current_distance
                })
                current_distance = 0
        
        return fuel_stops
    
    def _add_compliance_checkpoints(self, route: List[Dict]) -> List[Dict]:
        # Add required compliance checkpoints based on regulations
        # This is a simplified implementation
        MAX_DRIVING_TIME = 8 * 3600  # 8 hours in seconds
        checkpoints = []
        current_time = 0
        
        for i in range(len(route)):
            if i > 0:
                current_time += route[i]["arrival_time"] - route[i-1]["arrival_time"]
            
            if current_time >= MAX_DRIVING_TIME:
                checkpoints.append({
                    "location": route[i]["location"],
                    "type": "rest_break",
                    "duration_minutes": 45
                })
                current_time = 0
        
        return checkpoints