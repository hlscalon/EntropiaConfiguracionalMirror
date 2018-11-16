import sys
import boost_graph as bg
import matplotlib.pyplot as plt
import os

from datetime import datetime
from measurement import Measurement
from ase import Atom
from ase.io import read
from ase.data import covalent_radii
from ase.geometry import is_orthorhombic
from ase.visualize import view
from math import log
from operator import itemgetter
from random import uniform
from numpy import asarray
from numpy.polynomial.polynomial import polyfit

def run(configurationEntropy, m, n, c):
	H_n, H1n = configurationEntropy.calculate(m, n, c)
	return H_n, H1n

def getMaxMinSlabArray(slab):
	(dmin, dmax) = (
		[float("Inf"), float("Inf"), float("Inf")],  # x, y, z
		[-float("Inf"), -float("Inf"), -float("Inf")]   # x, y, z
	)

	positions = slab.get_positions(wrap=True) # wrap atoms back to simulation cell
	for distance in positions:
		for idx, d in enumerate(distance):
			if (d > dmax[idx]):
				dmax[idx] = d
			if (d < dmin[idx]):
				dmin[idx] = d

	return (asarray(dmin), asarray(dmax))

def generateGraphFromSlab(slab, covalent_radii_cut_off):
	graph = bg.Graph()

	atomic_numbers = slab.get_atomic_numbers()
	all_distances = slab.get_all_distances(mic=True)
	for atom1, distances in enumerate(all_distances):
		if not graph.has_node(atom1):
			graph.add_node(atom1) # add nodes not bonded

		atom1_cr = covalent_radii[atomic_numbers[atom1]]
		for atom2, distance in enumerate(distances):
			if atom1 != atom2:
				atom2_cr = covalent_radii[atomic_numbers[atom2]]
				# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
				if (distance < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
					graph.add_edge(atom1, atom2)

	return graph

def generateGraphFromSlabVinkFile(slab, covalent_radii_cut_off):
	all_distances = slab.get_all_distances(mic=True)
	atomic_numbers = slab.get_atomic_numbers()

	# so funciona se os atomos Si vierem antes dos de O (numeracao / aboria / grafo)

	mapping = {}
	for atom1, distances in enumerate(all_distances):
		if atomic_numbers[atom1] == 14: # Si
			atom1_cr = covalent_radii[atomic_numbers[atom1]]
			for atom2, distance in enumerate(distances):
				if atom1 == atom2:
					continue

				# so pega atomos de O
				if atomic_numbers[atom2] != 8: # O
					continue

				atom2_cr = covalent_radii[atomic_numbers[atom2]]
				# if the distance between two atoms is less than the sum of their covalent radii, they are considered bonded.
				if (distance < ((atom1_cr + atom2_cr) * covalent_radii_cut_off)):
					try:
						mapping[atom1].append(atom2)
					except KeyError:
						mapping[atom1] = []
						mapping[atom1].append(atom2)

					try:
						mapping[atom2].append(atom1)
					except KeyError:
						mapping[atom2] = []
						mapping[atom2].append(atom1)

	graph = bg.Graph()
	for atom1 in slab:
		if atom1.symbol == 'Si':
			if not graph.has_node(atom1.index):
				graph.add_node(atom1.index) # add nodes not bonded

			try:
				for n1_o in mapping[atom1.index]:
					if atomic_numbers[n1_o] == 8: # O
						for n2_si in mapping[n1_o]:
							if atomic_numbers[n2_si] == 14: # Si
								if atom1.index != n2_si:
									graph.add_edge(atom1.index, n2_si)
			except KeyError:
				pass

	# remove O atomos
	del slab[[atom.index for atom in slab if atom.symbol == 'O']]

	return graph

def calculateHcn(H_n_values, c):
	xy_polyfit = []
	Hc_n_values = []
	for n, H_n, H1n, consider in H_n_values:
		H1nDiv = 0.0
		if H_n > 0:
			H1nDiv = H1n / H_n

		H_n_extrapolated = H_n + (c * H1nDiv)
		g_n = 2 * log(n) # (spatial_dimensions - 1)
		Hc_n = H_n_extrapolated - g_n

		Hc_n_values.append((n, Hc_n))
		if consider == 'Y':
			if H1n > (H_n / 100):
				print("n: %d. H1(n) exceeds 1%% of H(n). Not a valid measurement." % n)
			else:
				xy_polyfit.append((n, Hc_n))

	return (Hc_n_values, xy_polyfit)

def calculateConfigurationalEntropy(n1, n2, H_n_values, c, calculate):
	Hc_n_values, xy_polyfit = calculateHcn(H_n_values, c)

	(x_p, y_p) = zip(*xy_polyfit)
	x_p = asarray(x_p)
	y_p = asarray(y_p)

	# straight line fit
	b, configurational_entropy = polyfit(x_p, y_p, 1) # configurational_entropy equals the slope of the line
	x, y = zip(*Hc_n_values)

	# dados grafico
	# date_now = datetime.now()
	# dados = "graficos/dados/grafico_" + str(date_now.day) + "_" + str(date_now.month) + "_" + str(date_now.year) + "_" + str(date_now.hour) + "_" + str(date_now.minute) + "_" + str(date_now.second) + ".data"
	# dirname = os.path.dirname(dados)
	# if not os.path.exists(dirname):
	# 	os.makedirs(dirname)
	# with open(dados, "w+") as file:
	# 	for x_y in Hc_n_values:
	# 		file.write(str(x_y[0]) + "\t" + str(x_y[1]) + "\n")

	if calculate == 'Y':
		plt.plot(x_p, b + configurational_entropy * x_p, '-')
		plt.scatter(x, y)
		plt.axis([n1, n2, -3, 10])
		plt.show()

	print("Estimated configurational entropy = %f" % (configurational_entropy))

def getNumberRandomPositions(n, total_nodes):
	return n * n * total_nodes

def startMeasurement(filepath, file_type, covalent_radii_cut_off, c, n1, n2, calculate):
	if n1 > n2:
		print("Final m cannot be smaller than initial m")
		return

	print("Starting script...")

	slab = read(filepath)

	total_particles = len(slab)

	print("Slab %s read with success. Total particles %d" % (filepath, total_particles))

	print("Creating graph...")

	if file_type == 'V':
		G = generateGraphFromSlabVinkFile(slab, covalent_radii_cut_off)
	else:
		G = generateGraphFromSlab(slab, covalent_radii_cut_off)

	total_nodes = G.get_total_nodes()
	if total_nodes == 0 or G.get_total_edges() == 0:
		print("No edges found in graph. Check covalent_radii_cut_off")
		return

	print("Graph created with success. Nodes found: %d" % total_nodes)

	cell = slab.get_cell()

	# somente para celulas ortogonais
	if not is_orthorhombic(cell):
		print("Unit cell is not orthorhombic")
		return

	measurement = Measurement()
	measurement.fromFile(filepath, covalent_radii_cut_off, c, n1, n2)
	measurement.createFile()

	(pbcX, pbcY, pbcZ) = slab.get_pbc()
	(dmin, dmax) = getMaxMinSlabArray(slab)
	maxM = getNumberRandomPositions(n2 - 1, total_particles)

	configurationalEntropy = bg.ConfigurationalEntropy(G, 3, len(slab), pbcX, pbcY, pbcZ, maxM)
	configurationalEntropy.add_positions(slab.get_positions(wrap=True))

	print("Generating random positions...")

	configurationalEntropy.init_search(0, cell[0][0], 0, cell[1][1], 0, cell[2][2], n2 -1, maxM, dmin, dmax)

	print("Random positions generated.")

	H_n_values = []
	for n in range(n1, n2):
		measurement.start()

		m = getNumberRandomPositions(n, total_particles)
		H_n, H1n = run(configurationalEntropy, m, n, c)

		measurement.writeResult(n, m, H_n, H1n)
		measurement.end()

		H_n_values.append((n, H_n, H1n, "Y"))

	calculateConfigurationalEntropy(n1, n2, H_n_values, c, calculate)

	print("Program ended correctly")
