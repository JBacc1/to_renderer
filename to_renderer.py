# -*- coding: utf-8 -*-
# Code par JB (https://www.openstreetmap.org/user/JBacc1) sous licence FTWPL (Licence publique + non responsabilité)

import math
import sys
import os.path
from osmdata import *

dtag_list_file='delete_tags.txt'
atag_list_file='add_tags.txt'
offset_file='offset.txt'

verbose=True

try : in_file=sys.argv[1]
except: 
	print("Usage : python to_renderer.py infile.osm")
	sys.exit()


def read_offset(filename):
	offset_dict={}
	with open(filename,"r",encoding='utf-8') as file:
		for ligne in file:
			if len(ligne.strip())>0:
				if ligne.strip()[0]!="#":
					t=ligne.strip("\n ").split()
					try:
						id=int(t[1])
						if t[0]=="node": 
							x,y=float(t[2]),float(t[3])
							offset_dict[id]=(x,y)
						else: print("("+filename+")Ligne non traitée (type d'objet non pris en charge) : "+ligne.strip("\n"))
					except:
						print("("+filename+")Ligne non traitée (identifiant non entier ou offset non décimal) : "+ligne.strip("\n"))
	return offset_dict
def read_tag_file(filename):
	lnodes,lways,lrels={},{},{}
	with open(filename,"r",encoding='utf-8') as file:
		for ligne in file:
			if len(ligne.strip())>0:
				if ligne.strip()[0]!="#":
					t=ligne.strip("\n ").split(" ")
	#				print(t)
					try:
						id=int(t[1])
						if t[0]=="node": lnodes[id]=t[2:]
						elif t[0]=="way": lways[id]=t[2:]
						elif t[0]=="rel" or t[0]=="relation": lrels[id]=t[2:]
						else: print("("+filename+")Ligne non traitée (type d'objet non défini) : "+ligne.strip("\n"))
					except:
						print("("+filename+")Ligne non traitée (identifiant non entier) : "+ligne.strip("\n"))
#				else: print("("+filename+")Ligne non traitée (commentaire) : "+ligne.strip("\n"))
	return (lnodes,lways,lrels)
	
def node_set_tags(node,tag_list):
	for tag in tag_list:
		node.set_tag(tag[0],tag[1])
def get_kv_from_string(t):
	kv=t.split('=')
	if len(kv)!=2: 
		print('tag ignoré, mal conditionné en "key=value" : "'+t+'"')
		raise ValueError("Tag mal conditionné")
	else: 
		if kv[0]=="name": kv[1]=kv[1].replace("_"," ")
		return kv[0],kv[1]
		
print("Script to_renderer.py de JB (https://www.openstreetmap.org/user/JBacc1) sous licence FTWPL (licence publique + non responsabilité")

print('Chargement du fichier : '+in_file)
osm = OsmData()
osm.load_xml_file(in_file)
osm.upload="never"
	

i=0	
##1ère partie : modifie les tags 
print("Modification de tags")
(dnodes,dways,drelations)=read_tag_file(dtag_list_file)
(anodes,aways,arelations)=read_tag_file(atag_list_file)

for id in list(dnodes.keys()):
	if osm.has_node(id):
		for key in dnodes[id]:
			osm.node(id).remove_tag(key)
	elif verbose: print("add_tag : node absent : "+str(id))
for id in list(dways.keys()):
	if osm.has_way(id):
		for key in dways[id]:
			osm.way(id).remove_tag(key)
	elif verbose: print("add_tag : way absent : "+str(id))
for id in list(drelations.keys()):
	if osm.has_relation(id):
		for key in drelations[id]:
			osm.relation(id).remove_tag(key)		
	elif verbose: print("add_tag : relation absente : "+str(id))

for id in list(anodes.keys()):
	if osm.has_node(id):
		for tag in anodes[id]:
			kv=get_kv_from_string(tag)
			osm.node(id).set_tag(kv[0],kv[1])
	elif verbose: print("delete_tag : node absent : "+str(id))
for id in list(aways.keys()):
	if osm.has_way(id):
		for tag in aways[id]:
			kv=get_kv_from_string(tag)
			osm.way(id).set_tag(kv[0],kv[1])
	elif verbose: print("delete_tag : way absent : "+str(id))
for id in list(arelations.keys()):
	if osm.has_relation(id):
		for tag in arelations[id]:
			kv=get_kv_from_string(tag)
			osm.relation(id).set_tag(kv[0],kv[1])
	elif verbose: print("delete_tag : relation absente : "+str(id))

###2ème partie : décale les points demandés
print("Décalage des noeuds spécifiés")
offset_dict=read_offset(offset_file)
for id in list(offset_dict.keys()):
	if osm.has_node(id):
		osm.node(id).location.offset_meters(offset_dict[id][0],offset_dict[id][1])
	elif verbose: print("offset_node : node absent : "+str(id))

	
print('Sauvegarde du fichier : '+in_file.replace('.osm','')+"_post.osm")
osm.save_xml_file(in_file.replace('.osm','')+"_post.osm")
print("OK")
