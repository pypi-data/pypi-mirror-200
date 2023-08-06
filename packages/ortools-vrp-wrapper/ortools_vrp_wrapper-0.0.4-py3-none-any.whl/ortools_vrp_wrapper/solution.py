import json
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from .problem import Problem, Time
from .routing_model import RoutingModel


Node = int
Index = int
Trip = list[Node]
IndexTrip = list[Index]


class Solution:
    def __init__(self, problem: Problem, routingModel: RoutingModel):
        self.problem = problem
        self.routingModel = routingModel

    def solve(self, searchParameters = pywrapcp.DefaultRoutingSearchParameters()):
        self.solution = self.routingModel.orToolsModel.SolveWithParameters(searchParameters)
        return self


    def getObjective(self):
        return {
            'min': self.solution.ObjectiveMin(),
            'value': self.solution.ObjectiveMin(),
            'max': self.solution.ObjectiveMax(),
        }
    

    def getIndexTripForVehicle(self, vehicleId: int = 0, allIndexes: bool = False):
        orToolsModel = self.routingModel.orToolsModel
        index = orToolsModel.Start(vehicleId)
        indexTrip = []

        while not orToolsModel.IsEnd(index):
            indexTrip.append(index)
            index = self.solution.Value(orToolsModel.NextVar(index))
        
        indexTrip.append(index)

        if allIndexes:
            return indexTrip

        if not self.problem.endsAtDepot:
            del indexTrip[-1]

        if not self.problem.startsAtDepot:
            del indexTrip[0]

        return indexTrip


    def getIndexTrips(self):
        def isEmptyTrip(indexes: list[int]):
            emptyTrip = (
                [self.problem.depot] if self.problem.startsAtDepot else []
                + [self.problem.depot] if self.problem.endsAtDepot else []
            )

            trip = [
                self.routingModel.indexManager.IndexToNode(index)
                for index in indexes
            ]

            return trip == emptyTrip
            
        indexTrips = [
            self.getIndexTripForVehicle(vehicleId)
            for vehicleId in range(self.problem.numVehicles)
        ]

        return {
            vehicleId: trip
            for vehicleId, trip in enumerate(indexTrips)
            if not isEmptyTrip(trip)
        }


    def getTimes(self):
        timeDimension = self.routingModel.orToolsModel.GetDimensionOrDie('Time')
        return {
            vehicleIndex: [
                self.solution.Min(timeDimension.CumulVar(index))
                for index in trip
            ]
            for vehicleIndex, trip in self.getIndexTrips().items()
        }
    

    def getTotalTime(self, vehicleId = 0):
        times = self.getTimes()[vehicleId]
        return times[-1] - times[0]
    

    def getTrips(self) -> dict[int, Trip]:
        return {
            vehicleIndex: [
                self.routingModel.indexManager.IndexToNode(index)
                for index in trip
            ]
            for vehicleIndex, trip in self.getIndexTrips().items()
        }


    def getSortedTrips(self) -> list[Trip]:
        return sorted(list(self.getTrips().values()))


    # Funcionando só para 1 veículo
    def calculateLateness(self, vehicleId = 0):
        def calculateOneLateness(node, time):
            if not node in self.problem.timeWindows:
                return 0

            maxTime = self.problem.timeWindows[node].end
            return max(0, time - maxTime)

        times = self.getTimes()[vehicleId]
        nodes = self.getTrips()[vehicleId]

        return [
            calculateOneLateness(node, time)
            for node, time in zip(nodes, times)
        ]

        return latenesses
    

    def getTotalLateness(self, vehicleId = 0):
        lateness = self.calculateLateness(vehicleId)
        return sum(lateness)
