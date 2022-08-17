import numpy as np
import random as random
from rotors import *

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def create_rotors(nr_rotors):

	rotors = []
	rotors_used = "\nUsing the following rotor combinations:"
	for i in range(nr_rotors):
		rotor = {}
		random_rotor_combination = random.choice(possible_rotor_combinations)
		rotors_used = rotors_used + "\n" + random_rotor_combination 
		for i in range(len(random_rotor_combination)):
			rotor[alphabet[i]] = random_rotor_combination[i]

		rotors.append(rotor)

	print(rotors_used)
	return rotors

def create_reflector():

	reflector = {}
	reflector_used = "\nUsing the following reflector:\n"
	random_reflector_combination = random.choice(possible_reflector_combinations)
	reflector_used += random_reflector_combination
	for i in range(len(random_reflector_combination)):
		reflector[alphabet[i]] = random_reflector_combination[i]

	print(reflector_used)
	return reflector

def create_random_enigma_setup(nr_rotors):

	plugboard = generate_random_plugboard_combination()
	print("\nUsing the following plugboard: ",plugboard.values())

	rotors = create_rotors(nr_rotors)
	reflector = create_reflector()

	return plugboard, rotors, reflector

def shift_values(rotor):
	combination = list(rotor.values())
	new_combination = np.roll(combination, 1)
	for key, index in zip(rotor.keys(),range(len(rotor))):
		rotor[key] = new_combination[index]

	return rotor

def update_rotors(rotors, rotors_rotation):

	rotors_rotation[0] = rotors_rotation[0] + 1
	rotors[0] = shift_values(rotors[0])
	for i in range(len(rotors_rotation)):		
		if rotors_rotation[i] % len(alphabet) == 0 and rotors_rotation[i] != 0:
			rotors_rotation[i] = 0		
			if i + 1 < len(rotors):
				rotors_rotation[i+1] = rotors_rotation[i+1] + 1
				rotors[i+1] = shift_values(rotors[i+1])
			
	return rotors

def run_rotors(letter, letter_path, rotors, reflector):

	# forward pass
	new_letter = letter
	for j in range(len(rotors)):
		rotor = rotors[j]
		new_letter = rotor[new_letter]
		letter_path = letter_path + " -> " + new_letter

	# reflector pass
	new_letter = reflector[new_letter]
	letter_path = letter_path + " -> " + new_letter

	# backward pass
	for _rotor in reversed(rotors):
		new_letter = list(_rotor.keys())[list(_rotor.values()).index(new_letter)][0]
		letter_path = letter_path + " -> " + new_letter

	return new_letter, letter_path

def run_plugboard(letter, letter_path, plugboard, is_reverse = False):

	if not is_reverse:
		new_letter = plugboard[letter]
		letter_path = letter + " -> " + new_letter
	else: 
		new_letter = list(plugboard.keys())[list(plugboard.values()).index(letter)][0]
		letter_path = letter_path + " -> " + new_letter

	return new_letter, letter_path

def encode_letter(letter, plugboard, rotors, reflector):

	path = ""
	coded_letter, path = run_plugboard(letter, path, plugboard)
	coded_letter, path = run_rotors(coded_letter, path, rotors, reflector)
	coded_letter, path = run_plugboard(coded_letter, path, plugboard, True)
	#print(path)

	return coded_letter

def generate_random_plugboard_combination(nr_pairs = 13):

	plugboard = {}

	free_indexes = np.linspace(0,25,num=26, dtype='int')
	final_combination = np.empty(len(alphabet),dtype='str')

	for i in range(len(final_combination)):
		final_combination[i] = alphabet[i]


	while free_indexes.size != 0 and nr_pairs >= 0:
		nr_pairs = nr_pairs - 1
		index1 = random.choice(free_indexes)
		free_indexes = np.delete(free_indexes, np.where(free_indexes == index1))
		#print('index 1', index1)

		index2 = random.choice(free_indexes)
		free_indexes = np.delete(free_indexes, np.where(free_indexes == index2))
		#print('index 2', index2)

		final_combination[index1] = alphabet[index2]
		final_combination[index2] = alphabet[index1]

	for letter, index in zip(alphabet, range(len(alphabet))):
		plugboard[letter] = final_combination[index]
		
	return plugboard


if __name__ == '__main__':
	nr_rotors = 3
	rotors_rotation = []
	for i in range(nr_rotors):
		rotors_rotation.append(0)

	plugboard, rotors, reflector = create_random_enigma_setup(nr_rotors)

	while True:
		letter = input("Type letter to encode. (Input empty letter to exit) :\n")
		if letter == "":
			exit()
		else:
			letter = letter.upper()
			letter = encode_letter(letter, plugboard, rotors, reflector)
			rotors = update_rotors(rotors, rotors_rotation)
			print("Coded letter: ", letter) 