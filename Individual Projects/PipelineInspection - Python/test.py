import inspection_models as im
import inspection_operations as io

cases_true = []
cases_true.append((im.RectangleBox(15, 10, 2, 40), im.RectangleBox(16, 30, 5, 50))) # some overlap lengthwise and widthwise
cases_true.append((im.RectangleBox(15, 10, 2, 40), im.RectangleBox(16, 49, 5, 50))) # some overlap lengthwise and a 1 degree overlap widthwise
cases_true.append((im.RectangleBox(25, 10, 10, 40), im.RectangleBox(27, 45, 5, 50))) # lengthwise one includes the other, widthwise some overlap
cases_true.append((im.RectangleBox(25, 10, 5, 40), im.RectangleBox(27, 30, 5, 10))) # widthwise one includes the other, lengthwise some overlap
cases_true.append((im.RectangleBox(25, 10, 5, 40), im.RectangleBox(27, 30, 5, 20))) #  widthwise one includes the other and share one border, lengthwise some overlap
cases_true.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 30, 5, 20))) # widthwise one includes the other and one of the boxes passes 360 degrees, lengthwise some overlap
cases_true.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 330, 5, 20))) # widthwise one includes the other and one of the boxes passes 360 degrees, lengthwise some overlap
cases_true.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 330, 5, 40))) # widthwise one includes the other and both of the boxes pass 360 degrees
cases_true.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 350, 5, 80))) # both of the boxes pass 360 degrees, there is overlap lengthwise and widthwise
cases_true.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 350, 5, 80))) # one of them is at the border of 360 and widthwise/lengthwise some overlap
cases_true.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 300, 5, 80))) # one of them is at the border of 360 and contained by the other widthwise
cases_true.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 300, 5, 60))) # one of them is at the border of 360 and contained by the other widthwise and share one border widthwise
cases_true.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 340, 5, 60))) # one of them is at the border of 360 and has some overlap
cases_true.append((im.RectangleBox(25, 0, 5, 40), im.RectangleBox(27, 340, 5, 40))) # one of them is at the border of 0 and has some overlap

print "True cases:"
for pair in cases_true:
    print(io.has_overlap(pair[0], pair[1]))
    print(io.has_overlap(pair[1], pair[0]))

print ""

cases_false = []

cases_false.append((im.RectangleBox(15, 10, 2, 40), im.RectangleBox(18, 30, 5, 50))) # lengthwise no overlap but widthwise overlap
cases_false.append((im.RectangleBox(15, 10, 2, 40), im.RectangleBox(18, 60, 5, 50))) # lengthwise no overlap and widthwise no overlap
cases_false.append((im.RectangleBox(5, 10, 10, 40), im.RectangleBox(15, 320, 5, 100))) # lengthwise no overlap but widthwise overlap and one of the boxes passes 360 degrees
cases_false.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(35, 330, 5, 40))) # lengthwise no overlap but widthwise one includes the other and both of the boxes pass 360 degrees
cases_false.append((im.RectangleBox(25, 10, 5, 40), im.RectangleBox(27, 50, 5, 10))) # lengthwise overlap but widthwise no overlap(contiguous)
cases_false.append((im.RectangleBox(25, 10, 5, 40), im.RectangleBox(27, 60, 5, 20))) # lengthwise overlap but widthwise no overlap
cases_false.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 300, 5, 20))) # lengthwise overlap but widthwise no overlap and one of the boxes pass 360 degrees and they are contiguous widthwise
cases_false.append((im.RectangleBox(25, 320, 5, 100), im.RectangleBox(27, 300, 5, 10))) # lengthwise overlap but widthwise no overlap and one of the boxes pass 360 degrees
cases_false.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 0, 5, 80))) # lengthwise overlap but widthwise no overlap both of the boxes at the border of 360, but on opposite sides
cases_false.append((im.RectangleBox(25, 320, 5, 40), im.RectangleBox(27, 20, 5, 80))) # lengthwise overlap but widthwise no overlap one of the boxes at the border of 360


print "False cases:"
for pair in cases_false:
    print(io.has_overlap(pair[0], pair[1]))
    print(io.has_overlap(pair[1], pair[0]))

