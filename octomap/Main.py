from OctoMap import OctoMap
from RandomSearch import RandomSearch


def main():
    octomap = OctoMap()
    octomap.start()
    # point_list = RandomSearch().plan(octomap.get_octotree())

if __name__=="__main__":
    main()