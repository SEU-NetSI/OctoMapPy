
from OctoTree import OctoTree
from Config import TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH
from Inputter import Inputter


def display_tree():
    # test_point_list = [(110,110,110),(30,30,30),(110,110,110),(30,30,30),(110,110,110),(30,30,30),(110,110,110),(30,30,30),(110,110,110),(30,30,30),(110,110,110),(30,30,30)]
    # test_point_list = [(-10,-20,-30),(-10,-20,-30),(-10,-20,-30),(-10,-20,-30),(-10,-20,-30)]
    
    # test_point_list = [(30, 30, 30), (30, 30, 30), (30, 30, 30), (30, 30, 30), (30, 30, 30),(-10,-20,-30),(-10,-20,-30),(-10,-20,-30),(-10,-20,-30),(-10,-20,-30)]
    # myTree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
    # for test_point in test_point_list:
    #     myTree.ray_casting(TREE_CENTER, test_point)
    # myTree.visualize()

    start_point_list = [(-2, 0, -1), (-2, 0, -1), (-2, 0, -1), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, -1, 0), (-1, -1, 0), (-1, -2, 0), (-1, -2, 0), (-1, -2, 0), (-1, -3, 0), (0, -3, 0), (0, -3, 0), (0, -3, 0), (0, -3, 0), (0, -4, 0), (0, -4, 0), (-1, -4, 0), (-1, -4, 0), (-1, -4, 0), (-1, -4, 0), (-1, -4, 0), (-1, -4, 0), (-1, -5, 0), (-1, -5, 0), (-1, -5, 0), (-1, -5, -1), (-1, -5, -1), (-2, -5, -1), (-2, -5, -1), (-2, -6, -1), (-2, -6, -1), (-2, -6, -1), (-2, -6, -1), (-2, -6, -1), (-2, -7, -1), (-2, -7, -1), (-2, -7, -1), (-2, -8, -1), (-2, -8, -1), (-1, -8, -1), (-1, -9, -1), (-1, -9, 0), (-1, -10, 0), (-1, -10, 0), (0, -11, 0), (0, -11, 0), (0, -12, 0), (0, -12, 0), (0, -12, 0), (0, -13, 0), (0, -13, 0), (0, -13, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -16, 0), (0, -16, 0), (0, -16, 0), (0, -16, 0), (0, -16, 0), (0, -16, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -15, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -15, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0), (0, -14, 0)]
    end_point_list = [(37.7, 0.5, -0.9), (37.5, 0.6, -0.9), (37.5, 0.5, -0.9), (39.2, 0.4, 0.1), (38.3, 0.6, 0.1), (37.9, 0.6, 0.1), (38.0, -0.4, 0.1), (38.6, -0.4, 0.1), (38.6, -1.4, 0.1), (38.5, -1.4, 0.1), (38.7, -1.4, 0.1), (38.3, -2.4, 0.1), (39.5, -2.3, 0.1), (39.6, -2.2, 0.1), (39.5, -2.3, 0.1), (39.7, -2.3, 0.1), (39.6, -3.2, 0.1), (39.2, -3.3, 0.1), (38.2, -3.2, 0.1), (37.7, -3.1, 0.1), (38.3, -3.1, 0.1), (38.4, -2.9, 0.1), (38.0, -2.9, 0.1), (38.0, -2.8, 0.1), (37.8, -3.8, 0.1), (37.9, -3.8, 0.1), (38.2, -3.8, 0.1), (37.6, -3.8, -0.9), (38.3, -3.8, -0.9), (37.0, -3.8, -0.9), (37.4, -3.8, -0.9), (37.2, -4.8, -0.9), (37.1, -4.8, -0.9), (37.2, -4.8, -0.9), (37.4, -4.8, -0.9), (37.3, -4.8, -0.9), (37.7, -5.8, -0.9), (37.5, -6.0, -0.9), (37.0, -6.0, -0.9), (37.8, -7.1, -0.9), (36.9, -7.0, -0.9), (37.7, -6.9, -0.9), (38.4, -7.9, -0.9), (38.5, -8.0, 0.1), (37.6, -8.9, 0.1), (38.0, -8.9, 0.1), (38.2, -10.0, 0.1), (39.1, -9.9, 0.1), (38.2, -11.0, 0.1), (37.7, -11.0, 0.1), (37.3, -11.1, 0.1), (36.0, -12.1, 0.1), (35.2, -12.2, 0.1), (34.5, -12.2, 0.1), (33.3, -13.2, 0.1), (33.3, -13.2, 0.1), (32.1, -13.3, 0.1), (31.7, -13.3, 0.1), (31.3, -14.3, 0.1), (30.7, -14.3, 0.1), (30.4, -14.3, 0.1), (30.2, -14.4, 0.1), (29.6, -14.5, 0.1), (29.6, -14.5, 0.1), (29.7, -15.5, 0.0), (30.0, -15.5, 0.0), (30.0, -15.5, 0.0), (29.1, -15.5, 0.0), (29.7, -15.5, 0.0), (30.0, -15.6, 0.0), (29.7, -14.6, 0.0), (30.2, -14.6, 0.0), (30.0, -14.4, 0.0), (30.5, -14.5, 0.0), (30.8, -14.7, 0.0), (30.7, -13.6, 0.0), (31.3, -13.5, 0.1), (31.8, -13.6, 0.0), (31.4, -13.6, -0.0), (31.2, -13.6, -0.7), (31.4, -13.6, -0.1), (30.9, -13.6, -0.5), (31.4, -13.6, -0.2), (31.7, -13.6, -0.3), (31.6, -13.6, -0.3), (31.0, -13.6, -0.2), (30.9, -13.6, -0.3), (30.9, -13.6, -0.3), (31.5, -13.6, -0.2), (31.8, -13.6, -0.2), (31.4, -13.6, -0.3), (31.3, -13.6, -0.2), (31.7, -13.6, -0.2), (31.4, -14.7, -0.2), (31.5, -13.7, -0.2), (31.4, -13.7, -0.2), (31.9, -13.7, -0.2), (31.6, -13.7, -0.2), (31.2, -13.7, -0.2), (31.1, -13.7, -0.2)]
    # start_point_list = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
    # end_point_list = [(50,10,10),(50,10,10),(50,10,10),(50,10,10),(50,10,10)]
    myTree = OctoTree(TREE_CENTER, TREE_RESOLUTION, TREE_MAX_DEPTH)
    for index in range(len(end_point_list)):
        myTree.ray_casting(start_point_list[index], end_point_list[index])
    myTree.visualize()    
    

def test_log():
    display_tree()
    # input = Inputter()

if __name__=="__main__":
    test_log()