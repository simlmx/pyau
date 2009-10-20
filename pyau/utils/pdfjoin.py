#! /usr/bin/env python
import sys
import os
import unicodedata

def command_with_output(cmd):
    cmd = unicode(cmd,'utf-8')
    #should this be a part of slashify or command_with_output?
    if sys.platform=='darwin' :
        cmd = unicodedata.normalize('NFC',cmd)
    child = os.popen(cmd.encode('utf-8'))
    data = child.read()
    err = child.close()
    return data


def pdfjoin(infiles,outfile):
    from pyPdf import PdfFileWriter
    from pyPdf import PdfFileReader
    
    outpdf = PdfFileWriter()
    for ifile in infiles :
        inpdf = PdfFileReader(file(ifile, "rb"))
        pgcnt=inpdf.getNumPages()
        for p in range(pgcnt) :
            outpdf.addPage(inpdf.getPage(p))
    outpdf.write(file(outfile,'wb'))
    
def die_with_usage() :
    print 'pdfjoin.py uses pypdf to join pages'
    print 'Usage:'
    print 'pdfjoin.py [flags] <infile1> ... <infile_k> <outfile>'
    print '<infile1> ... <infile_k> are joined and written to the file <outfile>'

    sys.exit(0) 



##----MAIN ----
if __name__=='__main__' :
    if len(sys.argv)<2 :
        die_with_usage()


    infiles=sys.argv[1:len(sys.argv)-1]
    outfile=sys.argv[-1]

    if os.path.exists(outfile) :
        while True :
            ans = raw_input('File %s exists. Do you want to overwrite it? y/N >' % outfile)
            if ans.lower()=='y' :
                break
            elif ans.lower()=='n' :
                sys.exit(0)


    print 'Joining infiles',infiles,'to',outfile

    #currently this drops graphics dont know why
    #pdfjoin(infiles,outfile)

    cmd = 'gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=%s' % outfile
    for f in infiles :
        cmd = '%s %s' % (cmd,f)
    print 'Executing',cmd
    command_with_output(cmd)
        

