import cv2
import os
  
class Save_frames:
    def __init__(self,path,f_count):
        self.path=path
        self.f_count=f_count
        self.currentframe=1
    def save(self):
        # Read the video from specified path
        cam = cv2.VideoCapture(self.path)
        time_skips=float(500)
        try:
            # creating a folder named data
            if not os.path.exists('data'):
                os.makedirs('data')
        
        # if not created then raise error
        except OSError:
            print ('Error: Creating directory of data')
        
        # frame
        # currentframe = 1
        # cnt=434
        while(True):
            
            # reading from frame
            ret,frame = cam.read()
        
            if ret:
                # if video is still left continue creating images
                name = './data/image_' + str(self.f_count) + '.jpg'
                print ('Creating...' + name)
        
                # writing the extracted images
                cv2.imwrite(name, frame)
                cam.set(cv2.CAP_PROP_POS_MSEC,(self.currentframe*time_skips))
                # increasing counter so that it will
                # show how many frames are created
                self.currentframe+= 1
                self.f_count+=1
            else:
                break
        
        # Release all space and windows once done
        cam.release()
        cv2.destroyAllWindows()