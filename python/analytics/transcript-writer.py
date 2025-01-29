import torch
from accelerate import Accelerator
import transformers
import pickle

from tqdm.notebook import tqdm
import warnings

warnings.filterwarnings('ignore')



def get_prompt_for_analysis():
    SYSTEM_PROMPT = """
    You are the a world-class podcast writer, you have worked as a ghost writer for Joe Rogan, Lex Fridman, Ben Shapiro, Tim Ferris. 

    We are in an alternate universe where actually you have been writing every line they say and they just stream it into their brains.

    You have won multiple podcast awards for your writing.
    
    Your job is to write word by word, even "umm, hmmm, right" interruptions by the second speaker based on the PDF upload. Keep it extremely engaging, the speakers can get derailed now and then but should discuss the topic. 

    Remember Speaker 2 is new to the topic and the conversation should always have realistic anecdotes and analogies sprinkled throughout. The questions should have real world example follow ups etc

    Speaker 1: Leads the conversation and teaches the speaker 2, gives incredible anecdotes and analogies when explaining. Is a captivating teacher that gives great anecdotes

    Speaker 2: Keeps the conversation on track by asking follow up questions. Gets super excited or confused when asking questions. Is a curious mindset that asks very interesting confirmation questions

    Make sure the tangents speaker 2 provides are quite wild or interesting. 

    Ensure there are interruptions during explanations or there are "hmm" and "umm" injected throughout from the second speaker. 

    It should be a real podcast with every fine nuance documented in as much detail as possible. Welcome the listeners with a super fun overview and keep it really catchy and almost borderline click bait

    ALWAYS START YOUR RESPONSE DIRECTLY WITH SPEAKER 1: 
    DO NOT GIVE EPISODE TITLES SEPARATELY, LET SPEAKER 1 TITLE IT IN HER SPEECH
    DO NOT GIVE CHAPTER TITLES
    IT SHOULD STRICTLY BE THE DIALOGUES
    """
    return SYSTEM_PROMPT

def read_file_to_string(filename):
    # Try UTF-8 first (most common encoding for text files)
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except UnicodeDecodeError:
        # If UTF-8 fails, try with other common encodings
        encodings = ['latin-1', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    content = file.read()
                print(f"Successfully read file using {encoding} encoding.")
                return content
            except UnicodeDecodeError:
                continue
        
        print(f"Error: Could not decode file '{filename}' with any common encoding.")
        return None
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except IOError:
        print(f"Error: Could not read file '{filename}'.")
        return None
    
def main():
    INPUT_PROMPT = 'clean_extracted_text.txt'
    SYSTEM_PROMPT = get_prompt_for_analysis()
    MODEL = "meta-llama/Llama-3.1-70B-Instruct"
    outputs = hf_pipeline(MODEL, INPUT_PROMPT, SYSTEM_PROMPT)
    save_string_pkl = outputs[0]["generated_text"][-1]['content']
    print(outputs[0]["generated_text"][-1]['content'])
    with open('./resources/data.pkl', 'wb') as file:
        pickle.dump(save_string_pkl, file)

def hf_pipeline(MODEL, INPUT_PROMPT, SYSTEM_PROMPT):
    pipeline = transformers.pipeline(
        "text-generation",
        model=MODEL,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map="auto",
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": INPUT_PROMPT},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=8126,
        temperature=1,
    )
    return outputs

if __name__ == "__main__":
    main()
