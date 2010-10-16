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
    AHHost host = AHHost();
    AHTrack* track = host.AddTrack("automat1");
    
    
    //AHAudioUnit* delay = track->AddEffect("AUDelay");
    //AHAudioUnit* reverb = track->AddEffect("TAL Reverb Plugin");
    //AHAudioUnit* dub = track->AddEffect("TAL dub III Plugin");
    //track->AddEffect("camelcrusher");
    AHAudioUnit* reverb = track->AddEffect("TAL Reverb Plugin");
    //track->AddEffect("camelcrusher");
    
    
    track->GetSynth()->LoadAUPresetFromFile("/Users/simon/tmp/debug_reset_aut1.aupreset");
    track->Arm();
    AHAudioUnit* matrixrev = track->AddEffect("AUMatrixReverb");
    reverb->LoadAUPresetFromFile("/Users/simon/tmp/debug_reset_rev.aupreset");
    //dub->LoadAUPresetFromFile("/Users/simon/tmp/debug_reset_dub.aupreset");
    //delay->LoadAUPresetFromFile("/Users/simon/tmp/debug_reset_delay.aupreset");
    host.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/59.mid");
    
    printf("presque\n");
    list<AUPreset> liste = matrixrev->GetFactoryPresetList(0,0);
    list<AUPreset> liste2 = track->GetSynth()->GetFactoryPresetList(0,0);
    
    for (list<AUPreset>::iterator it=liste.begin(); it!=liste.end(); it++) {
        PrintCFStringRef((*it).presetName);
        printf("\n");
        cout << ((*it).presetNumber) << endl;
    }
    for (list<AUPreset>::iterator it=liste2.begin(); it!=liste2.end(); it++) {
        PrintCFStringRef((*it).presetName);
        printf("\n");
    }
    
    printf("oui\n");
    
    CFRunLoopRun();

    printf("\nplaying");
    host.Play();
    sleep(1);
    //reverb->SaveAUPresetToFile("/Users/simon/tmp/temp_preset.aupreset");
    printf("\nStop");
    host.Stop();
    host.ResetAudioUnits();
    sleep(2);
    //AUGraphStop(host.GetAHGraph()->GetAUGraph());
//    printf("\nReset");

    
    //track->RemoveEffectAt(1);
    
    host.Play();
    
    sleep(1);
    host.Stop();
    //AUGraphStart(host.GetAHGraph()->GetAUGraph());
    
    //host.LoadMidiFile("/Users/simon/Lib/pyau/pyau/ressources/63.mid");
    //host.Play();

    //host2.ResetAudioUnits();
    sleep(12); 
    

}
    