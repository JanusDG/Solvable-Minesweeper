from constraint import *
problem = Problem()
problem.addVariable("a", [0,1])
problem.addVariable("b", [0,1])
problem.addVariable("c", [0,1])
problem.addVariable("d", [0,1])
problem.addVariable("e", [0,1])
problem.addVariable("f", [0,1])
problem.addVariable("g", [0,1])
problem.addVariable("h", [0,1])
problem.addVariable("i", [0,1])
problem.addVariable("j", [0,1])
# print(problem.getSolutions())


problem.addConstraint(ExactSumConstraint(1), ("a", "b"))
problem.addConstraint(ExactSumConstraint(1), ("a", "b", "c"))
problem.addConstraint(ExactSumConstraint(1), ("c", "d", "e"))
problem.addConstraint(ExactSumConstraint(2), ("d", "e", "f"))
problem.addConstraint(ExactSumConstraint(1), ("e", "f", "g"))
problem.addConstraint(ExactSumConstraint(1), ("g", "h", "i"))
problem.addConstraint(ExactSumConstraint(1), ("h", "i", "j"))
problem.addConstraint(ExactSumConstraint(1), ("i", "j"))
dicts = problem.getSolutions()
for item in dicts:
    print(item)


common = {k: v for k, v in dicts[0].items() if all(d[k] == v for d in dicts)}
print()
print(common)