/*
 *  simonTest.cpp
 *
 *  Created by simon on 14/03/09.
 *  Copyright 2009 . All rights reserved.
 *
 */

//#define DEBUG 1

#include <AudioToolbox/AudioToolbox.h>
#include <CoreAudio/CoreAudio.h>
#include "AHHost.h"
#include "AHAudioUnit.h"
#include "AHUtils.h"
#include "FileSystemUtils.h"

#include <iostream>
using namespace std;

void print_host(AHHost &host)
{    
    for (int i=0; i<(int)host.GetTracks().size(); i++)
    {
        AHTrack* t = host.GetTracks()[i];
        cout << "track " << i << ": ";
        PrintCFStringRef(t->GetSynth()->GetName());
        list<AHAudioUnit*> effects = t->GetEffects();
        for ( list<AHAudioUnit*>::iterator it=effects.begin(); it != effects.end(); it++)
        {
            cout << " => [";
            PrintCFStringRef((*it)->GetName());
            cout << "]";
        }
        cout << endl;            
    }        
}

int main( int argc, const char* argv[] )
{
    //PrintAllAudioUnits();
    //AHHost host = AHHost();
    //AHTrack* track = host.AddTrack("automat1");
    //host.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    
    AHHost host2 = AHHost();
    AHTrack* track2 = host2.AddTrack("automat1");
    AHAudioUnit* reverb = track2->AddEffect("TAL Reverb Plugin");
    //camel->LoadAUPresetFromFile("/Users/simon/Lib/Gamme/projects/timbre/synthparams/test/l/0/l0kdhv0/CamelCrusher.aupreset");
    AHAudioUnit* dub = track2->AddEffect("TAL Dub III Plugin");
    //dub->LoadAUPresetFromFile("/Users/simon/Lib/Gamme/projects/timbre/synthparams/test/l/0/l0kdhv0/TAL Dub III Plugin.aupreset");
    
    host2.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    //host.BounceToFile("/Users/simon/tmp/test.wav");
    //track->Arm();
    printf("\nplaying");
    host2.Play();
    usleep(300000);
    host2.Stop();
    host2.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/63.mid");
    host2.Play();
    usleep(400000);
    host2.Play();
    printf("\nstoping");

    //host2.ResetAudioUnits();
    sleep(12); 
    

}
    