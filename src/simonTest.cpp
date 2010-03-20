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

int main( int argc, const char* argv[] )
{
//    PrintAllAudioUnits();
    /*list<CAComponent> liste = GetMatchingCAComponents(CAComponentDescription('aufx'));
    list<CAComponent> liste2 = GetMatchingCAComponents(CAComponentDescription('aumf'));
    list<CAComponent> listes[] = {liste, liste2};
    for(int i=0; i<2; i++)
    {
        for (list<CAComponent>::iterator it = listes[i].begin(); it != listes[i].end(); it++)
        {
            CAComponentDescription desc = it->Desc();
            char type[5], subtype[5], manu[5];
            FileSystemUtils::OSType2str(desc.Type(), type);
            FileSystemUtils::OSType2str(desc.SubType(), subtype);
            FileSystemUtils::OSType2str(desc.Manu(), manu);
            cout << type << " " << subtype << " " << manu << " ";
            PrintCFStringRef(it->GetAUName()); cout << endl;
        }
        cout << endl;
    }*/
    
    
    AHHost host;
    AHTrack* track1 = host.AddTrack("Automat1");
    AHTrack* track2 = host.AddTrack("Crystal");
    AHTrack* track3 = host.AddTrack("Automat1");
    AHTrack* track4 = host.AddTrack("Crystal");

    track3->AddEffect("Chorus-60-AU-Effect");
    track3->AddEffect("CamelCrusher");
    
    track2->AddEffect("CamelCrusher");
    track2->AddEffect("CamelCrusher");
    
    track3->RemoveLastEffect();

    track1->Arm();
    
    track3->SetSynth("Crystal");
    
    host.LoadMidiFile("/Users/simon/tmp/midis/69.mid");
    host.Bounce();
    
    while(1)
        sleep(1);
}