from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional
from sys import maxsize


Time = int
Cost = Time
Weight = int
TimeTable = list[list[Time]]
Node = int


@dataclass_json
@dataclass
class TimeWindow:
    start: Time
    end: Time


TimeWindows = dict[Node, TimeWindow]


@dataclass_json
@dataclass
class PickupDelivery:
    pickup: Node
    delivery: Node


@dataclass_json
@dataclass
class Problem:
    tripTimeTable: TimeTable = field(default_factory=lambda: [[0]])
    pickupDeliveries: Optional[list[PickupDelivery]] = None
    numVehicles: int = 1
    depot: int = 0
    startsAtDepot: bool = True
    endsAtDepot: bool = False
    timeWindows: TimeWindows = field(default_factory=dict)
    startTime: Time = 0
    vehicleFixedCost: Cost = 0
    vehicleMaxTime: Time = maxsize
    demands: Optional[list[Weight]] = None
    vehicleCapacities: Optional[list[Weight]] = None


    def properTripTimeTable(self):
        def isZero(i, j):
            return (
                (i == 0 and not self.startsAtDepot)
                or (j == 0 and not self.endsAtDepot)
            )

        return [[
            0 if isZero(i, j) else time
            for j, time in enumerate(row)
        ] for i, row in enumerate(self.tripTimeTable)]


    @staticmethod
    def roundFloatTimeTable(tripTimeTable: list[list[float]]) -> TimeTable:
        return [[round(j) for j in i] for i in tripTimeTable]


    @staticmethod
    def getVehicleFixedCost(tripTimeTable: TimeTable, numVehicles: int) -> Cost:
        return int(0.7 * sum([sum(i) for i in tripTimeTable]) / len(tripTimeTable) / numVehicles)