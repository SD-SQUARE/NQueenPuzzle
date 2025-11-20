import constants

solutions = []
canvas = None
n_var = None
strategy_var = None
listbox = None
cancel_flag = False
status_var = None

is_reporting = False


# main screen timer
# main_timer_seconds = 15 * 60    # 900 seconds
main_timer_seconds = 1 * 10    # 900 seconds
main_timer_running = False
main_timer_label = None
main_timer_started_once = False

#  report screen timer
timer_seconds = 0
timer_running = False
timer_label = None


# Global results: strategy -> {"solutions": [...], "times": [...]}
algorithm_results = {
    constants.ALGO_BACKTRACKING: {"solutions": [], "times": []},
    constants.ALGO_BEST_FIRST:   {"solutions": [], "times": []},
    constants.ALGO_HILL_CLIMB:   {"solutions": [], "times": []},
    constants.ALGO_CULTURAL:     {"solutions": [], "times": []},
}