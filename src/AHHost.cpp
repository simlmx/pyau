/*
 *  AHHost.cpp
 *  Midi2Audio
 *
 *  Created by simon on 20/04/09.
 *  Modified on march 16th 2010
 *  Copyright 2009 . All rights reserved.
 *
 */

#include <sstream>
#include <iostream>
#include <iomanip>

#include "AHHost.h"



using namespace std;

namespace
{
    const string MIDI_EXTENSION( ".mid" );
    const string WAV_EXTENSION( ".wav" );

	//UInt32 OFFLINE_RENDER_PROPERTY_VALUE = 1;
    //Float32 START_TIME = 0;
}


AHHost::AHHost():
	listeningToMidi_(true),
    graph_(&tracks_),
    midiPlayer_(&graph_, &tracks_),
    bufferSize_(DEFAULT_BUFFER_SIZE),
    sampleRate_(DEFAULT_SAMPLE_RATE)
{    
   	//we want to listen for incoming midi
	PrintIfErr( MIDIClientCreate(CFSTR("AudioUnitHost"), NULL, NULL, &client_) );
	PrintIfErr( MIDIInputPortCreate(client_, 
									  CFSTR("InputPort"), 
									  MidiReadProc, 
									  this, 
									  &inputPort_ ) );
	
	for(int i=0; i<int(MIDIGetNumberOfSources()); i++)
		PrintIfErr( MIDIPortConnectSource(inputPort_, MIDIGetSource(i), NULL) );
	ListenToMidi();
    //listeningToMidi_ = true;
    graph_.Start();
}	


AHHost::~AHHost()
{
	for(int i=0; i<int(MIDIGetNumberOfSources()); i++)		
		PrintIfErr( MIDIPortDisconnectSource(inputPort_, MIDIGetSource(i)) );
	PrintIfErr( MIDIPortDispose(inputPort_) );
	PrintIfErr( MIDIClientDispose(client_) );
    
    //StopListeningToMidi();
    graph_.Stop();
    graph_.DisconnectMixerInputs();
    graph_.UpdateGraph();
    
    for(int i=0; i<(int)tracks_.size(); i++)
        delete tracks_.at(i);
}

void AHHost::Reset()
{
	midiPlayer_.Reset();
}

void AHHost::LoadMidiFile(const std::string midiFile)
{
	midiPlayer_.LoadMidiFile(midiFile);	
}

void AHHost::CreateOneNote(int noteNumber, float duration, int velocity)
{
    midiPlayer_.CreateOneNote(noteNumber, duration, velocity); 
}

// Most was copy-pasted from PlaySequence example
void AHHost::Play()
{	
    // in case we were already playing
    Stop();
    ResetAudioUnits();
    //StopListeningToMidi();
	midiPlayer_.Start();
    PrintIfErr( AUGraphAddRenderNotify(graph_.GetAUGraph(), PlayCallBack, this) );
}

OSStatus AHHost::PlayCallBack(	void *							inRefCon,
                              AudioUnitRenderActionFlags *	ioActionFlags,
                              const AudioTimeStamp *			inTimeStamp,
                              UInt32							inBusNumber,
                              UInt32							inNumberFrames,
                              AudioBufferList *				ioData)
{
    AHHost* host = (AHHost*)inRefCon;
    AHMidiPlayer* midiplayer = host->GetAHMidiPlayer();
    MusicTimeStamp time;
    PrintIfErr( MusicPlayerGetTime(midiplayer->GetMusicPlayer(), &time) );	
    //printf("%2.2f sur %2.2f\n", time , midiplayer->GetSequenceLength());

	if ( time >= midiplayer->GetSequenceLength() )
        host->Stop();

    
    return noErr;
}

void AHHost::PlayAndBlock()
{
    // could be improved, we should listen to the sound to know when to stop, not to the sequence_length, which is
    // often too long
    Stop();
    ResetAudioUnits();
    AHMidiPlayer* midiplayer = this->GetAHMidiPlayer();
    midiplayer->Start();
    
    MusicTimeStamp time;
    while(true)
    {
        PrintIfErr( MusicPlayerGetTime(midiplayer->GetMusicPlayer(), &time) );
        if( time >= midiplayer->GetSequenceLength() )
            return;
    }
}


void AHHost::Stop()
{
    Boolean isPlaying;
    MusicPlayerIsPlaying(this->midiPlayer_.GetMusicPlayer(), &isPlaying);
    
    /*if (isRunning)
        printf("\ngraph is running");
    else 
        printf("\ngraph is NOT running");*/
    
    PrintIfErr( AUGraphRemoveRenderNotify(this->GetAHGraph()->GetAUGraph(), PlayCallBack, this) );
    if (isPlaying)
    {
        midiPlayer_.Stop();
    	Reset();
    }    
    
    /*MusicPlayerIsPlaying(this->midiPlayer_.GetMusicPlayer(), &isPlaying);
    if (isPlaying)
        printf("\n music player still playing???");
    
    Boolean isRunning;
    AUGraphIsRunning(graph_.GetAUGraph(), &isRunning);
    if (isRunning)
        printf("\nit is still runnin!");*/
    
    //if (!IsListeningToMidi())
    //    ListenToMidi();
}

// Most was copy-pasted from PlaySequence example
void AHHost::BounceToFile( const string& outputFilePath )
{
	StopListeningToMidi();    

	// we change the outputunit temporarily
	CAComponentDescription tempDesc = graph_.GetOutput()->Comp().Desc();
	graph_.SetOutput(GENERIC_OUTPUT_DESCRIPTION);

	// offline render mode
	UInt32 value =1;
	for (UInt32 i=0; i<tracks_.size(); i++)
    {
        AudioUnitSetProperty( tracks_[i]->GetSynth()->AU(),
                                         kAudioUnitProperty_OfflineRender,
                                         kAudioUnitScope_Global,
                             0, &value, sizeof( value ) );
    }

	UInt32 size;
	UInt32 numFrames = bufferSize_;
	Float64 srate = sampleRate_;
	
	CAStreamBasicDescription outputFormat;
	outputFormat.mChannelsPerFrame = 2;
	outputFormat.mSampleRate = srate;
	outputFormat.mFormatID = kAudioFormatLinearPCM;	
	outputFormat.mBytesPerPacket = outputFormat.mChannelsPerFrame * 2;
	outputFormat.mFramesPerPacket = 1;
	outputFormat.mBytesPerFrame = outputFormat.mBytesPerPacket;
	outputFormat.mBitsPerChannel = 16;		
	outputFormat.mFormatFlags = kLinearPCMFormatFlagIsSignedInteger | kLinearPCMFormatFlagIsPacked;
			
	//printf ("Writing to file: %s with format:\n* ", outputFilePath.c_str());
	//outputFormat.Print();
	
	//FileSystemUtils::DeleteFile(outputFilePath); in a flag in ExtAudioFileCreateWithURUL since 10.6
	//FileSystemUtils::CreateDirectory(FileSystemUtils::GetParentDirectoryPath(outputFilePath)); some bug with that... we'll have to create the dir by hand... or in python wrapper

//	FSRef parentDir;
//	CFStringRef destFileName;
//	verify_noerr( PosixPathToParentFSRefAndName(outputFilePath.c_str(), parentDir, destFileName) );
	
	ExtAudioFileRef outfile;
    CFStringRef path = CFStringCreateWithCString(kCFAllocatorDefault, outputFilePath.c_str(), kCFStringEncodingMacRoman);
    CFURLRef url = CFURLCreateWithString(NULL, path, NULL);
	//verify_noerr( ExtAudioFileCreateNew (&parentDir, destFileName, kAudioFileWAVEType, &outputFormat, NULL, &outfile) );
    
    PrintIfErr( ExtAudioFileCreateWithURL(url, kAudioFileWAVEType, &outputFormat, NULL, kAudioFileFlags_EraseFile, &outfile) );
      
	CFRelease (path);
	
	AudioUnit outputUnit = graph_.GetOutput()->AU();
	
	{
		CAStreamBasicDescription clientFormat;
		size = sizeof(clientFormat);
		PrintIfErr (AudioUnitGetProperty (outputUnit,
													  kAudioUnitProperty_StreamFormat,
													  kAudioUnitScope_Output, 0,
													  &clientFormat, &size) );
		size = sizeof(clientFormat);
		PrintIfErr( ExtAudioFileSetProperty(outfile, kExtAudioFileProperty_ClientDataFormat, size, &clientFormat) );
		
		{
			MusicTimeStamp currentTime;
			AUOutputBL outputBuffer (clientFormat, numFrames);
			AudioTimeStamp tStamp;
			memset (&tStamp, 0, sizeof(AudioTimeStamp));
			tStamp.mFlags = kAudioTimeStampSampleTimeValid;
			//int i = 0;
			//int numTimesFor10Secs = (int)(10. / (numFrames / srate));
			MusicTimeStamp sequenceLength = midiPlayer_.GetSequenceLength();
			midiPlayer_.Start();
			do {
				outputBuffer.Prepare();
				AudioUnitRenderActionFlags actionFlags = 0;
				PrintIfErr( AudioUnitRender (outputUnit, &actionFlags, &tStamp, 0, numFrames, outputBuffer.ABL()) );
				
				tStamp.mSampleTime += numFrames;
				
				PrintIfErr( ExtAudioFileWrite(outfile, numFrames, outputBuffer.ABL()) );	
				
				midiPlayer_.GetTime(&currentTime);
				//if (++i % numTimesFor10Secs == 0)
				//	printf ("current time: %6.2f beats\n", currentTime);
			} while (currentTime < sequenceLength);
			midiPlayer_.Stop();
			Reset();
		}
	}
	
	// close
	ExtAudioFileDispose(outfile);
	
	// disabling the offline render mode
	value =0;
	for (UInt32 i=0; i<tracks_.size(); i++)
    {
        AudioUnitSetProperty( tracks_[i]->GetSynth()->AU(),
                                     kAudioUnitProperty_OfflineRender,
                                     kAudioUnitScope_Global,
                                     0,
                                     &value,
                                 sizeof( value ) );

    }
	
	// we set back the output unit
    
    graph_.SetOutput(tempDesc);
	ListenToMidi();
}

vector< list< vector<float> > > AHHost::Bounce()
{
    //CAStreamBasicDescription outputStreamDescription;	
	//GetOutputUnitStreamFormat(outputStreamDescription);
		
	vector< list< vector<float> > > data = RenderToBuffer();//(outputStreamDescription);
	
	return data;
}

vector< list< vector<float> > > AHHost::RenderToBuffer()//CAStreamBasicDescription& outputStreamDescription)
{
	StopListeningToMidi();
	CAComponentDescription tempDesc = graph_.GetOutput()->Comp().Desc();
	graph_.SetOutput(GENERIC_OUTPUT_DESCRIPTION);
	UInt32 value =1;
	for (UInt32 i=0; i<tracks_.size(); i++)
    {
        AudioUnitSetProperty( tracks_[i]->GetSynth()->AU(),
                                         kAudioUnitProperty_OfflineRender,
                                         kAudioUnitScope_Global,
                             0, &value, sizeof( value ) );
    }
//	UInt32 bufferSize = auChainGroup_->GetBufferSize();
	CAStreamBasicDescription outputUnitFormat;
	GetOutputUnitStreamFormat(outputUnitFormat);
    AUOutputBL outputBuffer( outputUnitFormat, bufferSize_ );
	
//	outputUnitFormat.Print();
	
    MusicTimeStamp currentTime;
    AudioTimeStamp tStamp;
    memset(&tStamp, 0, sizeof(AudioTimeStamp));
    tStamp.mFlags = kAudioTimeStampSampleTimeValid;
    
    MusicTimeStamp musicSequenceLength = midiPlayer_.GetSequenceLength();
    AudioUnit outputUnit = graph_.GetOutput()->AU();
	int nbChannels = outputUnitFormat.NumberChannels();

	vector< list< vector<float> > > data;
	for (int i=0; i<nbChannels; i++)
	{
		list< vector<float> > temp;
		data.push_back(temp);
	}
		
	midiPlayer_.Start();
    do
    {
		outputBuffer.Prepare();
        AudioUnitRenderActionFlags actionFlags = 0;
        PrintIfErr( AudioUnitRender(outputUnit,
                                    &actionFlags,
                                    &tStamp,
                                    0,
                                    bufferSize_,
                                    outputBuffer.ABL()));
        
        tStamp.mSampleTime += bufferSize_;
		AudioBufferList* abl = outputBuffer.ABL();
		for(UInt32 i=0; i<abl->mNumberBuffers; i++)//buffers/channels
		{
			vector<float> data_temp(bufferSize_);
			AudioBuffer ab = abl->mBuffers[i];
			// TODO : if my understanding is correct, since we assume that we are using the genericOutput, we also assume that 32-bit little-endian float, deinterleaved
			//        are coming from AudioUnitRender
			memcpy(&(data_temp[0]), ab.mData, ab.mDataByteSize);
			data[i].push_back(data_temp);
			
		}
				
        midiPlayer_.GetTime( &currentTime );        
    }
    while (currentTime < musicSequenceLength);
	
//	cout << (*(data[0].begin()))[0] << "  " << (*(data[0].begin()++))[1] << endl;
	
	//outputBuffer.Print();
	
	midiPlayer_.Stop();
	
	value =0;
	for (UInt32 i=0; i<tracks_.size(); i++)
    {
		AudioUnitSetProperty( tracks_[i]->GetSynth()->AU(),
                                         kAudioUnitProperty_OfflineRender,
                                         kAudioUnitScope_Global,
                                         0,
                                         &value,
                                 sizeof( value ) );

    }
	graph_.SetOutput(tempDesc);
	
	Reset();
	
	//for(int j=0; j<nbChannels; j++)
//	{
//		for(int i=0; i<10; i++)
//			printf("%.5f ", data[j].front()[i]);
//		printf("\n");
//	}
	
//	cout << (*(data[0].begin()))[0] << "  " << (*(data[0].begin()++))[1] << endl;
	ListenToMidi();
	return data;
}

void AHHost::GetOutputUnitStreamFormat(CAStreamBasicDescription& outOutputUnitStreamDescription)
{
    AudioUnit outputUnit = graph_.GetOutput()->AU();
    UInt32 size = sizeof(outOutputUnitStreamDescription);
    PrintIfErr(AudioUnitGetProperty(outputUnit, kAudioUnitProperty_StreamFormat, kAudioUnitScope_Output, 0, &outOutputUnitStreamDescription, &size));	
}

void AHHost::MidiReadProc(const MIDIPacketList* pktlist, void* readProcRefCon, void* srcConnRefCon)
{
	AHHost* host = (AHHost*)readProcRefCon;
	if (host->IsListeningToMidi() && host->GetTracks().size())
	{
        int numPackets = pktlist->numPackets;
        if (!numPackets)
            return;
        const MIDIPacket* pkt = &pktlist->packet[0];
        bool retour_chariot = false;
		for(int i=0; i<numPackets; ++i)		
		{
            for(int j=0; j<pkt->length; j++)
            {
                UInt32 status = (UInt32) pkt->data[j];
                UInt32 data1 = (UInt32) pkt->data[j+1];
                UInt32 data2 = (UInt32) pkt->data[j+2];
                
                // let's filter some messages before printing
                /*if ( !(status == 0xf8 || status == 0xfe) )
                {
                    cout << "( ";
                    cout << hex << status << " ";
                    cout << hex << data1 << " ";
                    cout << hex << data2 << " )";
                    retour_chariot = true;
                }*/
                vector<AHTrack*> tracks = host->GetTracks();
                    
                // And we send the midi message to every armed track
                for ( int i=0; i<(int)tracks.size(); i++)
                    if (tracks[i]->IsArmed())
                        tracks[i]->GetSynth()->MIDIEvent(status, data1, data2, 0);                
                j+=2;
            }
            pkt = MIDIPacketNext(pkt);
		}
    
    //if(retour_chariot)
    //    cout << endl;   
	}
}

AHTrack* AHHost::AddTrack(const CAComponentDescription synthDescription)
{
    graph_.DisconnectMixerInputs();
    AHTrack* track = new AHTrack(synthDescription, &graph_, tracks_.size());
    tracks_.push_back(track);
    graph_.ConnectMixerInputs();
    graph_.UpdateGraph();
    
    //TODO : if it's the first track, we should arm it!
    //       or something like this... I need to think about this

    return tracks_.back();
}

AHTrack* AHHost::AddTrack(const string name, const string manu)
{
    CAComponentDescription desc;
    if (FindAudioUnitFromName(name, manu, desc))
    {
        return AddTrack(desc);  
    } else
    {        
        cout << "\nThe audio unit '" << name;
        if (!manu.empty())
            cout << "' - '" << manu;
        cout << "' could not be found";
        return NULL;
    }
}

void AHHost::RemoveLastTrack()
{
    graph_.DisconnectMixerInputs();
    delete tracks_.back();
    tracks_.pop_back();
    graph_.ConnectMixerInputs();
    graph_.UpdateGraph();
}

void AHHost::ListenToMidi()
{
    listeningToMidi_ = true;
//    graph_.Start();
}

void AHHost::StopListeningToMidi()
{
    listeningToMidi_ = false;
//    graph_.Stop();
}


void ResetAudioUnit(AHAudioUnit* audiounit)
{
//    printf("\nCleaning ");
//    PrintCFStringRef(audiounit->GetName());

    //AudioUnit au = audiounit->AU();
    
    //PrintIfErr( MusicDeviceMIDIEvent(au, 0xb0, 123, 0, 0) );
    //PrintIfErr( MusicDeviceMIDIEvent(au, 0xb0, 120, 0, 0) );
    
    PrintIfErr( audiounit->GlobalReset() );
    
    PrintIfErr( audiounit->Reset(kAudioUnitScope_Input, 0) );
    if( audiounit->Reset(kAudioUnitScope_Output, 0) )
        printf("\n no output");    
    
    //PrintIfErr( audiounit->Uninitialize() );
    //PrintIfErr( audiounit->Initialize() );
}

void AHHost::ResetAudioUnits()
{    
    for (vector<AHTrack*>::iterator it = tracks_.begin(); it!= tracks_.end(); it++)
    {
        ResetAudioUnit((*it)->GetSynth());
        
        list<AHAudioUnit*> effects = (*it)->GetEffects();
        int i=0;
        for (list<AHAudioUnit*>::iterator jt = effects.begin(); jt != effects.end(); jt++)
        {            
            // HACK
            // HACK for some plugins that doesn't reset
            // HACK
            CAComponentDescription desc = (*jt)->Comp().Desc();
            if ( (desc.Type() == 'aumf' && desc.SubType() == '676v' && desc.Manu() == 'TOGU') || // TAL reverb 1
                 (desc.Type() == 'aumf' && desc.SubType() == 'xg70' && desc.Manu() == 'TOGU')  ) // TAL dub 3
            {
                CFPropertyListRef preset;
                PrintIfErr( (*jt)->GetAUPreset(preset) );
                (*it)->RemoveEffectAt(i);
                AHAudioUnit* new_au = (*it)->AddEffect(desc, i);
                (new_au)->SetAUPreset(preset);
            }
            else
                ResetAudioUnit(*jt);

            i++;
        }
    }
    //ResetAudioUnit(graph_.GetMixer());
    //ResetAudioUnit(graph_.GetOutput());   
}