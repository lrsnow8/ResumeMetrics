import textAnalysis

print("textAnalysis Imported")

print("results pending...")


#sample id: 1
text = "In a project, our software experienced a critical bug just before launch. I quickly diagnosed the issue, coordinated with the team to implement a fix, and conducted thorough testing overnight. Our prompt action resolved the problem, ensuring a successful launch without delays or quality compromises."

ACTION_VERBS='action_verbs.txt'
action_verbs, lemmatizer = textAnalysis.nlp_spin_up(ACTION_VERBS)


print(textAnalysis.analyze_text(text))

