# to_renderer.py 
Un script pour automatiser des modifications de fichiers. Initialement conçu pour permettre de réappliquer automatiquement des modifications à des fichiers utilisés pour du rendu cartographique.

# Attention 

N'utilisez cet outil que pour modifier des fichiers localement. **N'approchez pas les fichiers générés par cette bibliothèque des api de contribution à OpenStreetMap, les informations de modifications ne sont pas générées !**

# Utilisation
Nécessite les packages pyOsmData et osmxml_routines disponibles ici : https://github.com/JBacc1/pyOsmData

`python to_renderer.py file.osm`

puis récupérer le fichier file_post.osm  
Le script recherchera les fichiers add_tags.txt, delete_tags.txt et offset.txt pour les informations à modifier. Fournir au minimum un fichier vide.  
Structure des fichiers :  
delete_tags.txt : `way 355521590 amenity`  
add_tag.txt : `way 220788521 trail_visibility=bad layer=-1`  
offset.txt : `node 3046370547 10 50` (delta lon,delta lat, en mètres)





# État des lieux

Les exemples détaillés restent à faire.  
Ce script a été utilisé pour la réalisation d'une carte de randonnée autour de Samoëns : [http://randocarto.fr/demo/Samoens_A1_400dpi.png](http://randocarto.fr/demo/Samoens_A1_400dpi.png)