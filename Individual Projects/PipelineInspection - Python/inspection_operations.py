import inspection_models as im

def check_validity(box):
    """
    checks validity of a rectanbular box
    """
    if not isinstance(box, im.RectangleBox):
        raise TypeError

    if box.longitudinal_position < 0 or box.circumferential_position < 0 or box.length <= 0 or box.width <= 0 or box.width > 360:
        raise ValueError


def validate_box(box):
    """
    validates a box and if there is an error prints it.
    """
    try:
        check_validity(box)
    except ValueError:
        print "Value error:"
        print box
        exit()
    except TypeError:
        print "Type error:" + str(box)
        print "Type RectangleBox is expected instead of " + str(type(box))
        exit()


def has_overlap(box1, box2):
    """
    Checks if box1 and box2 has any overlap. box1 and box2 are objects of RectangleBox
    Return: True if there is some overlap; False if there is no overlap
    """

    # validate the values and types of the boxes
    validate_box(box1)
    validate_box(box2)

    # start and end positions of the boxes lengthwise
    box1_length_start = box1.longitudinal_position
    box1_length_end = box1.longitudinal_position + box1.length
    box2_length_start = box2.longitudinal_position
    box2_length_end = box2.longitudinal_position + box2.length

    # invert the opposite case (nonoverlap): if the start of one of the boxes is bigger than or equal to the end of the
    # second or the end of it is smaller than or equal to the start of the second
    # (the symmetric case is intrinsically handled)
    has_lengthwise_overlap = not(box1_length_start >= box2_length_end or box1_length_end <= box2_length_start)

    # if there is no lengthwise overlap no need to calculate the widthwise overlap, so return false
    if not has_lengthwise_overlap:
        return False

    # start and end positions of the boxes widthwise
    box1_width_start = box1.circumferential_position
    box1_width_end = (box1.circumferential_position + box1.width) % 360
    box2_width_start = box2.circumferential_position
    box2_width_end = (box2.circumferential_position + box2.width) % 360

    # 4 cases considered:
    # neither of them pass 360 degrees
    # the second box passes the 360 degree but the first one does not
    # the first box passes the 360 degree but the second one does not
    # both of them pass the 360 degree
    if box1_width_end > box1_width_start:
        # if none of the boxes pass 360 degrees, check the opposite (nonoverlap) case and invert it
        if box2_width_end > box2_width_start:
            has_widthwise_overlap = not(box2_width_start >= box1_width_end or box2_width_end <= box1_width_start)
        # if box2 passes 360 degree but box1 not, check the opposite case and invert it
        else:
            has_widthwise_overlap = not(box2_width_start >= box1_width_end and box2_width_end <= box1_width_start)
    else:
        # if box1 passes 360 degree but box2 not, check the opposite case and invert it
        if box2_width_end > box2_width_start:
            has_widthwise_overlap = not(box1_width_start >= box2_width_end and box1_width_end <= box2_width_start)
        # if both passes 360 there is always an overlap widthwise
        else:
            has_widthwise_overlap = True

    # no need to check has_lengthwise_overlap again(since we returned false if it was false) but for the sake of
    # readability and safety
    if has_lengthwise_overlap and has_widthwise_overlap:
        return True
    else:
        return False

def get_count_overlaps(boxes_list_1, boxes_list_2):
    """
    Counts the number of pairs that overlap such that the first box comes from boxes_list_1 and the second box
    comes from boxes_list_2.
    Return: the number of overlaps; the list of overlapping pairs; the list of non-overlapping pairs
    """

    n_overlap = 0
    overlap_pairs = []
    non_overlap_pairs = []
    for box_data_1 in boxes_list_1:
        box_1 = im.RectangleBox(box_data_1[0], box_data_1[1], box_data_1[2], box_data_1[3])
        for box_data_2 in boxes_list_2:
            box_2 = im.RectangleBox(box_data_2[0], box_data_2[1], box_data_2[2], box_data_2[3])
            if has_overlap(box_1, box_2):
                overlap_pairs.append((box_1, box_2))
                n_overlap += 1
            else:
                non_overlap_pairs.append((box_1, box_2))

    return n_overlap, overlap_pairs, non_overlap_pairs





