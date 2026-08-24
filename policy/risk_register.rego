# The risk register's rules, written as policy instead of as a script.
#
# Open Policy Agent enforces these. OPA is a CNCF Graduated project under
# Apache-2.0, so a buyer reading this repository sees a rule engine they already
# know rather than eighty lines of Python only this estate has ever run.
#
# What this file covers and what it cannot:
#
#   covered here   every rule about the shape of a row -- required fields,
#                  duplicate ids, allowed status words, a claim of mitigated
#                  with no receipt, a receipt written as a path inside one
#                  person's home directory, an empty register, a register where
#                  nothing has ever moved.
#
#   NOT covered    whether the program a receipt names actually exists on this
#                  machine. That is a filesystem question and Rego cannot read
#                  the filesystem, by design. scripts/verify.d/85-risk-register.sh
#                  keeps that half and stays the fallback for all of it.
#
# So this does not delete the script. It moves the seven rules a policy engine
# is better at, leaves the one it cannot do, and gives the estate two checks
# that must agree.
#
# Run it:
#   jq -s '{risks: .}' risk/REGISTER.jsonl | conftest test --parser json -p policy -
#
# The {risks: .} wrapper is not decoration. conftest splits a top-level JSON
# array into one document per element, so a bare array makes `input` a single
# row and every whole-register rule fires once per row. Measured 2026-08-24:
# eleven identical failures from a register that was fine.
package main

required := {
	"id", "opened", "title", "what_goes_wrong", "likelihood",
	"cost", "mitigation", "residual", "owner", "evidence", "status",
}

allowed_status := {"open", "mitigated", "closed", "accepted"}

worked_status := {"mitigated", "closed"}

# The first word of a receipt is the program it runs.
first_word(s) := split(trim_space(s), " ")[0]

# A row that does not carry every field is a row somebody stopped writing
# halfway. Name the missing fields, because "invalid row" costs a reader a diff.
deny contains msg if {
	some row in input.risks
	missing := required - object.keys(row)
	count(missing) > 0
	msg := sprintf("%v lacks %v", [object.get(row, "id", "a row with no id"), sort(missing)])
}

# Two rows with one id means one of them is invisible to every query that reads
# the register by id, and nobody finds out which.
deny contains msg if {
	some i, j
	input.risks[i].id == input.risks[j].id
	i < j
	msg := sprintf("%v appears twice", [input.risks[i].id])
}

deny contains msg if {
	some row in input.risks
	not row.status in allowed_status
	msg := sprintf("%v has status %q, expected one of %v", [row.id, row.status, sort(allowed_status)])
}

# Mitigated is a claim. Without a receipt it is somebody's opinion wearing the
# word, which is the exact failure a register exists to prevent.
deny contains msg if {
	some row in input.risks
	row.status in worked_status
	trim_space(row.evidence) == ""
	msg := sprintf("%v claims %v with no evidence command", [row.id, row.status])
}

# A receipt whose first word is a path inside somebody's home directory runs on
# one machine and nowhere else. It is this estate's fingerprint, and a buyer
# checking the row from their own laptop gets nothing. Both spellings are
# refused: the tilde a person writes, and the expanded path a script produces.
deny contains msg if {
	some row in input.risks
	prog := first_word(row.evidence)
	home_path(prog)
	msg := sprintf(
		"%v evidence starts with %q, a path inside one person's home directory -- nobody else can run it. Write a receipt whose first word is a program on PATH, or a repo-relative path.",
		[row.id, prog],
	)
}

home_path(p) if startswith(p, "~")

home_path(p) if startswith(p, "/Users/")

home_path(p) if startswith(p, "/home/")

deny contains msg if {
	count(input.risks) == 0
	msg := "the risk register is empty"
}

# A register where nothing has ever moved is a list of complaints. This is the
# one rule that judges the register as a whole rather than a row.
deny contains msg if {
	count(input.risks) > 0
	worked := [row | some row in input.risks; row.status in worked_status]
	count(worked) == 0
	msg := "all risks are still open -- a register that only grows is a list of complaints, not a register"
}
