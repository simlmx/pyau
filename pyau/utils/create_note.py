#! /usr/bin/env python
''' 
    Simon Lemieux
    27 dec 2009
    
    Creating 1-note midi files
'''

import sys

from midi import *

def create_1note_midifiles(notes, velocities, durations, midi_filename):
    ''' See method print_usage_and_exit() for help
        For more fancy
    '''    
    count = 0
    for n in notes:
        for v in velocities:
            for d in durations:
                
                filename = midi_filename.replace('[note]', str(n))
                filename = filename.replace('[velocity]', str(v))
                filename = filename.replace('[duration]', str(d))

                #print n,v,d
                #print filename 

                file = MidiFile()
                file.file = open(filename, 'w')
                file.ticksPerQuarterNote = 96
                
                track = MidiTrack(0)
                file.tracks=[track]
                
                time = 0
                delta0 = DeltaTime(track)
                delta0.time = 0
                
                time += delta0.time
            
                note_on = MidiEvent(track)
                note_on.type = "NOTE_ON"
                note_on.time = time
                note_on.velocity = v
                note_on.pitch = n
                note_on.channel = 1
                
                delta1sec = DeltaTime(track)
                delta1sec.time = int(96./500.*d + .5)
                
                time += delta1sec.time    
                
                note_off = MidiEvent(track)
                note_off.type = "NOTE_ON"
                note_off.time = time
                note_off.velocity = 0
                note_off.pitch = n
                note_off.channel = 1
                
                time += delta0.time
            
                end_of_track = MidiEvent(track)
                end_of_track.type = "END_OF_TRACK"
                end_of_track.time = delta0.time + delta1sec.time
                end_of_track.data = ''
                
                track.events = [delta0, note_on, delta1sec, note_off, delta0, end_of_track]
                
                #print file
                file.write()    
                file.file.close()
                count += 1
    print '%i midi files have been created' % count
            

def print_usage_and_exit():
    print
    print 'python create_note.py -n notes [-v velocity -d duration -o midi_filename]'
    print 
    print 'Creates midi files with a single note of a given pitch/velocity/duration.'
    print 
    print 'Arguments :'
    print '  - notes'
    print '          Can be either an integer between 0 and 127 (representing the midi note) or'
    print '          a range first-last-step, e.g 100-106-2 would create 4 midi files with midi notes 100, 102, 104 and 106.'

    print '  - velocity'
    print '          The velocity of the note(s), between 0 and 127.'
    print '          Like the previous parameter, can be of the form first-last-step.'
    print '          All combinations of notes/velocities will be computed.' 
    print '          default value of 100'
    print '  - duration'
    print '          The duration of the note(s) in ms'
    print '          default value of 1500 (1.5 sec)'
    print '          Again, can be of the form first-last-step.'
    print '  - midi_filename'
    print '          The name of the midi files.'
    print '          "[note]" "[velocity]" "[duration]" will be replaced by, respectively, the note number, the velocity and the duration.'
    print '          e.g. "python create_note.py -n 40 -o note_[note].mid" will create a file name note_40.mid'
    print 
    print 'Typical use :' 
    print '   python create_note.py -n 0-127 -v 80 -d 1000 -o [note].mid'
    print
    sys.exit()
    
    
if __name__ == '__main__':
    
    
    def arg_to_range(str):
        ''' Example : convert the string '3-7' into the list [3, 4, 5, 6, 7]
                      or 3-7-2 to [3,5,7]
        '''
        arg = map(int,str.split('-'))
        if len(arg) == 1:
            arg *= 2
        if len(arg) == 2:
            arg.append(1)
        arg[1] +=1
        arg = range(*arg)
        return arg
                
    args = sys.argv
    
    if len(args) < 3:
        print_usage_and_exit()    
    
    velocities = [100]
    duration = 1500
    while len(args)>=3:
        if args[1] == '-n':
            notes = arg_to_range(args[2])
        elif args[1] == '-v':
            velocities = arg_to_range(args[2])
        elif args[1] == '-d':
            durations = arg_to_range(args[2])
        elif args[1] == '-o':
            midi_filename = args[2]
        else:
            print 'Error : "' + args[1] + '" is a invialid argument.'
            sys.exit()
        args.pop(1); args.pop(1)
        
    create_1note_midifiles(notes, velocities, durations, midi_filename)
    
