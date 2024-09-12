# Ce programme définit la classe PWMControl.

import machine
import time


class SceneControl:
    """La classe SceneControl permet d'appeler des fonctions quelconques selon un scénario indéxé sur le temps.

    Le scénario est construit à l'aide de la méthode add_call_after(). Le scénario peut ensuite être exécuté en
    appelant la méthode start().

        # Création d'une instance de SceneControl.
        scene_control = SceneControl()

        # Ajout de tâches
        scene_control.add_call_after(0, print, "a")
        scene_control.add_call_after(1000, print, 2)
        # Appeler la méthode reinit de l'objet scene_control permet de revenir au début de la scene.
        scene_control.add_call_after(2000, scene_control.reinit)

        # Pour commencer tout cela, on appelle la méthode start()
        scene_control.start()

    À noter que l'ordre d'exécution de 2 tâches programmées pour le même moment est indéterminé.
    """

    class _Task:
        def __init__(self, scene_control, start_time_ms, func, *args, **kwargs):
            # Le nombre et la nature des paramètres reçus par func est quelconque.
            self.scene_control = scene_control
            self.start_time_ms = start_time_ms
            self.func = func
            self.args = args
            self.kwargs = kwargs

        def init(self, timer, scene_start_time):
            delay_ms = max(self.start_time_ms - scene_start_time, 0)
            timer.init(mode=machine.Timer.ONE_SHOT, period=delay_ms, callback=self._task)

        def _task(self, t):
            self.func(*self.args, **self.kwargs)
            self.scene_control.start_task()

        @staticmethod
        def sorted(list_of_tasks):
            return sorted(list_of_tasks, key=lambda task: task.start_time_ms)

    def __init__(self):
        """SceneControl() initialise un objet qui permettra de gérer l'appel de fonctions
        synchronisées avec le temps.
        """
        self._tasks = []
        self._task_index = None
        self._scene_start_tick = None
        self._timer = machine.Timer()

    def add_call_after(self, start_time_ms, func, *args, **kwargs):
        """La méthode add_call_after() ajoute un appel de fonction au scénario.

        :param start_time_ms: int, le nombre de millisecondes à partir de l'appel à la methode start()
        après lequel la fonction func sera appelée.
        :param func: la fonction qui sera appelée.
        :param args: une liste (éventuellement vide) de paramètres positionnels qui seront passés à la fonction
        func lorsqu'elle sera appelée.
        :param kwargs: un dictionnaire (éventuellement vide) de paramètres par mots-clefs qui seront passés
        à la fonction func lorsqu'elle sera appelée.
        """
        self._tasks.append(SceneControl._Task(self, start_time_ms, func, *args, **kwargs))
        self._tasks = self._Task.sorted(self._tasks)
        # TODO: as the tasks are added one by one, sorting is a matter of inserting the new task at the right place
        # TODO: replace the sorted() call

    # TODO: def add_call_each(self, period_ms, func, *args, **kwargs)

    def reinit(self):
        if len(self._tasks) > 0:
            self._task_index = 0
            self._scene_start_tick = time.ticks_ms()

    def start(self):
        """La méthode start() lance l'exécution du scénario construit avec la méthode add_call().
        """
        if self._task_index is None and len(self._tasks) > 0:
            self.reinit()
            self.start_task()

    def stop(self):
        """La méthode stop() interrompt l'exécution du scénario en cours d'exécution.
        """
        self._timer.deinit()
        self._task_index = None

    def start_task(self):
        if self._task_index is not None and self._task_index < len(self._tasks):
            self._tasks[self._task_index].init(self._timer, time.ticks_diff(time.ticks_ms(), self._scene_start_tick))
            self._task_index += 1

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
        start = ticks_ms()
        def time_print(*args, **kwargs):
            print(time.ticks_diff(ticks_ms(), start), *args, **kwargs)

        # Création d'une instance de SceneControl.
        scene_control = SceneControl()

        # Quand la méthode start() de l'objet scene_control sera appelée...
        # La fonction time_print() sera immédiatement appelée et on lui passera la chaîne de caractère "a"
        scene_control.add_call_after(0, time_print, "a")
        # Après 1 seconde (1000 millisecondes), la fonction time_print() sera appelée et on lui passera l'entier 2
        scene_control.add_call_after(1000, time_print, 2)
        # Après 1.5 secondes, la fonction time_print() sera appelée et on lui passera le float 3.14
        scene_control.add_call_after(1500, time_print, 3.14)
        scene_control.add_call_after(1500, time_print, 3.15)
        # Après 3 secondes, la fonction time_print() sera appelée et on lui passera les chaînes "hello" et "world"
        scene_control.add_call_after(3000, time_print, "hello", "world")
        # Enfin au bout de 5 secondes, la méthode start() sera rappelée et le scénario se reproduira
        scene_control.add_call_after(5000, scene_control.reinit)

        # Pour commencer tout cela, on appelle la méthode start()
        scene_control.start()

        # Ici le programme s'arrête et Python retourne au REPL. On peut donc à nouveau taper
        # des instructions dans la console pendant que le scénario se déroule.
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
