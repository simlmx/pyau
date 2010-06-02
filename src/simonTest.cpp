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
    PrintAllAudioUnits();
    AHHost host = AHHost();
    AHTrack* track = host.AddTrack("automat1");
    host.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    host.Play();
    sleep(2);
    host.Stop();
}
    