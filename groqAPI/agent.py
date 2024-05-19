import json
import os
from GroqInteractor import GroqInteractor
from election_api import *
from vector_api import *
import re

class Agent:

    def __init__(self):
        self.message_list = []
        self.llm = GroqInteractor()
        self.nextStep = "IntroduceYourself"
        self.summary = None
        self.exact_result_requirement = {}
        
        self.looper = [
            "IntroduceYourself",
            "ClarifyUserRequest",
            "GetUserInput",
            "ChooseStep",
            "UseToolToFindInformationAboutUserQuery",
        ]

        self.finderPromptNames = {
            "exact_year":"findExactYear",
            "exact_constituency":"findExactStateOrConstituency",
            "exact_state":"findExactStateNameInYear",
            "exact_party":"findExactPartyInYear",
        }

        self.dependencies = {
            "exact_constituency":["exact_year"],
            "exact_state":["exact_year"],
            "exact_party":["exact_year"],
            "exact_year":[],
            "exact_candidate":["exact_year"],
        }

        self.dbDependencies = {
            "exact_constituency": [
                {
                    "name":"state_list",
                    "fn":get_states_in_year,
                    "args":[
                        "exact_year"
                    ]
                },
                {
                    "name":"constituency_list",
                    "fn":get_constituencies_in_year,
                    "args":[
                        "exact_year"
                    ]
                } 
            ], 
            "exact_state": [
                {
                    "name":"state_list",
                    "fn":get_states_in_year,
                    "args":[
                        "exact_year"
                    ]
                }
            ],
            "exact_party": [
                {
                    "name":"party_list",
                    "fn":get_parties_in_year,
                    "args":[
                        "exact_year"
                    ]
                }
            ], 
            "exact_candidate": [
                {
                    "name":"candidate_list",
                    "fn":get_closest_docs_to_summary,
                    "args":[
                        "exact_year"
                    ]
                }
            ]

        }

        _tools = []
        for f in os.listdir("./Prompts"):
            if f.endswith(".txt"):
                _tools.append(f.split(".")[0])

        self.tool_dependencies = {}

        for t in _tools:
            #Find the dependencies of the tool. These will be variable names in curly brackets like {exact_year}
            with open(f"./Prompts/{t}.txt") as f:
                _content = f.read()
                #use regex to find all the dependencies
                _deps = re.findall(r"\{(.+?)\}", _content)
                self.tool_dependencies[t] = _deps
                

    def _greyPrint(self, *args):
        print("\033[90m", end="")
        print(*args)
        print("\033[0m", end="")

    def _getInputFromUser(self):
        _mess = input("You: ")
        self._addMessageToList(_mess, "user")
        return _mess
    
    def _addMessageToList(self, message, role):
        self.message_list.append({
                "role":role,
                "content":message
            }
        )

    def _extractMessage(self, message):
        return message.choices[0].message.content

    def _getGroqResponse(self, **kwargs):
       return self.llm._getGroqResponse(**kwargs)
    
    def doStep(self, prompt_name, prompt_args, model="llama3-70b-8192", json_mode=True):
        with open(f"./Prompts/{prompt_name}.txt") as f:
            prompt = f.read()

        #format the prompt with the arguments
        prompt = prompt.format(**prompt_args)
        _f = [{
            "role":"system",
            "content":prompt
        }]
        return self._extractMessage(self.llm._getGroqResponse(message_list=_f, model=model, json_mode=json_mode, temperature=0.5))
    
    def chooseStep(self):
        args = {
            "conversation":json.dumps(self.message_list, indent=4)
        }
        summary = self.doStep("summarizer", args)
        try:
            summary = json.loads(summary)
            self.summary = summary
            self.nextStep = summary["nextStep"] 
        except:
            summary = None
    
    def _respondToUser(self, message):
        print("Assistant: ", message)
        self._addMessageToList(message, "assistant")

    def resolveRequirement(self, requirement, message_list, summary):
        if (requirement in self.exact_result_requirement):
            return
        args = {
            "conversation":json.dumps(message_list, indent=4),
            "summary":summary
        }
        key = requirement
        if (key in self.dependencies):
            for d in self.dependencies[key]:
                self.resolveRequirement(d, message_list, summary)
        
            for d in self.dependencies[key]:
                if (d in self.exact_result_requirement):
                    args[d] = self.exact_result_requirement[d]
        
        if (key in self.dbDependencies):
            for d in self.dbDependencies[key]:
                fn_ = d["fn"]
                args_ = [self.exact_result_requirement[arg] for arg in d["args"]]
                _val = fn_(*args_)
                try:
                    args[d["name"]] = "\n ".join(_val)
                except:
                    args[d["name"]] = _val
        output_ = self.doStep(self.finderPromptNames[key], args, model="llama3-70b-8192")
        self.exact_result_requirement[key] = json.loads(output_)[key]
        return
    
    def _summarizeResults(self, results):
        total_seats = 0
        return_summary = False
        for item in results:
            if "Won" in item:
                return_summary = True
                total_seats += item["Won"]
            
        if return_summary:
            _result_summary = {
                "total_seats":total_seats,
            }
            return _result_summary
        else:
            return None


    def loop(self):
        self._greyPrint("CURRENT STEP: ", self.nextStep)
        if self.nextStep == "IntroduceYourself":
            promptForUser = self.doStep("Introducer", {}, json_mode=False)
            self._respondToUser(promptForUser)
            self.nextStep = "GetUserInput"
        elif self.nextStep == "ClarifyUserRequest":
            args = {
                "conversation":json.dumps(self.message_list, indent=4)
            }
            promptForUser = json.loads(self.doStep("Clarifier", args))["promptForUser"]
            self._respondToUser(promptForUser)
            self.nextStep = "GetUserInput"
        elif self.nextStep == "RespondToUser":
            assistant_output = self._extractMessage(self.llm._getGroqResponse(message_list=self.message_list, model="llama3-8b-8192", json_mode=False))
            self._respondToUser(assistant_output)
            self.nextStep = "GetUserInput"
        elif self.nextStep == "GetUserInput":
            _mess = self._getInputFromUser()
            self.nextStep = "ChooseStep"
            return _mess
        elif self.nextStep == "ChooseStep":
            self.chooseStep()
        elif self.nextStep == "UseToolToFindInformationAboutUserQuery":
            #This tool executes the following loop
            #clarify requirement.
            #choose tool to execute
            #tool execution
            #tool response
            _summ = self.summary["summary"]
            self._greyPrint(_summ)
            args = {
                "conversation":json.dumps(self.message_list, indent=4),
                "summary":_summ
            }
            choice = json.loads(self.doStep("InternalClarifier", args))
            for key in choice.keys():
                if (key in self.exact_result_requirement):
                    #we're done for this guy, move on
                    continue
                else:
                    self._greyPrint("RESOLVING REQUIREMENT: ", key)
                    self.resolveRequirement(key, self.message_list, _summ)
                    self._greyPrint(self.exact_result_requirement[key])
            self._greyPrint("EXACT REQUIREMENTS:", self.exact_result_requirement)
            no_values = []
            for key in self.exact_result_requirement:
                if (self.exact_result_requirement[key] == "" or self.exact_result_requirement[key] == None or self.exact_result_requirement[key] == "None"):
                    no_values.append(key)
                    
            if (len(no_values) > 0):
                _a = {
                    "summary":_summ,
                    "no_value_fields":no_values
                }
                response = self.doStep("NoValuesResponder", _a, json_mode=False)
                self._respondToUser(response)
                self.nextStep = "GetUserInput"
            else:
                
                #We have all the values we need.
                #Now lets find a tool to execute.
                args = {
                    "summary":_summ
                }
                for k in self.exact_result_requirement:
                    args[k] = self.exact_result_requirement[k]
                _tool = self.doStep("PrecisionToolFinder", args, model="llama3-70b-8192")
                _tool = json.loads(_tool)["resultFinderTool"]
                self._greyPrint("TOOL: ", _tool)

                #Check whether all the tool's dependencies are satisfied
                self._greyPrint("Resolving additional requirements for tool: ", _tool)
                if (_tool in self.tool_dependencies):
                    for dep in self.tool_dependencies[_tool]:
                        if (dep not in self.exact_result_requirement):
                            self._greyPrint("RESOLVING DEPENDENCY: ", dep)
                            self.resolveRequirement(dep, self.message_list, _summ)
                
                #The tool will generate a query to run.
                _q = self.doStep(_tool, args, model="llama3-70b-8192")
                query = json.loads(_q)["query"]
                self._greyPrint("GENERATED QUERY: \n```sql\n", query, "\n```")
                
                #Execute the query
                result = execute_query(query)
                self._greyPrint("RESULT: ", result)
                result_summary = self._summarizeResults(result)
                result_summary = result_summary if result_summary != None else ""
                
                #Respond to the user
                f_args = {
                    "summary":_summ,
                    "toolName":_tool,
                    "exact_requirements":self.exact_result_requirement,
                    "tool_result":result, 
                    "result_summary":result_summary,
                }

                resp = self.doStep("resultCommunicator", f_args, model="llama3-70b-8192", json_mode=False)
                self._respondToUser(resp)
                self.exact_result_requirement = {}
                self.nextStep = "GetUserInput"
        elif self.nextStep == "InternalClarifier":
            pass
            
            

class SimpleInteractiveAgent(Agent):

    def __init__(self):
        super().__init__()

    def start(self):
        pass


if __name__ == "__main__":
    agent = SimpleInteractiveAgent()
    shouldContinue = True
    while shouldContinue:
        user_message = agent.loop()
        if user_message == "/x":
            shouldContinue = False
            break
        

