import cv2 as cv

def rescaleFrame(frame, scale = 0.75):
    # for Images, Videos and Live Videos
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dimensions = (width,height)
    return cv.resize(frame, dimensions, interpolation = cv.INTER_AREA)

def changeRes(feed,width,height):
    #live video only
    feed.set(3,width)
    feed.set(4,height)