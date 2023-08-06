from ortools_vrp_wrapper.problem import Problem
from ortools_vrp_wrapper.routing_model import RoutingModel
from ortools_vrp_wrapper.solution import Solution
from tests.trip_time_tables import *
import unittest
 

class TestModel(unittest.TestCase):
    def test_basic_problem(self):
        problem = Problem(aTableWithStraightSolution())
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        self.assertListEqual([[0, 1, 2]], list(solution.getTrips().values()))
        self.assertListEqual([[0, 3, 7]], list(solution.getTimes().values()))


    def test_basic_problem_with_pickup_and_delivery(self):
        problem = Problem(
            aTableWithStraightSolution(),
            [{'pickup': 2, 'delivery': 1}]
        )
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        self.assertListEqual([[0, 2, 1]], list(solution.getTrips().values()))


    def test_rather_large_problem(self):
        problem = Problem(aRatherLargeTripTimeTable())
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        self.assertListEqual([[0, 3, 1, 10, 6, 8, 7, 9, 11, 5, 4, 2]], list(solution.getTrips().values()))


    def test_rather_large_problem_with_multiple_vehicles(self):
        problem = Problem(aRatherLargeTripTimeTable(), numVehicles=10)
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        trips = sorted(list(solution.getTrips().values()))
        self.assertListEqual([[0, 1, 3], [0, 10, 6, 8, 7, 9, 11, 5, 4, 2]], trips)


    # Same test as before, but one vehicle stays unused because of fixed costs
    def test_vehicle_with_fixed_costs(self):
        problem = Problem(aRatherLargeTripTimeTable(), numVehicles=10, vehicleFixedCost=1000)
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        trips = sorted(list(solution.getTrips().values()))
        self.assertListEqual([[0, 3, 1, 10, 6, 8, 7, 9, 11, 5, 4, 2]], trips)


    def test_vehicle_max_time(self):
        problem = Problem(aRatherLargeTripTimeTable(), numVehicles=10, vehicleMaxTime=5000)
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        trips = sorted(list(solution.getTrips().values()))
        self.assertListEqual([[0, 1, 3], [0, 2, 4, 5], [0, 10, 6, 8, 7, 9, 11]], trips)


    def test_demands(self):
        tripTimeTable = aRatherLargeTripTimeTable()
        demands = [0] + [1] * (len(tripTimeTable) - 1)
        problem = Problem(tripTimeTable, numVehicles=10, demands=demands, vehicleCapacities=[3] * 10)
        routingModel = RoutingModel(problem)
        solution = Solution(problem, routingModel).solve()
        trips = solution.getSortedTrips()
        self.assertListEqual([[0, 1, 3], [0, 2, 4, 5], [0, 9, 7, 11], [0, 10, 6, 8]], trips)