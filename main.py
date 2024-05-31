import wolframalpha
import wikipedia
import re

# Wikipedia search function
def search_wiki(keyword=''):
    try:
        search_results = wikipedia.search(keyword)
        if not search_results:
            message = "Sorry, no result from Wikipedia. Try again."
            return message
        else:
            page = wikipedia.page(search_results[0])
            wiki_summary = page.summary.encode('utf-8').decode('utf-8')
            return wiki_summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Ambiguous search term. Try to be more specific. Options: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Page not found in Wikipedia."

# Wolframalpha search function
def search(text=''):
    try:
        res = client.query(text)
        if res['@success'] == 'false':
            return search_wiki(text)
        else:
            pod1 = res['pod'][1]
            if ('definition' in pod1['@title'].lower()) or ('result' in pod1['@title'].lower()) or (
                    pod1.get('@primary', 'false') == 'true'):
                return resolve_list_or_dict(pod1['subpod'])
            else:
                question = resolve_list_or_dict(res['pod'][0]['subpod'])
                question = question.split('(')[0]
                return search_wiki(question)
    except Exception as e:
        return str(e)

# Resolve list or dictionary
def resolve_list_or_dict(variable):
    if isinstance(variable, list):
        return variable[0]['plaintext']
    else:
        return variable['plaintext']

# Bot activity function
def activity(data, context):
    if re.search(r"(hello|hi|hey).*", data):
        return "Hello! How can I assist you today?", context
    elif re.search(r"how are you.*", data):
        return "I'm just a bot, but I'm doing fine! How about you?", context
    elif re.search(r"(.*) your name(.*)", data):
        return "I'm Wiki-Bandaara. Nice to meet you!", context
    elif re.search(r"(.*) help(.*)", data):
        return "I can provide information from Wikipedia or answer questions using Wolfram|Alpha. Feel free to ask anything!", context
    elif re.search(r"(.*) in wikipedia(.*)", data) or re.search(r"(.*) from wikipedia(.*)", data):
        result = search_wiki(data)
        return result, context
    elif re.search(r"stop|bye|quit", data):
        return 'Bot: Bye\nListening stopped', context
    else:
        result = search(data)
        return result, context

# Text response function
def response(data):
    print('Bot:', data)

# Main
appId = '7TVG5H-XEQEL89L86'
client = wolframalpha.Client(appId)

greet = "Hi there, what can I do for you?"
response(greet)

# Initialize conversation context
context = {}

# Loop until listening is False
listening = True
while listening:
    user_input = input('User: ').lower()
    if user_input:
        result, context = activity(user_input, context)
        response(result)
        if result.startswith('Bot: Bye'):
            break
    else:
        message = "Please try again."
        response(message)
