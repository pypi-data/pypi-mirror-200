#In the name of GOD
#please put your code under here

import wx

def size():
    return (-1,-1)

def main (panel=None):
    #print 'out'
    q = wx.GetActiveWindow()
    p = wx.GetApp()
    
    if str(q) == 'None':
        p.Exit()

    else:
        #print q.m_mgr
        if 'timer' in dir(q):
            q.timer.Stop()
        q.m_mgr.UnInit()
        q.Destroy()

    
if __name__ == '__main__':
    main (None)
