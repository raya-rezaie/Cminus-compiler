from semantic_actions import *
from semantic_stack import *
from run_time_memory import *
PB_BASE = 0
PB_BOUND = 99
DB_BASE = 100
DB_BOUND = 499
TP_BASE = 500
TP_BOUND = 1000

stack = SemantciStack()
program_block = programBlock(PB_BASE , PB_BOUND)
data = dataBlock(DB_BASE , DB_BOUND)
temps = temporaryBlock(TP_BASE , TP_BOUND)

#memory = run_time_memory()

    