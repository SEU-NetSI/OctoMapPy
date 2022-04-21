import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig

from Config import URI, LOGGER, TREE_CENTER, TREE_MAX_DEPTH, TREE_RESOLUTION, WHETHER_FLY
from OctoTree import OctoTree
from Util import rotate_and_create_points


class OctoMap:
    def __init__(self):
        self.octotree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
        self.counter = 0

    def mapping(self):
        cflib.crtp.init_drivers()
        self.cf = Crazyflie(ro_cache=None, rw_cache='cache')

        # Connect callbacks from the Crazyflie API
        try:
            self.cf.connected.add_callback(self.connected)
        except:
            LOGGER.info("Connect failed.")
        self.cf.disconnected.add_callback(self.disconnected)

        # Connect to the Crazyflie
        self.cf.open_link(URI)
    
    def connected(self, URI):
        LOGGER.info('We are now connected to {}'.format(URI))

        # Add log configuration
        try:
            lmap = self.get_log_config()
            self.cf.log.add_config(lmap)
            lmap.data_received_cb.add_callback(self.update_map)
            lmap.start()
        except KeyError as e:
            LOGGER.error('Could not start log configuration,''{} not found in TOC'.format(str(e)))
        except AttributeError:
            LOGGER.error('Could not add Measurement log config, bad configuration.')

    def disconnected(self, URI):
        LOGGER.info('Disconnected')

    def get_octotree(self):
        return self.octotree

    def update_map(self, timestamp, data, logconf):
        measurement, start_point = self.parse_log_data(data)
        end_points = self.get_end_point(start_point, measurement)
        for end_point in end_points:
            self.octotree.ray_casting(tuple(start_point), tuple(end_point))

        # export nodes each 100 times ranging
        self.counter += 1
        # TODO: new a thread to export
        if self.counter % 100 == 0:
            self.octotree.export_known_node()
    
    def get_log_config(self):
        lmap = LogConfig(name='Mapping', period_in_ms=100)
        
        lmap.add_variable('stateEstimateZ.x')
        lmap.add_variable('stateEstimateZ.y')
        lmap.add_variable('stateEstimateZ.z')
        
        lmap.add_variable('range.front')

        lmap.add_variable('stabilizer.roll')
        lmap.add_variable('stabilizer.pitch')
        lmap.add_variable('stabilizer.yaw')

        return lmap
    
    def parse_log_data(data):
        measurement = {
            # cm
            'x': data['stateEstimateZ.x'] / 10,
            'y': data['stateEstimateZ.y'] / 10,
            'z': data['stateEstimateZ.z'] / 10,
            # ±90, ±90, ±180
            'roll': round(data['stabilizer.roll'], 2),
            'pitch': round(data['stabilizer.pitch'], 2),
            'yaw': round(data['stabilizer.yaw'], 2),
            # cm
            'front': data['range.front'] / 10,
        }
        start_point = [
            int(measurement['x']),
            int(measurement['y']),
            int(measurement['z'])
        ]
        return measurement, start_point
                     
    def get_end_point(self, start_point: list, measurement: dict):
        end_points = rotate_and_create_points(measurement, start_point)
        return end_points
    
