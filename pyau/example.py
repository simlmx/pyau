""" example of usage of pygmy.audiounit """
#todo : change for local stuff, not /users/simon/...
import pygmy.audiounit as AU

h = AU.Host()
t = h.add_track('automat1')
t2 = h.add_track('crystal')
t3 = h.add_track('automat1')
t.add_effect('camelcrusher')
t2.add_effect('camelcrusher')
t2.add_effect('camelcrusher')


print h

s = t.synth
s.load_aupreset('/Users/simon/tmp/test_64.aupreset')

t.arm()
t2.arm()

print h

for p in s.get_parameters()[:10]:
    print p
print '...'