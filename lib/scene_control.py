# Ce programme définit la classe PWMControl.

import machine

class SceneControl:
    """La classe SceneControl permet d'appeler des fonctions selon un scénario indéxé sur le temps.

    Le scénario est construit à l'aide de la méthode add_call(). Il peut être ensuite exécuté avec
    la méthode start().
    """

    class _TimerWithData:
        # La classe privée _TimerWithData est utilisée pour associer un timer avec les données
        # nécessaires à sa mise en œuvre dans le cadre d'une scène.
        def __init__(self, schedule_ms, func, *args, **kwargs):
            # Le nombre et la nature des paramètres reçus par func est quelconque.
            self.schedule_ms = schedule_ms
            self.func = func
            self.args = args
            self.kwargs = kwargs

            self._timer = machine.Timer()

        def init(self):
            # Fonction d'initialisation du timer
            self._timer.init(mode=machine.Timer.ONE_SHOT, period=self.schedule_ms,
                             callback=lambda t: self.func(*self.args, **self.kwargs))

        def deinit(self):
            self._timer.deinit()

    def __init__(self):
        """SceneControl() initialise un objet qui permettra de gérer l'appel de fonctions
        synchronisées avec le temps.
        """
        self._timers_with_data = []

    def add_call(self, schedule_ms, func, *args, **kwargs):
        """La méthode add_call() ajoute un appel de fonction au scénario.

        :param schedule_ms: int, le nombre de millisecondes à partir de l'appel à la methode start()
        après lequel la fonction func sera appelée.
        :param func: la fonction qui sera appelée.
        :param args: une liste (éventuellement vide) de paramètres positionnels qui seront passés à la fonction
        func lorsqu'elle sera appelée.
        :param kwargs: un dictionnaire (éventuellement vide) de paramètres par mots-clefs qui seront passés
        à la fonction func lorsqu'elle sera appelée.
        """
        self._timers_with_data.append(SceneControl._TimerWithData(schedule_ms, func, *args, **kwargs))

    def start(self):
        """La méthode start() lance l'exécution du scénario construit avec la méthode add_call().
        """
        for schedule_func_param in self._timers_with_data:
            schedule_func_param.init()

    def stop(self):
        """La méthode stop() interrompt l'exécution du scénario en cours d'exécution.
        """
        for schedule_func_param in self._timers_with_data:
            schedule_func_param.deinit()

    def __del__(self):
        # La méthode __del__ est appelée quand l'objet est détruit.
        # Elle arrête proprement tout ce qui doit l'être.
        self.stop()
        

if __name__ == "__main__":
    # Démonstration de l'utilisation de la classe SceneControl.

    # Le programme ci-dessous est inclus dans un gestionnaire d'exception afin de s'arrêter proprement
    # s'il est interrompu.
    try:
        from time import ticks_ms, sleep

        # Pour les besoins de la démonstration, on définit la fonction time_print().
        # Elle se comporte comme la fonction print() mais chaque ligne commence
        # par un marqueur temporel en millisecondes correspondant au moment de l'affichage.
        def time_print(*args, **kwargs):
            print(ticks_ms(), *args, **kwargs)

        # Création d'une instance de SceneControl.
        scene_control = SceneControl()

        # Quand la méthode start() de l'objet scene_control sera appelée...
        # La fonction time_print() sera immédiatement appelée et on lui passera la chaîne de caractère "a"
        scene_control.add_call(0, time_print, "a")
        # Après 1 seconde (1000 millisecondes), la fonction time_print() sera appelée et on lui passera l'entier 2
        scene_control.add_call(1000, time_print, 2)
        # Après 1.5 secondes, la fonction time_print() sera appelée et on lui passera le float 3.14
        scene_control.add_call(1500, time_print, 3.14)
        # Après 3 secondes, la fonction time_print() sera appelée et on lui passera les chaînes "hello" et "world"
        scene_control.add_call(3000, time_print, "hello", "world")
        # Enfin au bout de 5 secondes, la méthode start() sera rappelée et le scénario se reproduira
        scene_control.add_call(5000, scene_control.start)

        # Pour commencer tout cela, on appelle la méthode start()
        scene_control.start()

        # Ici le programme s'arrête et Python retour au REPL (et on peut à nouveau taper
        # des instructions dans la console).
        # Néanmoins, il peut être intéressant de faire autre chose pendant que le scénario se déroule...
        # Par exemple, ici on entre dans une boucle infinie qui affiche une ligne de séparation une fois par seconde.
        # Pendant ce temps, le scénario ci-dessus s'exécute de manière indépendante.
        #
        # while True:
        #     print("--<>--<>--<>--<>--<>--<>--<>--<>--")
        #     sleep(1)

    except KeyboardInterrupt:
        # L'utilisateur a interrompu le programme, on réinitialise la carte.
        machine.reset()
