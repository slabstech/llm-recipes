Trajectory Generators

TODO
- Add Docker compose for 
	- ollama with gpu
	- ollama with cpu
- replace code intepreter with codestral
- test runs with mistral7b. 8x7b and 7x22b 
- Trial finetuning 7b using examples.

- How can this idea added to Warehouse automation. can we augment it to bin pick robots.
 
	


- Commands
`
git clone --recurse-submodules https://github.com/kwonathan/language-models-trajectory-generators.git

cd language-models-trajectory-generators/

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

# remove thinplate

pip install -U git+https://github.com/luca-medeiros/lang-segment-anything.git



mkdir XMem/saves

mkdir -p images/trajectory

wget -P XMem/saves https://github.com/hkchengrex/XMem/releases/download/v1.0/XMem.pth

`
# TODO - Replace openAI with ollama + Mistral 


--
- Reference
  - https://github.com/johanndiep/language-models-trajectory-generators/tree/main_mistral
  - https://github.com/luca-medeiros/lang-segment-anything
