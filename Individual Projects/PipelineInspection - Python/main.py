import inspection_operations as io
import pandas as pd

# lists of rectangle boxes to be compared for overlaps
df_boxes_1 = pd.read_csv("data/list_boxes_1.csv")
df_boxes_2 = pd.read_csv("data/list_boxes_2.csv")

boxes_data_1 = df_boxes_1.values
boxes_data_2 = df_boxes_2.values

# number of total comparisons (or pairs or rectangular boxes)
n_comparisons = len(boxes_data_1) * len(boxes_data_2)

n_overlap, _, _ = io.get_count_overlaps(boxes_data_1, boxes_data_2)

print ("Total Overlap: " + str(n_overlap) + " out of " + str(n_comparisons))