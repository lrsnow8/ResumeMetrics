import re
import pandas as pd
import textstat
from language_tool_python import LanguageTool

#this can be imported or run as a script with the file hardcoded within the main at the bottom

"""
analyze_text(text) - runs all and returns a dict of all the metrics for a given string
analyze_dataframe(df,text_col,id_col) - runs all and outputs a df with the id and a column for each metric

count_words - counts the words, returns int
count_characters - counts characters, returns, int
keyword_presence - checks for problem solving or some variation of that along with skill or analytic, returns boolean
keyword_count - sum of keywords checked for in keyword_presence, returns int
keyword_ratio - ratio of keyword_count to count_words, return float
flesch_reading_ease - FRE score from textstat, returns float
gunning_fog - GF score from textstat, returns float
dale_chall - DC score from textstat, returns float
ari_score - ARI score from textstat, returns float
grammar_errors - finds grammar errors with LanguageTool from language_tool_python, returns sum of errors as int
grammar_score - score for grammer = (count_words - grammar_errors)/ count_words, so higher is better, 1.0 is max
action_verb_count - counts action verbs from a hardcoded list of actions verbs, returns a int
"""



#EFFORT METRICS (Mousavi)

def count_words(text):
    #M1: Count number of words
    if not text or pd.isna(text):
        return 0
    return len(text.split())


def count_characters(text):
    #M2: Count number of characters
    if not text or pd.isna(text):
        return 0
    return len(text)


#(Abraham & Burbano)

def keyword_presence(text):

    #Check if keywords are present (1=yes, 0=no)
    

    if not text or pd.isna(text):
        return 0

    text_lower = text.lower()

    # Check for problem+solv* within 3 words
    problem_solving = r'\bproblem\b(?:\s+\S+){0,3}\s+\bsolv\w*\b|\bsolv\w*\b(?:\s+\S+){0,3}\s+\bproblem\b'

    # Check for skill* and analytic*
    skill = r'\bskill\w*\b'
    analytic = r'\banalytic\w*\b'

    if re.search(problem_solving, text_lower) or re.search(skill, text_lower) or re.search(analytic, text_lower):
        return 1
    return 0


def keyword_count(text):
    #count total keyword occurances
    if not text or pd.isna(text):
        return 0

    text_lower = text.lower()
    count = 0


    #count the problem solve combination
    problem_solving = r'\bproblem\b(?:\s+\S+){0,3}\s+\bsolv\w*\b|\bsolv\w*\b(?:\s+\S+){0,3}\s+\bproblem\b'
    count += len(re.findall(problem_solving, text_lower))

    # Count skill and analytic
    count += len(re.findall(r'\bskill\w*\b', text_lower))
    count += len(re.findall(r'\banalytic\w*\b', text_lower))

    return count


def keyword_ratio(text):
    #Ratio of keywords to total words
    words = count_words(text)
    if words == 0:
        return 0.0
    return keyword_count(text) / words


#(Mousavi,Yang)
#TODO inverse FRE score and normalize all three scores from 0-1
def flesch_reading_ease(text):
    #Flesch Reading Ease score
    if not text or pd.isna(text) or len(text.strip()) == 0:
        return 0.0
    try:
        return textstat.flesch_reading_ease(text)
    except:
        return 0.0


def gunning_fog(text):
    #Gunning-Fog Index
    if not text or pd.isna(text) or len(text.strip()) == 0:
        return 0.0
    try:
        return textstat.gunning_fog(text)
    except:
        return 0.0


def dale_chall(text):
    #M1: Dale-Chall Readability Score
    if not text or pd.isna(text) or len(text.strip()) == 0:
        return 0.0
    try:
        return textstat.dale_chall_readability_score(text)
    except:
        return 0.0


def ari_score(text):
    
    #just gets the ari for a given cell

    if not text or pd.isna(text) or len(text.strip()) == 0:
        return 0.0
    try:
        return textstat.automated_readability_index(text)
    except:
        return 0.0


#(Sajjadiani)

# this grammar_tool setup does not make sense to me but it works
_grammar_tool = None

def get_grammar_tool():
    #lazy initialization of grammar tool
    global _grammar_tool
    if _grammar_tool is None:
        _grammar_tool = LanguageTool('en-US')
    return _grammar_tool


def grammar_errors(text):
    #M1: count grammar or spell error
    if not text or pd.isna(text) or len(text.strip()) == 0:
        return 0
    try:
        tool = get_grammar_tool()
        matches = tool.check(text)
        return len(matches)
    except:
        return 0


def grammar_score(text):
    #M1: Reverse coded, words - errors, higher better
    errors = grammar_errors(text)
    words = count_words(text)
    score = (words - errors)/words
    return score



# list of resume action words

# found this other implementation, could maybe work but might explode the compute time to be unrealistic for a large amount of text 
# https://stackoverflow.com/questions/62979191/a-way-to-find-action-verb-cognition-verb-stative-verb-and-trigger-words-using
ACTION_VERBS = {
    'achieved', 'adapted', 'administered', 'analyzed', 'applied',
    'approved', 'arranged', 'assembled', 'assessed', 'assisted',
    'built', 'calculated', 'clarified', 'coached', 'collected',
    'communicated', 'completed', 'conducted', 'coordinated', 'created',
    'delivered', 'demonstrated', 'designed', 'developed', 'devised',
    'directed', 'discovered', 'drafted', 'edited', 'educated',
    'eliminated', 'enabled', 'encouraged', 'engineered', 'enhanced',
    'established', 'evaluated', 'examined', 'exceeded', 'executed',
    'expanded', 'facilitated', 'focused', 'formulated', 'generated',
    'guided', 'hired', 'identified', 'illustrated', 'implemented',
    'improved', 'increased', 'influenced', 'initiated', 'innovated',
    'inspected', 'installed', 'instructed', 'integrated', 'introduced',
    'investigated', 'launched', 'led', 'maintained', 'managed',
    'marketed', 'maximized', 'measured', 'mentored', 'minimized',
    'modified', 'monitored', 'motivated', 'negotiated', 'operated',
    'optimized', 'organized', 'originated', 'oversaw', 'performed',
    'persuaded', 'pioneered', 'planned', 'prepared', 'presented',
    'prioritized', 'processed', 'produced', 'programmed', 'promoted',
    'proposed', 'provided', 'published', 'recommended', 'recorded',
    'recruited', 'redesigned', 'reduced', 'refined', 'regulated',
    'reorganized', 'repaired', 'replaced', 'reported', 'represented',
    'researched', 'resolved', 'restored', 'restructured', 'reviewed',
    'revised', 'saved', 'scheduled', 'screened', 'secured',
    'selected', 'served', 'simplified', 'solved', 'spearheaded',
    'standardized', 'streamlined', 'strengthened', 'structured', 'studied',
    'supervised', 'supported', 'tested', 'tracked', 'trained',
    'transformed', 'updated', 'upgraded', 'utilized', 'validated',
    'verified', 'wrote'
}


def action_verb_count(text):
    #count action verbs
    if not text or pd.isna(text):
        return 0

    words = re.findall(r'\b\w+\b', text.lower())
    #holy return statement
    return sum(1 for word in words if word in ACTION_VERBS)


#MAIN STUFF

def analyze_text(text):
#return all the things in a dict for a single block of text
    return {
        # Effort metrics
        'word_count': count_words(text),
        'char_count': count_characters(text),

        # Keyword matching
        'keyword_presence': keyword_presence(text),
        'keyword_count': keyword_count(text),
        'keyword_ratio': keyword_ratio(text),

        # Readability
        'FRE_score': flesch_reading_ease(text),
        'GF_score': gunning_fog(text),
        'DC_score': dale_chall(text),
        'ARI_score': ari_score(text),

        # Spelling and grammar
        'grammar_errors': grammar_errors(text),
        'grammar_score': grammar_score(text),

        # Action verbs
        'action_verbs_count': action_verb_count(text)
    }


def analyze_dataframe(df, text_col='SKILLS', id_col='ID'):
    
    #analyze all texts in df
    #args: id column and text_col 
    #returns: DataFrame with ID and all metrics, the metrics are all in a single dict within the df for an ID
    
    results = []

    for _, row in df.iterrows():
        metrics = analyze_text(row[text_col])
        metrics[id_col] = row[id_col]
        results.append(metrics)

    #result dataframe with ID first
    results_df = pd.DataFrame(results)
    cols = [id_col] + [col for col in results_df.columns if col != id_col]
    return results_df[cols]


#usage as script

if __name__ == "__main__":
    try:
        #name of excel file goes here (mine was weird bc of linux) or path to file if not in folder
        df = pd.read_excel('1 SkillsResponses_Sample.xlsx')
        print(f"loaded {len(df)} responses")

        results = analyze_dataframe(df)
        print(f"analysis done")

        print("\nhead of result df")
        print(results.head())

        # Save results, change the name to specify
        results.to_excel('R1V2Results.xlsx', index=False)
        print("\nsaved as: R1V2Results.xlsx")

    except FileNotFoundError:
        print("Excel file not found")
    except Exception as e:
        print(f"Error: {e}")
