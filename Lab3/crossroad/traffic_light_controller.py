from Lab3.crossroad.enums import TrafficLightControllerState, CellDirection, LightSignal, CrossroadLightState
from Lab3.crossroad.cell import TrafficLight, RoadZone, ZoneContainer
from Lab3.crossroad.data import TrafficLightDataPoint, GlobalData


class TrafficLightController():
    def __init__(self, state, tlights, zones):
        self.state = state
        self.tlights = TrafficLightContainer(tlights)
        self.zones = zones
        self.traffic_lights_manager = self.init_tf_manager(state = self.state, tlights=self.tlights, zones=self.zones)
           
    @staticmethod
    def init_tf_manager(tlights, zones, state = TrafficLightControllerState.TURNED_OFF):
        match state:
            case TrafficLightControllerState.SIMPLE:
                return SimpleManager(tlights, zones)
            case TrafficLightControllerState.ADAPTIVE:
                return AdaptiveManager(tlights, zones)
            case _:
                return TurnedOffManager(tlights, zones)
            
    def update(self):
        self.traffic_lights_manager.update()
        GlobalData.traffic_light_data.append(TrafficLightDataPoint(self.traffic_lights_manager.total_load, self.traffic_lights_manager.ns_fullness, self.traffic_lights_manager.ew_fullness, self.traffic_lights_manager.current_delay, self.traffic_lights_manager.current_state))


class TrafficLightContainer():
    def __init__(self, tlights):
        self._NS_group = []
        self._EW_group = []
        self.set_groups(tlights)

    def set_groups(self, objects):
        for obj in objects:
            if isinstance(obj, TrafficLight):
                if obj.direction in (CellDirection.NORTH, CellDirection.SOUTH):
                    self._NS_group.append(obj)
                elif obj.direction in (CellDirection.EAST, CellDirection.WEST):
                    self._EW_group.append(obj)
                else:
                    print(f"Error. Incorect direction. Object = {obj}, direction = {obj.direction}")
            else:
                print(f"Error. Incorect cell type. Cell = {obj}")
                
    def set_light_state(self, state):
        match state:
            case CrossroadLightState.TURN_OFF_ALL:
                for item in self._NS_group + self._EW_group:
                    item.light_signal = LightSignal.TURNED_OFF
            case CrossroadLightState.WAITING:
                for item in self._NS_group + self._EW_group:
                    item.light_signal = LightSignal.YELLOW
            case CrossroadLightState.ALLOW_ALL:
                for item in self._NS_group + self._EW_group:
                    item.light_signal = LightSignal.GREEN
            case CrossroadLightState.BUN_ALL:
                for item in self._NS_group + self._EW_group:
                    item.light_signal = LightSignal.RED
            case CrossroadLightState.ALLOW_NS:
                for item in self._NS_group:
                    item.light_signal = LightSignal.GREEN
                for item in self._EW_group:
                    item.light_signal = LightSignal.RED
            case CrossroadLightState.ALLOW_EW:
                for item in self._EW_group:
                    item.light_signal = LightSignal.GREEN
                for item in self._NS_group:
                    item.light_signal = LightSignal.RED
            case _:
                print(f"Wrong state: {state}")


class TrafficLightManager:
    def __init__(self, traffic_lights, zones):
        self.traffic_lights = traffic_lights
        self.zones = zones
        self.total_load = 0
        self.ns_fullness = 0
        self.ew_fullness = 0
        self.current_state = CrossroadLightState.TURN_OFF_ALL
        self.base_delay = 40
        self.current_delay = self.base_delay
        
    def calc_load(self):
        self.ns_fullness = self.zones.ns_zone.get_fullness_ratio()
        self.ew_fullness = self.zones.ew_zone.get_fullness_ratio()
        self.total_load = (self.ns_fullness + self.ew_fullness) / 2

    def update(self):
        raise NotImplementedError


class SimpleManager(TrafficLightManager):
    def __init__(self, traffic_lights, zones):
        super().__init__(traffic_lights, zones)
        self.waiting = 10
        self.current_tick = 0
        self.cycle_time = self.base_delay * 2 + self.waiting * 2

    def update(self):
        self.calc_load()
        
        cycle_position = self.current_tick % self.cycle_time
        if cycle_position == 0:
            self.current_state = CrossroadLightState.ALLOW_NS        
            self.traffic_lights.set_light_state(self.current_state)
        elif cycle_position == self.base_delay:
            self.current_state = CrossroadLightState.WAITING        
            self.traffic_lights.set_light_state(self.current_state)
        elif cycle_position == self.cycle_time / 2:
            self.current_state = CrossroadLightState.ALLOW_EW        
            self.traffic_lights.set_light_state(self.current_state)
        elif cycle_position == self.base_delay * 2 + self.waiting:
            self.current_state = CrossroadLightState.WAITING        
            self.traffic_lights.set_light_state(self.current_state)

        self.current_tick += 1
  

class AdaptiveManager(TrafficLightManager):
    def __init__(self, traffic_lights, zones):
        super().__init__(traffic_lights, zones)
        self.current_tick = 0
        self.current_state = CrossroadLightState.ALLOW_NS
        self.next_state = None
        self.calc_state = None
        self.zone_switch_count = 0
        self.max_switch_count = 3

    def update(self):
        self.calc_load()

        if self.current_state in (CrossroadLightState.ALLOW_NS, CrossroadLightState.ALLOW_EW):
            if self.current_state == CrossroadLightState.ALLOW_NS:
                if self.ns_fullness > self.ew_fullness:
                    self.zone_switch_count += 1
                else:
                    self.zone_switch_count = 0
                    self.next_state = CrossroadLightState.ALLOW_EW
            elif self.current_state == CrossroadLightState.ALLOW_EW:
                if self.ew_fullness > self.ns_fullness:
                    self.zone_switch_count += 1
                else:
                    self.zone_switch_count = 0
                    self.next_state = CrossroadLightState.ALLOW_NS

            if self.zone_switch_count > self.max_switch_count:
                self.next_state = CrossroadLightState.ALLOW_NS if self.current_state == CrossroadLightState.ALLOW_EW else CrossroadLightState.ALLOW_EW
                self.zone_switch_count = 0
                
        if self.current_state == CrossroadLightState.WAITING:
            if self.zones.crossroad_zone.is_empty():
                self.current_state = self.next_state
                self.traffic_lights.set_light_state(self.current_state)

        self.current_delay = self.base_delay - int(20 * self.total_load)
        self.current_tick += 1
        if self.current_tick >= self.current_delay:
            if self.next_state != self.current_state:
                if self.zones.crossroad_zone.is_empty():
                    self.current_state = self.next_state
                    self.traffic_lights.set_light_state(self.current_state)
                    self.current_tick = 0
                else:
                    self.current_state = CrossroadLightState.WAITING
                    self.traffic_lights.set_light_state(self.current_state)
        

class TurnedOffManager(TrafficLightManager):
    def update(self):
        self.traffic_lights.set_light_state(self.current_state)