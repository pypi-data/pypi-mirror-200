from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from .problem import *
from sys import maxsize


class RoutingModel:
    def __init__(
        self,
        problem: Problem
    ):
        tripTimeTable = problem.properTripTimeTable()

        self.indexManager = pywrapcp.RoutingIndexManager(
            len(tripTimeTable),
            problem.numVehicles,
            problem.depot,
        )

        self.orToolsModel = pywrapcp.RoutingModel(self.indexManager)

        self.timeCallback = self.__registerTimeCallback(tripTimeTable)
        self.timeDimension = self.__createTimeDimension(problem.vehicleMaxTime)

        self.__setArcCosts()
        self.__setTimeObjective(problem.numVehicles)

        self.__setTimeWindows(problem.timeWindows, self.__getLatenessPenalty(tripTimeTable))
        self.__setStartTime(problem.startTime, problem.depot, problem.timeWindows)

        if problem.pickupDeliveries is not None:
            self.__setPickupsAndDeliveries(problem.pickupDeliveries)

        self.__setVehicleFixedCost(problem.vehicleFixedCost)

        if problem.demands is not None and problem.vehicleCapacities is not None:
            self.demandCallback = self.__registerDemandCallback(problem.demands)
            self.__addCapacityDimension(problem.vehicleCapacities)


    def __setVehicleFixedCost(self, cost):
        self.orToolsModel.SetFixedCostOfAllVehicles(cost)


    def __registerTimeCallback(self, tripTimeTable: TimeTable):
        def time_callback(from_index, to_index):
            from_node = self.indexManager.IndexToNode(from_index)
            to_node = self.indexManager.IndexToNode(to_index)
            return tripTimeTable[from_node][to_node]
        

        return self.orToolsModel.RegisterTransitCallback(time_callback)


    def __setArcCosts(self):
        self.orToolsModel.SetArcCostEvaluatorOfAllVehicles(self.timeCallback)


    def __createTimeDimension(self, vehicleMaxTime: Time):
        time = 'Time'
        self.orToolsModel.AddDimension(
            self.timeCallback,
            0,
            vehicleMaxTime,
            False,
            time)

        return self.orToolsModel.GetDimensionOrDie(time)


    def __setTimeWindows(self, timeWindows: TimeWindows, latenessPenalty: Cost):
        for location_idx, time_window in timeWindows.items():
            index = self.indexManager.NodeToIndex(location_idx)
            self.timeDimension.CumulVar(index).SetMin(time_window.start)
            self.timeDimension.SetCumulVarSoftUpperBound(index, time_window.end, latenessPenalty)


    # This number will be used as a penalty for not arriving on time.
    # It needs to be high enough to never be worthy,
    # but if we use max int size the router wont be able to
    # choose the better one all possible unfeasible routes.
    def __getLatenessPenalty(self, tripTimeTable: TimeTable):
        return int(sum([sum(i) for i in tripTimeTable]) / len(tripTimeTable))


    def __setStartTime(self, startTime: Time, depot: int, timeWindows: TimeWindows):
        index = self.indexManager.NodeToIndex(depot)
        if depot in timeWindows.keys():
            timeWindow = timeWindows[depot]
            startTime = max(startTime, timeWindow.start)
        
        self.timeDimension.CumulVar(index).SetMin(startTime)


    def __setTimeObjective(self, numVehicles: int):
        for i in range(numVehicles):
            self.orToolsModel.AddVariableMinimizedByFinalizer(
                self.timeDimension.CumulVar(self.orToolsModel.End(i)))
            self.orToolsModel.AddVariableMaximizedByFinalizer(
                self.timeDimension.CumulVar(self.orToolsModel.Start(i)))


    def __setPickupsAndDeliveries(self, pickupDeliveries: list[Node]):
        for pickupDelivery in pickupDeliveries:
            pickup_index = self.indexManager.NodeToIndex(pickupDelivery['pickup'])
            delivery_index = self.indexManager.NodeToIndex(pickupDelivery['delivery'])
            self.orToolsModel.AddPickupAndDelivery(pickup_index, delivery_index)

            self.orToolsModel.solver().Add(
                self.orToolsModel.VehicleVar(pickup_index)
                == self.orToolsModel.VehicleVar(delivery_index)
            )

            self.orToolsModel.solver().Add(
                self.timeDimension.CumulVar(pickup_index)
                <= self.timeDimension.CumulVar(delivery_index)
            )


    def __registerDemandCallback(self, demands: list[Weight]):
        def demand_callback(from_index):
            """Returns the demand of the node."""
            # Convert from routing variable Index to demands NodeIndex.
            from_node = self.indexManager.IndexToNode(from_index)
            return demands[from_node]


        return self.orToolsModel.RegisterUnaryTransitCallback(demand_callback)


    def __addCapacityDimension(self, vehicleCapacities: list[Weight]):
        self.orToolsModel.AddDimensionWithVehicleCapacity(
            self.demandCallback,
            0,  # null capacity slack
            vehicleCapacities,
            True,  # start cumul to zero
            'Capacity')
