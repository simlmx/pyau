import numpy
import time
def resample(x,ratio,quality='sinc_medium',window=None,algo='scikits') :
    """Resamples signal column-wise.
    By default will try to use scikits.samplerate.resample if available.
    Otherwise will use scipy.signal.resample.
    
      ratio: A float value indicating ratio for resampling
    quality: A quality string to be passed to scikits.samplerate.resample. 
             Useful quality values include sinc_medium, sinc_fastest, sinc_best.
             This value is ignored by the scipy algorithm
     window: A window to be passed to scipy.signal.resample. Default is None. 
             This value is ignored by the scikits algorithm.
       algo: The algorithm to be used, either 'scipy' or 'scikits'. Default is 'scikits'
    """
    #decide which function we will use
    func=None
    if algo=='scikits' :
        try :
            import scikits.samplerate
            func=(lambda x,ratio,quality,window: scikits.samplerate.resample(x,ratio,quality))
        except :
            print "Cannot find scikits.samplerate. Resampling using scipy.signal.resample"
            algo='scipy'
    if algo=='scipy' :
        import scipy.signal
        func=(lambda x,ratio,quality,window: scipy.signal.resample(x,int(round(len(x)*ratio)),window=window))
    if func is None:
        raise ValueError("Unknown algo %s. Use either scikits or scipy" % algo)
              
    #call function over columns of array
    if len(x.shape)==1 or x.shape[1]==1 : 
        y = func(x,ratio,quality,window)
    else :
        y=numpy.array([])
        for i in range(x.shape[1]) :
            y=numpy.concatenate((y,func(x[:,i],ratio,quality,window)))
        y=y.reshape(x.shape[1],-1).T
    return y

    



if __name__=='__main__' :
    from pygmy import io
    import sys
    if len(sys.argv)<3 :
        print 'Usage: resample.py <audio file> <ratio of resampling>'
        sys.exit(0)

    fin=sys.argv[1]
    ratio=float(sys.argv[2])

    af = io.AudioFile(fin)
    x,fs,sval=af.read()
    x=x[0:fs*10,:]
    tic=time.time()
    print 'File %s shape=%s fs=%i ratio=%4.4f' % (fin,str(x.shape),fs,ratio)
    v1=resample(x,ratio,algo='scikits')
    print 'scikits',time.time()-tic

    tic=time.time()
    v2=resample(x,ratio,algo='scipy')
    print 'samplerate',time.time()-tic,x.shape,v1.shape,v2.shape
    import pylab
    pylab.subplot(311)
    pylab.plot(x)
    pylab.xlabel('signal')
    pylab.axis([0,len(x),-1,1])
    pylab.subplot(312)
    pylab.plot(v1)
    pylab.xlabel('scikits')
    pylab.axis([0,len(v1),-1,1])
    pylab.subplot(313)
    pylab.plot(v2)
    pylab.xlabel('scipy')
    pylab.axis([0,len(v2),-1,1])
    pylab.show()
