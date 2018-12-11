add_library('controlP5')
import time

class GUI():
    
    def __init__(self, cp5, cam, callback):
        
        self.cp5 = cp5
        self.cam = cam
        self.callback = callback
        self.index = 0
        self.in  = True
        self.out = False
        self.diff_list = [0.0 for _ in range(32)]
        self.lastTouchedTime = 0.0
        self.diff_listenable = True
        
        self.cp5.addToggle('in') \
            .setValue(self.in) \
            .setPosition(20, height - 40) \
            .setSize(16, 16) \
            .addListener(self.listener)

        self.cp5.addToggle('out') \
            .setValue(self.out) \
            .setPosition(40, height - 40) \
            .setSize(16, 16) \
            .addListener(self.listener)
                
        
        self.cp5.addSlider('index') \
            .setRange(0, 50) \
            .setSize(width - 90, 16) \
            .setPosition(60, height - 40) \
            .setNumberOfTickMarks(51) \
            .addListener(self.listener)
        
        for i in range(32):
            self.cp5.addSlider('diff_%d' % i) \
                .setRange(-0.4, 0.4) \
                .setPosition(width - 145, 20 + i * 20) \
                .addListener(self.listener)        
    
        self.cp5.addButton('reset') \
            .setValue(False) \
            .setPosition(width - 30, 660) \
            .setSize(16, 16) \
            .addListener(self.listener)
    
        self.cp5.setAutoDraw(False)

    def listener(self, event):
        
        self.lastTouchedTime = time.time()
        
        name = str(event.getName())
        
        if name.startswith('diff'):

            ind = int(name[5:])
            self.diff_list[ind] = float(event.getValue())      
      
            if self.diff_listenable:
                self.callback('diff', self.diff_list)

        elif name == 'index':

            self.diff_listenable = False
            for i in range(32):
                controller = self.cp5.getController('diff_%d' % i) 
                controller.setValue(0)
            self.diff_listenable = True

            self.index = int(event.getValue())
            self.callback('index', self.index)

        elif name == 'in':
            
            self.in = bool(event.getValue())

        elif name == 'out':
            
            self.out = bool(event.getValue())

        elif name == 'reset':
            
            self.diff_listenable = False
            for i in range(32):
                controller = self.cp5.getController('diff_%d' % i)
                controller.setValue(0)
            self.diff_listenable = True
            self.callback('diff', self.diff_list)

    def draw(self):
                
        hint(DISABLE_DEPTH_TEST)
        self.cam.beginHUD()
        self.cp5.draw()
        self.cam.endHUD()
        hint(ENABLE_DEPTH_TEST)
        
    def is_operation(self):

        return time.time() - self.lastTouchedTime < 0.3
