""" example of usage of pygmy.audiounit """
import pyau

#creating a host
h = pyau.Host()

# adding some tracks 
# we have to specify the synth (by his name) of the track
t = h.add_track('automat1')
t2 = h.add_track('DLSMusicDevice')
# we can also specify the manufacturer, if there might be a conflict (2 audio units with the same name)
t3 = h.add_track('DLSMusicDevice', 'apple')
# if we add a track with a audio unit that doesn't exist, it adds nothing (and returns None)
h.add_track('tests', 'sdfs')
# if you want to know the names and manufacturer of the audio units
# installed on your computer, you can use the next line
#pyau.print_audiounits()

# adding effects
eff = t.add_effect('AUPitch')
t2.add_effect('AUPitch')
# same thing for effects, we could add the manufacturer
t3.add_effect('AUPitch', 'apple')
t3.add_effect('AUPitch', 'apple')

# print the host with his tracks
print h

# to get the synth of a track
s = t2.synth
print s
# we can load a preset
#s.load_aupreset('.../some_preset.aupreset')

# if we want a track to listen to incomming midi messages, we have to "arm" it
t2.arm()

print h

# printing some parameters of an audio unit
print 'Some parameters for synth %s :' % s.name
for p in s.get_parameters()[:10]:
    print p
