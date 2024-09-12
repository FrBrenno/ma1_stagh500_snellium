# Week 8 - 02.09/06.09

09/09/2024

Bonjour Monsieur Quitin,

J'espère que vous allez bien.

Avant de vous faire mon rapport de la semaine passée, je souhaite insister sur la date de la visite de mi-parcours. Récemment, j'ai appris que l'étudiant avec qui j'organisais cette visite ne fait plus de stage, et je dois maintenant m'en occuper seul. Je vous propose donc à nouveau la date du lundi 16/09 à 11h pour la visite de mi-parcours. Mon maître de stage est disponible, et selon le calendrier public de Cédric Boey, il l'est également. J'ai besoin de votre confirmation au plus vite afin de pouvoir contacter Cédric.

Voici maintenant le rapport de ma huitième semaine.

Je me concentre actuellement sur l'intégration de mon code dans le logiciel existant. Cette semaine, j'ai pu terminer la première étape, qui consistait en la création d'un module d'abstraction pour un microcontrôleur. Il s'agit de l'interface d'utilisation du microcontrôleur ainsi que de l'interface que le véritable module doit implémenter. L'architecture est la suivante :

Dans l'espace **_daemon_**, qui concerne le logiciel, nous avons :

- le module **_core_**, qui maintient les fonctionnalités de base et est responsable de la gestion des autres modules. 

- le module **_microcontroller_**, qui est une abstraction + interface pour les microcontrôleurs. 

Dans l'espace **_module_**, nous avons les modules réels qui implémentent les abstractions, définies dans le daemon, et sont spécifiques à un appareil. Par exemple, je devrai à l'avenir implémenter un module _microcontroller_serial_ qui gérera un microcontrôleur communiquant en série avec le logiciel.

Cette partie a été fusionnée avec succès au code de base après près de deux semaines de révisions avec mon maître de stage. Grâce à ces révisions, j'ai pu identifier et corriger de nombreux défauts dans mon code, qu'il s'agisse de bugs ou de mauvais choix de conception.

Pour finir, j'ai rédigé la documentation de ce module, expliquant l'architecture, le fonctionnement et le protocole de communication.

Alors la suite de mon travail consistait à développer un module _microcontroller_virtual_ qui simule un microcontrôleur afin de pouvoir faire des tests de l'ensemble de l'application. Par contre, en commençant à écrire le code de ce module, j'ai constaté beaucoup de redondances dans l'architecture du logiciel. En effet, les modules **_camera_** et **_microcontroller_** sont très similaires, et certaines méthodes ne diffèrent que par un type ou un nom. Dans le but de réduire cette redondance, voire de simplifier l'architecture, j'ai proposé à mon maître de stage de créer une abstraction. Celle-ci consisterait en un module **_device_** qui servirait d'interface pour tout type d'appareil. La redondance entre **_camera_** et **_microcontroller_** pourrait être réduite en extrayant le code commun vers un module d'abstraction supérieur, ne laissant que les parties spécifiques à chaque module. 

Ma tâche cette semaine sera donc d'étudier cette possibilité et de mener à bien cette abstraction.

Bien à vous,  

Brenno Ferreira.