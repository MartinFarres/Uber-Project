import unittest
from algorithm import dijkstra, find_nearest_cars
from uber_map import Map, load_grid_map
from direction import Direction
from dynamic_location import DynamicLoc
from min_heap import Heap


class DijkstraTest(unittest.TestCase):


    def test_shortest_path_simple(self):
        map1 = Map(["s", "t", "y", "z", "x"], [])
        # Connected map
        map1.insert_directed("s", "t", 10)
        map1.insert_directed("s", "y", 5)
        map1.insert_directed("t", "y", 2)
        map1.insert_directed("t", "x", 1)
        map1.insert_directed("y", "t", 3)
        map1.insert_directed("y", "z", 2)
        map1.insert_directed("y", "x", 9)
        map1.insert_directed("z", "s", 7)
        map1.insert_directed("z", "x", 6)
        map1.insert_directed("x", "z", 4)
        dijkstra_results1 = dijkstra(map1, "s", "x")
        self.assertEqual(["x", "t", "y", "s"], dijkstra_results1.path)
        self.assertEqual(9, dijkstra_results1.weight)
        
    def test_disconnected_component(self):
        map1 = Map(["s", "t", "y", "m", "n"], [])

        # Connected component
        map1.insert_directed("s", "t", 10)
        map1.insert_directed("s", "y", 5)

        # Disconnected component
        map1.insert_directed("m", "n", 3)

        dijkstra_results1 = dijkstra(map1,"s", "m")
        self.assertEqual(None, dijkstra_results1)

    def test_shortest_same_weight(self):

        # Straight line path
        map1 = load_grid_map(10)
        
        dijkstra_results1 = dijkstra(
            map1,
            10,
            19
        )

        self.assertEqual(dijkstra_results1.path, list(reversed(range(10, 20))))
        self.assertEqual(dijkstra_results1.weight, 9)

    def test_shortest(self):

        # Straight line path
        map1 = load_grid_map(10)

        for (u, v) in map1.street_generator():
            map1.update_street(u, v, 20)

        # Sets a short path
        map1.update_street(0, 10, 1)
        map1.update_street(10, 11, 1)
        map1.update_street(11, 12, 1)
        map1.update_street(12, 22, 1)
        map1.update_street(22, 23, 1)
        map1.update_street(23, 24, 1)
        map1.update_street(24, 14, 1)
        map1.update_street(14, 4, 1)
        map1.update_street(4, 5, 1)
        map1.update_street(5, 6, 1)
        map1.update_street(6, 7, 1)
        map1.update_street(7, 8, 1)
        map1.update_street(8, 9, 1)
        map1.update_street(9, 19, 1)
        map1.update_street(19, 29, 1)
        map1.update_street(29, 28, 1)
        map1.update_street(28, 27, 1)
        map1.update_street(27, 26, 1)
        
        dijkstra_results1 = dijkstra(map1, 0, 26)
        self.assertEqual(dijkstra_results1.weight, 18)
        self.assertEqual(dijkstra_results1.path, [26, 27, 28, 29, 19, 9, 8, 7, 6, 5, 4, 14, 24, 23, 22, 12, 11, 10, 0])

    def test_find_func(self):
        """
        If there is a bidirected street, the algorithm moves the
        path as if the car could turn in the corner
        
        """
        map1 = load_grid_map(3)

        # The car1 is in the street (0, 3), NOT in (3, 0)
        # this means it's going downwards

        # The car2 is in the street (5, 8), going downwards

        cars = [
            DynamicLoc("C1", Direction(0, 0.3, 3, 0.7), 1.0),
            DynamicLoc("C2", Direction(5, 0.7, 8, 0.3), 1.0)
        ]

        p1 = DynamicLoc("P1", Direction(4, 0.4, 5, 0.6), 100)

        # Stores the cars and it's weight
        heap = Heap(len(cars))

        for car in cars:
            
            start_node = car.direction.edge2
            end_node = p1.direction.edge1

            start_distance = car.direction.d2 + p1.direction.d1

            result = dijkstra(map1, start_node, end_node)

            total_distance = start_distance + result.weight

            heap.add(car.name, total_distance)

    def test_find_nearst_cars(self):
        map1 = load_grid_map(3)

        cars = {
            "C1" : DynamicLoc("C1", Direction(0, 0.3, 3, 0.7), 1.0),
            "C2" : DynamicLoc("C2", Direction(5, 0.7, 8, 0.3), 1.0)
        }

        p1 = DynamicLoc("P1", Direction(4, 0.4, 5, 0.6), 100)
        result = find_nearest_cars(map1, cars, p1, 2)

        self.assertEqual(result[0].car_name, "C1")
        self.assertEqual(result[1].car_name, "C2")

        self.assertEqual(result[0].path, [4, 3])
        self.assertEqual(result[1].path, [4, 7, 8])

        self.assertEqual(result[0].price, 2.1)
        self.assertEqual(result[1].price, 2.7)

    def test_find_nearst_cars(self):
        map1 = load_grid_map(5)

        cars = {
            "C1" : DynamicLoc("C1", Direction(0, 0.3, 5, 0.7), 1.0),
            "C2" : DynamicLoc("C2", Direction(2, 0.1, 3, 0.9), 1.0),
            "C3" : DynamicLoc("C3", Direction(17, 0.4, 12, 0.6), 1.0)
        }

        p1 = DynamicLoc("P1", Direction(13, 0.6, 14, 0.4), 100)

        def price_func(car, distance):
            return distance

        result = find_nearest_cars(map1, cars, p1, 3, price_func)

        #for car_data in result:
        #    print(car_data.car_name, car_data.path, car_data.price)

        self.assertEqual(result[0].car_name, "C3")
        self.assertEqual(result[1].car_name, "C2")
        self.assertEqual(result[2].car_name, "C1")


        self.assertEqual(result[0].path, [13, 12])
        self.assertEqual(result[0].price, 2.2)
        
        self.assertEqual(result[1].path, [13, 8, 3])
        self.assertEqual(result[1].price, 3.5)

        self.assertEqual(result[2].path, [13, 8, 7, 6, 5])
        self.assertEqual(result[2].price, 5.3)

    def test_find_nearst_cars_edge_case(self):
        """
        TODO In this case, the car makes a 180 degree flip at the end of the street
        is this valid?
        """
        map1 = load_grid_map(5)
        cars = {
            "C3" : DynamicLoc("C3", Direction(17, 0.4, 12, 0.6), 1.0)
        }

        p2 = DynamicLoc("P2", Direction(23, 0.7, 22, 0.3), 100)

        def price_func(car, distance):
            return distance

        result = find_nearest_cars(map1, cars, p2, 3, price_func)

        for car_data in result:
            print(car_data.car_name, car_data.path, car_data.price)

if __name__ == "__main__":
    unittest.main()
