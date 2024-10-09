
# 10-min speech plan

- Brenno - Motivation et recherche de stage
- Snellium - Présentation de société
	- Histoire:
		- projet spin-off de l'ULB
		- start up depuis 2021
		- 6 employés et des étudiants en stage
	- Business:
		- B2B
		- R&D on optical solutions
		- Mise en valeur de leur technologie
		- Industrie et marché
			- Verres
			- Un compétiteur direct
	- Technologie: Promethee
		- Deflectometrie
		- Project d'un pattern
		- Acquisition d'image avec des multiples caméras
		- Reconstruction de l'image en 3D
		- Comparaison avec le modèle CAD
		- Avantages:
			- Bon marché
			- Facile à entretenir
			- Plus rapide
			- Solution conventionnel
				- Système de pistons mécaniques
				- Gabarits
				- Résistances mécanique
- Projet : Unité de contrôle pour les caméras
	- Processus d'acquisition d'image
		- Interaction avec le logiciel
		- Déclenchement simultané des cameras
	- Exigences
		- Formel and documenté
		- Supporte des fonctionnalités futures
		- Application industrielle
	- Représentation du projet dans l'environnement de la société:
		- Acquisition d'image automatisée
		- Base d'interaction avec microcontrôleur

# Questions

> Quel est le produit initial de Snellium et qu'est qu'ils proposent d'autre ?

Promethée est leur produit initial et le principal produit qu'ils mettent en valeur à leur clients. Ils ont d'autres produits secondaires comme le MTF qui calcule et fournit les propriétés optiques des verres et ils fournissent également d'études d'application pour des projets secondaires.

> Pourquoi j'ai choisi Snellium ?

Parce que un de leur projet s’alignait avec mes objectifs de trouver un stage dans mon domaine d'étude, les systèmes embarqués. Lors de vites échanges avec le maître de stage, Vincent, nous avons aboutit à un énoncé de projet qui bénéficiait les deux parties.

> En quel mesure ton projet est important et ne pas réalisé en quelques semaines?

D'abord, mon projet a changé d'énoncé vers la moitié de celui-ci. Avant, je devais tout simplement faire un système qui activait simultanément les caméras sous interaction d'un logiciel sur ordinateur. Une fois le prototype réalisé, l'énoncé devient l'intégration de ce logiciel dans l'architecture courante et aussi, l'adaptation de cette architecture pour faciliter l'implémentation des nouveaux éléments dans l'avenir.

En effet, mon projet est et a été réalisé en question d'un mois. Par contre, l'étude, l'analyse et l'intégration de mon code dans leur logiciel a été la partie la plus onéreuse à effectuer. Apporter des modifications dans un produit qui est développé est sensible et mérite beaucoup plus d'attention.

![Technology Readiness Level](img/technology_readiness_level.jpg)
Indeed, chez Snellium je travaille sur un produit de niveau de maturité technologique 6 ou 7. Apporter des changements à des systèmes à ce niveau de maturité est une tâche extrêmement ardue et m'a pris beaucoup de temps.

> Quels sont tes qualités et défauts?

J'était engagé et motivé pour bien faire mon projet. J'avais de l'autonomie en ce qui concerne le point de vue technique. Par contre, j'ai souffert d'un manque de confiance pour prendre des décisions et un manque de gestion du temps. En effet, plusieurs fois j'ai du recommencer mon travail parce que je ne savais pas me décider et je n'avais pas une vision claire de ce que je voulais faire avant de commencer à programmer. La gestion du temps a aussi était un problème car au départ, j'avance de tâche en tâche, sans me soucier de ce qui venait par la suite car j'ai pensé que j'avais beaucoup de temps. Vers la moitié du stage, quand j'ai finalement établi un planning, j'ai pu remarquer que les temps était court et que je devrais me dépêcher. À ce moment là, j'ai mis en place une stratégie par semaine où chaque début de semaine j'ai listé les tâches qui doivent absolument être finies pour cette semaine et chaque jour j'ai revisité cette liste et j'ai essayé de maintenir un rythme régulier.

> Quels sont les outils mise en place pour assurer la qualité du code ?

Les ingénieurs de Snellium doivent respecter une convention de style de programmation pour assurer l'uniformité du code. Egalement, une fois une partie du code prêt, ce code passe par une révision détaillé via Merge Requests on GitLab. C'était la première fois que je travaille avec ce genre d'outil et cela m'a permis à être plus consistent et corriger certaines erreurs que mon superviseur ait pu retrouver. En dernier, tout git push vers le repositoire en remote passe par une pipeline de test et verification qui test à la fois le style, la compilation et la bonne exécution des tests unitaires. Chaque module du logiciel possède sa propre collection de test unitaire ce qui permet l'exactiture fonctionnelle de l'ensemble du code.

> Comment est structuré la relation entre les étudiants et les employés ?

Une fois par jour nous faisons un Stand-Up Meeting pour présenter nos avancements et nos tâches pour la journée. Après cela, nous nous communiquons surtout avec Vincent, qui est le directeur technique en logiciel pour trancher certaines décisions et demander des directions. 
L'environnement dans le bureau est calme parce que chaque ingénieur est responsable de son projet et les projets sont assez spécifiques pour stimuler de la collaboration. Cependant, ce n'est pas toujours le cas car certains projets sont reliés et ont besoin de l'avancement un de l'autre.


# Feedback

- Présentation a été courte (7min et quelques) et manqué d'un fil conducteur.
	- Manque de profondeur et d'analyse dans les fait enoncés
		- Analyse en ce que cela m'apprend
- Présentation de la société n'était pas clair
	- Le marché et le produit n'est pas bien présenté 
	- Manque de précision dans ce qui Snellium vend et leur type de business
- Présentation du projet
	- Il manque l'évidence du côté **intégration logiciel** qui est la partie la plus difficile et celle qui me coûte le plus de temps.
		- Je n'ai pas du temps mis cela en évidence et mon projet semblait trop simple et facile
- Manque d'accroche et d'éléments pour rendre la présentation plus intéressante
- Il manque des aspects personnels
	- Je me suis concentré à dire ce qui est et ce qui j'ai fait mais pas trop pourquoi et comment cela me fait un meilleur ingénieur.
	- Il a manqué montrer que j'ai évolué en faisant ce stage
	- Les éléments étaient présents mais il a manqué de la profondeur et d'insistance sur certains points.
- La structure étaient bordélique car je suivais mon bullet point sans pas trop réfléchir à ce que je disais et surtout à comment je le disais.
	- Il manque un fil conducteur
	- les leçons apprises personnelles
	- les premières fois
	- en quoi l'unif a aidé et en quoi l'environnement professionnel est différent à l'unif
	- mes solutions étaient un peu naïves et manquait d'analyse
	- "j'ai l'impression de..."
- Conclusion : + personnelle
	- en quoi ce stage t'aide à comprendre ta future carrière
	- que j'ai appris sur la carrière, sur l'environnement professionnel, sur moi-même

- Il faut penser que les profs sont des recruteurs à que je suis en train de parler de mon stage et qui doivent m'engager.
	- Je dois rendre le sujet intéressant et me mettre en valeur 
	- C'était un peu trop scolaire et superficiel 
	- selon mes professeurs, je ne passe pas ce test.

- **Portfolio:** Bon
	- mais il faut m'attarder plus sur le côté non technique et être plus personnel
	- mon stage a aidé à appréhender sur certains points
	- éviter les anecdotes sauf si cela justifient un point
	- Ajouter du concret 

- Je dois soumettre la version finale de mon portfolio pour la semaine après la fin de mon stage
- Quitin me propose une collaboration régulière pour la rédaction de mon résumé de stage pour me guider.
	- Je dois entrer en contact avec lui pour que l'on mettre en place

Les dates de l'évaluation finale sera publiée prochainement mais ils estiment soit le 25/11 ou le 19/12.


## Feedback du superviseur

- Manque d'analyse et de réflexion dans les solutions proposées.
	- Penser à l'impact,l'extensibilité (scalability) et l'implementation  des mes choix avant de me plonger dans la programmation
	- Je dois mieux préparer ma solution avant de me plonger dans son implémentation.

Sinon tout se passe bien.

### Auto-évaluation vs Evaluation du superviseur

Je vais discuter ici les points qui ont les plus d'écart entre l'evaluation de mon superviseur et mon auto-évaluation.

**Personal:**
![Personal Evaluation](img/IPE_personal.jpeg)
Le deuxième point parle de la gestion de projet et du temps.
- En effet, ce projet n'a pas de contrainte de temps défini. Ce serait utile mais pas indispensable car le système actuel fonction mais est lent. 
- J'ai noté Strongly Agree parce que malgré le fait que je ne fais pas de gestion à long terme, j'ai planifié ma semaine personnellement et j'avançais en définissant des tâches au fur et à mesure. 
- En effet, ce n'est pas l'optimal et j'étais un peu trop optimiste en mettant Strongly agree.

Le cinquième point parle d'auto-évaluer la performance et faire des efforts en conséquence.
- Tous les deux nous sommes d'accord que je n'ai pas trop évaluer de manière assidue et exhaustive mes performances.

En général, je pense que j'ai tendance à sous-estimer ma performance personnelle.


**Team:**

![Team Evaluation](img/IPE_team.jpeg)

Ce domaine contient le plus de désaccord entre moi et mon superviseur. En général, il m'évalue de manière positive au sein de l'équipe alors que moi, je m'évalue de manière négative.
Nos points principaux de désaccord sont:
- _"Makes the appropriate efforts to be integrated ..."_
	- Personnellement, je ne trouve pas que je suis mal intégré mais je trouve que j'aurais pu apporter plus d'effort pour être mieux intégrer. Je sens qu'il m'a manqué de courage pour parler plus surtout pour connaître les gens autour de moi.
- _"Tailors the content of oral and written communication to the audience appropriately,..._
	- Je n'ai pas senti que j'ai fait l'effort nécessaire pour me faire comprendre. Des fois j'avais du mal à communiquer mes propos et comment cela affecte mon projet. 
- _"Relates to colleagues and stakeholders with empathy and curiosity..."_
	- Par la même raison du premier point, je sens que par manque de courage ou par timidité, je me suis un peu trop fermé et que je n'ai pas trop osé parler et m’intéresser à ceux présent.

**Outcomes:**
![Outcomes Evaluation](img/IPE_outcomes.jpeg)

Dans ce domaine, nous avons été plus ou moins d'accord à l'exception du dernier point:
_"Analyses how a given task or project impacts the larger mission or purpose of the organisation"_
- À vrai dire, je ne me souviens pas pourquoi je me suis évalué aussi bas car je comprends les enjeux que mon projet vise à résoudre.
- Je pense que j'ai peut-être manqué d'analyse dans ce que je faisais, car je fais mes tâches à la volée. Par contre, on relisant cela maintenant, je vois que ce n'est pas ce qui était demandé.

**Global Evaluation and Strengths:

![Global Evaluation and Strengths](img/IPE_global_strength.jpeg)
Nous sommes d'accord sur l'évaluation globale ce qui ne m'étonnes pas car je trouve que j'effectue un bon boulot et j'accomplis ce qui m'est demandé avec autonomie, efficacité et qualité.

_Points forts_:
- Le point en commun entre mon analyse et celle de mon superviseur est l'autonomie. Je suis quelqu'un à qui on donne une tâche et je fais ce que je peux pour l'accomplir sans devoir revenir demander des précisions ou des aides pour avancer. Je sais me débrouiller tout seul et ainsi, j'avance sur le projet.

**Improvement Points and Goals:**

![Improvement Points and Goals](img/IPE_improvements_goals.jpeg)

Mon superviseur atteste que je dois m'améliorer sur mon analyse du problème et du logiciel qui va le résoudre. Je suis d'accord avec lui car malgré le fait que j'ai proposé énormément des solutions pour leur logiciel, je le faisais à la volée et sans me soucier de l'ensemble du code. Ceci me causait d'innombrables problèmes qui aurait pu être évité si j'avais mieux étudier la situation. En conclusion, j'aurais pu avoir une meilleure qualité de code et une meilleure gestion du temps si j'avais arrêter pour quelques minutes pour réfléchir à la solution avant de plonger dans l'écriture de l'algorithme.

De mon côté, j'ai mis le doute de soi et mes compétences sociales. Le doute de soi parce que j'avais du mal à prendre un décision et je refaisais plusieurs fois la même tâche car j'étais pas convaincu qu'elle était suffisamment bonne. J'ai besoin d'être plus confiant car un jour dans l'avenir, je serai un spécialiste et je n'aurai personne pour me guider. Je dois avoir la confiance pour prendre les décisions par moi-même, en me basant sur l'analyse antérieure que j'ai fait du problème. Alors, je pense que mon problème de doute de soi peut être résolu en résolvant le problème d'analyse signalé par mon superviseur.
En ce qui concerne mes compétences sociales, je dirais que je dois faire plus d'effort pour parler et avoir des discussions intéressantes avec mes collègues. Me fermer sur moi et ne faire qu'écouter n'est pas une stratégie à avoir.

Pour ce qu'il reste du projet, moi et mon superviseur sommes d'accord qu'il faut que je gère mieux le projet pour le finir bien. Et c'est ce que je ferai pour la suite.