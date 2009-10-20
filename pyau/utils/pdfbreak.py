#! /usr/bin/env python
from pyPdf import PdfFileWriter
from pyPdf import PdfFileReader
import sys
import copy

def pdfbreak(infile,outfile,rowcount=2,colcount=1,marginPx=0):    
    
    input1 = PdfFileReader(file(infile, "rb"))
    pgcnt=input1.getNumPages()
    print 'Opening',infile,'with',pgcnt,'pages'


        
    output = PdfFileWriter()
    for p in range(pgcnt) :
        srcPg = input1.getPage(p)

        srcHeight=srcPg.mediaBox.getUpperRight_y()
        srcWidth=srcPg.mediaBox.getUpperRight_x()
        height=float(srcHeight)/rowcount
        width=float(srcWidth)/colcount

        print height,width
        pgBottom=copy.copy(srcPg)
        pgBottom.mediaBox.upperRight = (
            pgBottom.mediaBox.getUpperRight_x(),
            pgBottom.mediaBox.getUpperRight_y()/2
            )
        for r in range(rowcount) :
            for c in range(colcount) :
                pg=copy.copy(srcPg)
                pg.mediaBox.upperRight = (ur_x,ur_y)
                pg.mediaBox.lowerRight = (lr_x,lr_y)
                 


                
        
            output.addPage(pg)
    output.write(file(outfile,'wb'))
    
def die_with_usage() :
    print 'pdfbreak.py uses pypdf to break pages'
    print 'Usage:'
    print 'pdfbreak.py [flags] <pdffile>'
    print 'Flags'
    print '  -margin <px>  : remove a margin of px pixels'
    print '  -R <rowcount> : an optional number of row breaks to make. Default is 2 (as if source was "2up")'
    print '  -C <colcount> : an optional number of col breaks to make. Default is 1 (as if source was "2up")'
    print 'Arguments'
    print '  pdffile       :the pdf file to be split'
    print 'Output is written to break_<pdffile>'
    print 'Note: input file must end with .pdf'
    sys.exit(0) 



##----MAIN ----
if __name__=='__main__' :
    if len(sys.argv)<2 :
        die_with_usage()

    rowcount=2
    colcount=1
    marginPx=0
    while True :
        if sys.argv[1]=='-margin' :
            marginPx=int(sys.argv[2])
            sys.argv.pop(1)
        elif sys.argv[1]=='-R' :
            rowcount=int(sys.argv[2])
            sys.argv.pop(1)
        elif sys.argv[1]=='-C' :
            colcount=int(sys.argv[2])
            sys.argv.pop(1)        
        else :
            break
        sys.argv.pop(1)
        
    pdffile=sys.argv[len(sys.argv)-1]

    if not pdffile.lower().endswith('.pdf') :
        die_with_usage()

    outfile = '%s_break.pdf' % (pdffile[0:len(pdffile)-4])
    print 'Creating %s from %s using %i rows %i cols' % (outfile,pdffile,rowcount,colcount)
    pdfbreak(pdffile,outfile,rowcount=rowcount,colcount=colcount,marginPx=marginPx)


        

