#
# created by simon lemieux
# june 2009
# edited april 2010
#
# Recursive cleaning of files ending with something
# Maybe there's some cleaner command line way to do this...

import sys, os

def die_with_usage():
    print 'usage : python clean_files.py suffix directory'
    print 'delete recursively all files ending by "suffix" in directory'
    print 'example : python clean_lock_files.py .pdf my_dir'
    print '          will delete all *.pdf files recursively in my_dir'
    sys.exit()

if __name__ == '__main__':
    nb_min_args = 3
    if len(sys.argv) < nb_min_args:
        die_with_usage()
        
    suffix = sys.argv[1]
    type = sys.argv[2]

    
    for root, dirs, files in os.walk(dir):
        #print 'in %s' % root
        for f in files:
            if f.endswith(suffix):
                os.remove(os.path.join(root, f))
           
