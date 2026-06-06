from resemblyzer import VoiceEncoder,preprocess_wav
import numpy as np
import io #same as pillow
import streamlit as st
import librosa

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()

def get_voice_embeddings(audio_bytes):
    try:
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        wav=preprocess_wav(audio)
        embedding=encoder.embed_utterance(wav)
        return embedding.tolist()
    except Exception as e:
        st.error('voice recognition error')
        return None
    
def identify_speaker(new_embedding,candidate_dict,threshold=0.65):
    if new_embedding is None or not candidate_dict:
        return None,0.0
    
    best_stu_id=None
    best_score=-1.0
    for stu_id,stored_embedding in candidate_dict.items():
        if stored_embedding:
            similarity_score=np.dot(new_embedding,stored_embedding)
            if similarity_score>best_score:
                best_score=similarity_score
                best_stu_id=stu_id
        
    if best_score>=threshold:
        return best_stu_id,best_score
    
    return None,best_score

def process_bulk_audio(audio_bytes,candidate_dict,threshold=0.65):
    try:
        encoder=load_voice_encoder()
        audio,sr=librosa.load(io.BytesIO(audio_bytes),sr=16000)
        segments=librosa.effects.split(audio,top_db=30)
        detected_stu={}
        for st,end in segments:
            if(end-st)<sr*0.5:
                continue
            segment_audio=audio[st:end]
            wav=preprocess_wav(segment_audio)
            embedding=encoder.embed_utterance(wav)
            
            stu_id,best_score=identify_speaker(embedding,candidate_dict,threshold)
            
            if stu_id:
                if stu_id not in detected_stu or best_score>detected_stu[stu_id]:
                    detected_stu[stu_id]=best_score
                    
        return detected_stu
    
    except Exception as e:
        st.error('Bulk process error')
        return {}
    