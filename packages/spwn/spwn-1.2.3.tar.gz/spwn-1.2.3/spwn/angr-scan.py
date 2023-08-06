import angr
import resource

rsrc = resource.RLIMIT_DATA
_, hard = resource.getrlimit(rsrc)
resource.setrlimit(rsrc, (1 << 30, hard))

find = []
avoid = []

filename = "main"
proj = angr.Project(filename, auto_load_libs=False)

def dump_state(state):
	print("stdin:")
	print(state.posix.dumps(0))
	print()
	print("stdout:")
	print(state.posix.dumps(1))
	print()
	parent_addr = state.history.parent.addr
	if parent_addr:
		print("Caller address:", hex(parent_addr))
	print("callstack:")
	print(state.callstack.dbg_repr())
	print()

class CheckPrintf(angr.SimProcedure):
	def run(self, fmt, *args):
		if fmt.symbolic:
			print("Symbolic printf pointer")
			dump_state(self.state)
			return

		while True:
			bt = self.state.memory.load(fmt, 1)
			if bt.symbolic:
				print("Symbolic printf")
				dump_state(self.state)
				break
			if bt.args[0] == 0:
				break
			fmt += 1


proj.hook_symbol("printf", CheckPrintf())

initial_state = proj.factory.entry_state(
	add_options={
		angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS,
		angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY,
	}
)

sim = proj.factory.simgr(initial_state)

seen = set()
try:
	while sim.active:
		sim.step()
		if hasattr(sim, "unconstrained") and sim.unconstrained:
			for state in sim.unconstrained:
				if state not in seen:
					dump_state(state)
					seen.add(state)
except Exception as e:
	print("Killed")
	print(e)
