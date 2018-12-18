
def setup():
    
    global pts, binary_list
    
    size(600, 600)
    
    unit_length = 150
    
    binary_list = [False for _ in range(7)]
    
    pts = [
         PVector(-unit_length, -unit_length),
         PVector(-unit_length, 0),
         PVector(-unit_length, unit_length),
         PVector(0, unit_length),
         PVector(unit_length, unit_length),
         PVector(unit_length, 0),
         PVector(unit_length, -unit_length),
         PVector(0, -unit_length)
         ]

def draw():
    
    background(0)
    
    translate(width * 0.5, height * 0.5)
    
    stroke(160)
    
    for pt1, pt2 in zip(pts[::2], pts[2::2] + [pts[0]]):
        line(pt1.x, pt1.y, pt2.x, pt2.y)
    
    line(pts[0].x, pts[0].y, pts[2].x, pts[2].y)
    line(pts[0].x, pts[0].y, pts[2].x, pts[2].y)
    
    line(pts[1].x, pts[1].y, pts[7].x, pts[7].y)
    
    pt17 = (pts[1] + pts[7]) * 0.5
    pt57 = (pts[5] + pts[7]) * 0.5
    line(pt17.x, pt17.y, pt57.x, pt57.y)

    line(pts[1].x, pts[1].y, pts[7].x, pts[7].y)

    for i, pt in enumerate(pts[1:]):
        
        if binary_list[i] == True:
            stroke(0, 100, 250)
        else:
            stroke(160)

        line(0, 0, pt.x, pt.y)
        
    bin = ''
    for i in reversed(binary_list):
        bin += '1' if i == True else '0'
        
    decimal_value = int(bin, 2)
    fill(160)
    textSize(16)
    text(decimal_value, -width * 0.5 + 10, height * 0.5 - 15)


def mousePressed():

    active_index  = None
    smallest_dist = 9999
    
    for i, pt in enumerate(pts[1:]):

        d = dist(mouseX - width * 0.5, mouseY - height * 0.5, pt.x * 0.5, pt.y * 0.5)

        if d < smallest_dist:
            smallest_dist = d
            active_index  = i
        
    binary_list[active_index] = False if binary_list[active_index] else True
