prompt_runner_args = {
    "findExactPartyInYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "findExactStateNameInYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "findExactYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "findExactStateOrConstituency": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "getConstituencyResultInYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "getStateResultsSummaryInYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "getFullResultForConstituency": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "getStateResultsWithConstituencyBreakdownInYear": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "Introducer": {
        "temperature":0.5,
        "model":"llama3-8b-8192", 
        "json_mode":True,
    },
    "Clarifier": {
        "temperature":0.5,
        "model":"llama3-70b-8192", 
        "json_mode":True,
    },
    "InternalClarifier": {
        "temperature":0.5,
        "model":"llama3-70b-8192", 
        "json_mode":True,
    },
    "PrecisionToolFinder": {
        "temperature":0.5,
        "model":"llama3-70b-8192", 
        "json_mode":True,
    },
    "resultCommunicator": {
        "temperature":0.5,
        "model":"llama3-70b-8192", 
        "json_mode":True,
    }
}