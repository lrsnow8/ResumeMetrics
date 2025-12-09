import R1V2

print("R1V2 Imported")

print("results pending...")


#sample id: 1
#current issue from initial test: "resolved the problem" does not add to keyword count or precense bc of my regexp implementation, but if you take the prefix out,"action solved the problem", it was counted.
text = "In a project, our software experienced a critical bug just before launch. I quickly diagnosed the issue, coordinated with the team to implement a fix, and conducted thorough testing overnight. Our prompt action resolved the problem, ensuring a successful launch without delays or quality compromises."


print(R1V2.analyze_text(text))

