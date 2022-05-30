import os
from multiprocessing import Process
from queue import Queue

from OctoMap import OctoMap


def info(title):
    print(title)
    print('Module name:', __name__)
    print('Parent process:', os.getppid())
    print('Process id:', os.getpid())

def task_octomap():
    info("task_octomap")
    octomap = OctoMap()
    octomap.start()

def task_interaction():
    info("task_interaction")
    pass

def main():
    # queue = Queue()
    # p_octomap = Process(target=task_octomap, args=queue)
    # p_interaction = Process(target=task_interaction, args=queue)

    # p_octomap.start()
    # # p_interaction.start()
    # p_octomap.join()
    # # p_interaction.join()
    octomap = OctoMap()
    octomap.start()

if __name__=="__main__":
    main()