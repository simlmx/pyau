#! /usr/bin/env python
from pyPdf import PdfFileWriter
from pyPdf import PdfFileReader
import sys

def pdfsplit(infile,pages=list(),doBreak=False):


    
    input1 = PdfFileReader(file(infile, "rb"))
    pgcnt=input1.getNumPages()

    if len(pages)==0 :
        pages=range(1,pgcnt+1)
        

    print 'Infile is',infile,infile.endswith('.pdf')
    if not (infile.endswith('.pdf') or infile.lower().endswith('.pdf')) :
        print 'Must provide a file with extension .pdf'
        return

    stub=infile[0:len(infile)-4]
    for p in pages :


        if doBreak :
	    outfile='%s_%ia.pdf' % (stub,p)
            print 'Writing page',p,'a from',infile,'to',outfile
            output = PdfFileWriter()
            output.addPage(input1.getPage(p-1))
            output.write(file(outfile,'wb'))
	else :		
            outfile='%s_%i.pdf' % (stub,p)
            print 'Writing page',p,'from',infile,'to',outfile
            output = PdfFileWriter()
            output.addPage(input1.getPage(p-1))
            output.write(file(outfile,'wb'))
    
def die_with_usage() :
    print 'pdfsplit.py uses pypdf to split pages'
    print 'Usage:'
    print 'pdfsplit.py [flags] <pages> <pdffile>'
    print 'Flags'
    print '   -break -- breaks a 2up page into 2 individual pages a and b'
    print 'Arguments'
    print '    pages -- an optional sequence of pages. If omitted all pages are split'
    print '  pdffile -- the pdf file to be split'
    print 'Output is written to appropriately-numbered pages'
    print 'EG: file.pdf yields file_1.pdf file_2.pdf ...'
    print 'Examples:'
    print 'pdfsplit.py foo.pdf       -- extracts all pages'
    print 'pdfsplit.py 4-23 foo.pdf  -- extracts pages 4 through 23'
    print 'pdfsplit.py 4 5 9 foo.pdf -- extracts pages 4, 5 and 9'

    sys.exit(0) 



##----MAIN ----
if __name__=='__main__' :
    if len(sys.argv)<2 :
        die_with_usage()


    doBreak=True

    pages=list()
    while len(sys.argv)>2 :
        curr=sys.argv[1]
        if curr.count('-')>0 :
            vals = curr.split('-')
            st=int(vals[0])
            en=int(vals[1])
            for i in range(st,en+1) :
                pages.append(i)
        else :
            pages.append(int(sys.argv[1]))

        sys.argv.pop(1)
    
    pdffile=sys.argv[len(sys.argv)-1]
    pdfsplit(pdffile,pages,doBreak=doBreak)
    print pdffile
    print pages
        

