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
    AHHost host1 = AHHost();
    AHHost host2 = AHHost();
    
    AHTrack* track1 = host1.AddTrack("Kontakt 3");
    AHTrack* track2 = host2.AddTrack("Kontakt 3");
    
    track1->GetSynth()->LoadAUPresetFromFile("/Volumes/data/valid/valid_kontakt/z/g/zgstmij/Kontakt 3.aupreset");
    track2->GetSynth()->LoadAUPresetFromFile("/Volumes/data/valid/valid_kontakt/z/w/zw8xz1s/Kontakt 3.aupreset");
    
    //AHAudioUnit* dub1 = track1->AddEffect("TAL dub III Plugin");
    AHAudioUnit* dub2 = track2->AddEffect("TAL dub III Plugin");
    
    //dub1->LoadAUPresetFromFile("/Volumes/data/valid/valid_kontakt/z/g/zgstmij/TAL dub III Plugin.aupreset");
    dub2->LoadAUPresetFromFile("/Volumes/data/valid/valid_kontakt/z/w/zw8xz1s/TAL dub III Plugin.aupreset");
    
    host1.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    host2.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    
    host2.Play();3
    usleep(50000);
    host2.Stop();
    host2.ResetAudioUnits();
    host1.Play();
    
    CFRunLoopRun();
}