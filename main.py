#!/usr/bin/env python3
import PySimpleGUI as sg
import random
import webbrowser

sg.theme("DarkGreen7")
layout = [[sg.Button("Cum se joaca?")], [sg.Text()], [sg.Image("logo2.png")], [sg.Image("box.png")], [sg.Text()],
		[sg.Button("Joaca", bind_return_key=True, key="IN")]]
window = sg.Window("WORDLE", layout, size=(650, 300), finalize=True, element_justification="center")
window["IN"].set_focus()

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		window.close()
		quit()
	elif event == "Cum se joaca?":
		webbrowser.open('https://mashable.com/article/wordle-word-game-what-is-it-explained')
	elif event == "IN":
		break
window.close()

f=open("cuvinte.txt", "r")
L=f.read()
f.close()
L=L.split("\n")
L=L[:-1]

cuv=L[random.randint(0, 11455)]
guess = None
guesses = []
foundLetters = [0, 0, 0, 0, 0]
nr = 1
usedHint = False

layout = [[sg.Image("logo2.png")], [sg.Text()],
		[sg.Text(f"Guess {nr}"), sg.Input(key="-INPUT-"), sg.Ok(bind_return_key=True)],
		[sg.Button("Renunta")]]
window = sg.Window("WORDLE", layout, finalize=True, modal=True, element_justification="center")
window["-INPUT-"].set_focus()

while True:
	event, values = window.read()
	if event == sg.WIN_CLOSED:
		break
	elif event == "Renunta":
		sg.popup("Imi pare rau. Cuvantul era " + cuv, title=":(")
		break
	elif event == "Hint":
		hint = None
		hintIndex = None
		for i in range(len(cuv)):
			if foundLetters[i] == 0:
				hint = cuv[i]
				hintIndex = i
				break
		sg.Popup("Pe pozitia " + str(hintIndex+1) + " se afla litera " + hint, title="Hint")
		usedHint = True
		continue
	guess = values["-INPUT-"].upper()
	if len(guess) != 5 or not guess.isalpha() or guess not in L:
		sg.Popup("Te rog introdu un cuvant de 5 litere din limba romana.", title="Eroare")
		continue

	status=''
	for index in range(len(guess)):
		if guess[index]==cuv[index]:
			status+="✓"
			foundLetters[index] = 1
		elif guess[index] in cuv:
			status+="↔"
		else:
			status+="❌"
	guesses.append(guess + " - " + status)

	window.close()

	if status == "✓✓✓✓✓":
		window.close()
		layout = [[sg.Text("Ai reusit! Cuvantul era " + cuv + "\nTi-a luat " + str(nr) + " incercari.", font="default 10")],
				[sg.Text()], [sg.Image("happy.gif")]]
		window = sg.Window(title="Uraa!", layout=layout, size=(500, 300), modal=True, element_justification="center")
		event, values = window.read()
		break
	else:
		nr += 1

	layout = [[sg.Text("\n".join(guesses), font="default 12 normal")], [sg.Text()],
			[sg.Text(f"Guess {nr}"), sg.Input(key="-INPUT-"), sg.Ok(bind_return_key=True)],
			[sg.Button("Renunta")]]
	if usedHint == False:
		layout[3].append(sg.Button("Hint"))
	window = sg.Window("WORDLE", layout, modal=True, finalize=True, element_justification="center")
	window["-INPUT-"].set_focus()
window.close()
