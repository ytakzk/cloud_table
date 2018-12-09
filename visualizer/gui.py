add_library('controlP5')
import time

class GUI():
    
    def __init__(self, cp5, cam, callback):
        
        self.cp5 = cp5
        self.cam = cam
        self.callback = callback
        self.index = 0
        self.manipulation = False
        self.diff_list = [0.0 for _ in range(32)]
        self.lastTouchedTime = 0.0
        
        self.cp5.addToggle('manipulation') \
            .setValue(False) \
            .setPosition(20, height - 40) \
            .setSize(16, 16) \
            .addListener(self.listener)
        
        self.cp5.addSlider('index') \
            .setRange(0, 8000) \
            .setSize(width - 120, 16) \
            .setPosition(80, height - 40) \
            .setNumberOfTickMarks(8001) \
            .addListener(self.listener)
        
        for i in range(32):
            self.cp5.addSlider('diff_%d' % i) \
                .setRange(-1.0, 1.0) \
                .setPosition(width - 145, 20 + i * 20) \
                .addListener(self.listener)        
    
        self.cp5.addButton('reset') \
            .setValue(False) \
            .setPosition(width - 145, height - 60) \
            .setSize(16, 16) \
            .addListener(self.listener)
    
        self.cp5.setAutoDraw(False)

    def listener(self, event):
        
        self.lastTouchedTime = time.time()
        
        name = str(event.getName())
        
        if name.startswith('diff'):
            # print name
            ind = int(name[5:])
            self.diff_list[ind] = float(event.getValue())            
            self.callback('diff', self.diff_list)

        elif name == 'index':
            
            self.index = int(event.getValue())
            self.callback('index', self.index)

        elif name == 'manipulation':
            
            self.manipulation = bool(event.getValue())
            self.callback('manipulation', self.manipulation)

        elif name == 'reset':
            
            for i in range(32):
                controller = self.cp5.getController('diff_%d' % i) 
                controller.setValue(0)

    def draw(self):
                
        hint(DISABLE_DEPTH_TEST)
        self.cam.beginHUD()
        self.cp5.draw()
        self.cam.endHUD()
        hint(ENABLE_DEPTH_TEST)
        
    def is_operation(self):

        return time.time() - self.lastTouchedTime < 0.3
