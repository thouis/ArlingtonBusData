import numpy as np

# adapted from https://stackoverflow.com/questions/27161533/find-the-shortest-distance-between-a-point-and-line-segments-not-line

# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'pnt' the proc returns the shortest 
# distance from pnt to the line and the coordinates of the 
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line.
# Malcolm Kesson 16 Dec 2012


def pnt2line(pnts, start, end):
    assert pnts.shape[1] == 2
    start = start.reshape((1, 2))
    end = end.reshape((1, 2))
    line_vec = end - start
    pnt_vec = pnts - start
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    pnt_vec_scaled = pnt_vec / line_len
    ts = np.clip(line_unitvec.dot(pnt_vec_scaled.T), 0, 1)
    nearest = ts.T.dot(line_vec)
    dists = np.linalg.norm(nearest - pnt_vec, axis=1)
    nearest = start.reshape((1, 2)) + nearest
    return (dists, nearest)
