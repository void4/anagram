from collections import Counter
from random import choice, randint, random

words = []

paths = [
	"google-10000-english.txt",
	"english-adjectives.txt",
	"gerund.txt",
	"verbs.txt",
	"verbs-participle.txt",
]

for path in paths:
	words += open(path).read().splitlines()

print(len(words))

celebrities = open("celebrities.txt").read().splitlines()

def list_difference(l1, l2):
	"""All elements in l1 that are not in l2 (counted)"""
	l1 = sorted(l1)
	l2 = sorted(l2)
	result = []
	for e in l1:
		try:
			index = l2.index(e)
			l2.pop(index)
		except ValueError:
			result.append(e)
			continue

	return result

def list_union(l1, l2):
	"""All elements that are in l1 and l2 (counted)"""
	l1 = sorted(l1)
	l2 = sorted(l2)
	result = []
	for e in l1:
		try:
			index = l2.index(e)
			l2.pop(index)
			result.append(e)
		except ValueError:
			pass

	return result

words = [word.lower() for word in words if len(word)>=4]
words.extend("a an or in i the".split())
for w in "res und fur der ref usr def mrna mtv mls lbs les mel mlb lat rev hrs eur nhs href sur ser usd gen gif cdna".split():
	try:
		words.remove(w)
	except ValueError:
		pass
def find_anagram(name, attempts=5):
	target = name.replace(" ", "").lower()
	sortedtarget = sorted(target)
	cover = []
	scover = []

	attempt = 0
	while scover != sortedtarget:
		delta = list_difference(target, scover)
		possible = [word for word in words if len(word)<=len(delta) and word not in target and len(list_difference(word, delta)) == 0]
		#print(target, cover, scover, delta, possible)

		if len(possible) == 0:
			#print("Break", cover, delta)
			#return
			if len(cover) == 0:
				return

			attempt += 1

			if attempt > attempts:
				return

			popped = cover.pop(randint(0,len(cover)-1))
			scover = list_difference(scover, popped)
			continue

		c = Counter()
		for word in possible:
			letters = len(list_union(delta, list(word)))
			if letters > 0:
				c[word] = letters

		mostcommon = c.most_common(10)
		#print(mostcommon)
		if len(mostcommon) == 0:
			attempts += 1
			cover = []
			scover = []
			continue

		word = choice(mostcommon)[0]

		scover = sorted(scover+list(word))#sorted()
		cover.append(word)

	return cover

def find_name(anagram):
	anagram = sorted(anagram.replace(" ", "").lower())
	for celebrity in celebrities:
		target = sorted(celebrity.replace(" ", "").lower())
		#print(celebrity, target, anagram)
		if target == anagram:
			print("FOUND", celebrity)
			return celebrity


def sortlowerjoin(l):
	return sorted("".join(l).lower())

import sys
from itertools import permutations
if __name__ == "__main__":

	if len(sys.argv) > 1:
		inp = " ".join(sys.argv[2:])
		if sys.argv[1] == "find_name":
			find_name(inp)
		elif sys.argv[1] == "find_anagram":
			print(find_anagram(inp, attempts=1000))
		elif sys.argv[1] == "permute":
			for perm in permutations("".join(sys.argv[2:])):
				print(perm)
		elif sys.argv[1] == "compare":
			split = sys.argv[2:].index("^")
			print(sortlowerjoin(sys.argv[2:2+split]) == sortlowerjoin(sys.argv[2+split+1:]))
		elif sys.argv[1] == "sort":
			print(sortlowerjoin(sys.argv[2:]))
		elif sys.argv[1] == "subtract":
			split = sys.argv[2:].index("^")
			print(list_difference(sortlowerjoin(sys.argv[2:2+split]), sortlowerjoin(sys.argv[2+split+1:])))		
		else:
			raise Exception("Invalid argument")

	else:
		for celebrity in celebrities:#[:100]:
			cover = find_anagram(celebrity)
			if cover:
				print(celebrity, cover)
