

class ClockGenerator(object):
    def __init__(self, subsystems):
        self.timer_count = 0
        self.subsystems = subsystems

    def remove_component(self, subsystem, components):
        return

    def tick_to_components(self):
        for subsys in self.subsystems.system_name:
            for comp in self.subsystems.components[subsys].components_list:
                if comp is not None:
                    comp.tick(self.timer_count)
        self.timer_count += 1
