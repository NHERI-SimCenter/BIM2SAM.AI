# This script runs through the cyclic analysis of the model. It attempts multiple solution algorithms 
# to see which one will converge. The scrips also attempts using smaller step sizes. The tryTog determines
# if the solutions needs to iterate i.e., a smaller step size is used so multiple runs are needed to achieve
# the required Dincr
constraints Plain
numberer RCM
system BandGeneral
set globalSolutionTol 1.e-6;set numIter	50;set printFlagStatic 0;
test NormDispIncr $globalSolutionTol $numIter $printFlagStatic;
algorithm Newton;
analysis Static;
foreach ii $Peak {
set targetDisp [expr $ii];
if {abs($targetDisp) < 0.9} {set Dpos 0.001};if {abs($targetDisp) > 0.900} {set Dpos 0.001};
if {abs($targetDisp) < 0.9} {set Dneg -0.001};if {abs($targetDisp) > 0.90} {set Dneg -0.001};
set ok 0;
if {$targetDisp > 0} {set Dincr $Dpos} else {set Dincr $Dneg}
while {$ok == 0} {
set tryTog 0;
set failTog 0;


integrator DisplacementControl $nodeTag $dofTag $Dincr
set ok [analyze 1]
if {$ok == 0} {
puts "finished step $stepCount"
} else {puts "analysis failed, lets try smaller step size"
}

if {$ok != 0} {
set Dtry [expr $Dincr/100.]
set tryTog 1;
integrator DisplacementControl $nodeTag $dofTag $Dtry
set ok [analyze 1]

if {$ok == 0} {
puts "smaller step worked;finished step $stepCount"
} else {puts "analysis failed, lets try modified Newton"
}
}

if {$ok != 0} {
set tryTog 0;
integrator DisplacementControl $nodeTag $dofTag $Dincr
algorithm Newton -initial
set ok [analyze 1]

if {$ok == 0} {
puts "modified Newton worked;finished step $stepCount"
} else {puts "analysis failed, lets try smaller step"
}
}

if {$ok != 0} {
set Dtry [expr $Dincr/100.]
set tryTog 1;
integrator DisplacementControl $nodeTag $dofTag $Dtry
set ok [analyze 1]

if {$ok == 0} {
puts "smaller modified Newton step worked;finished step $stepCount"
} else {puts "analysis failed, try Krylov"
}
}

if {$ok != 0} {
set tryTog 0;
integrator DisplacementControl $nodeTag $dofTag $Dincr
algorithm KrylovNewton
set ok [analyze 1]

if {$ok == 0} {
puts "Krylov-Newton worked;finished step $stepCount"
} else {puts "analysis failed, lets try Krylov-Newton smaller"
}
}

if {$ok != 0} {
set Dtry [expr $Dincr/1000.]
set tryTog 1;
integrator DisplacementControl $nodeTag $dofTag $Dtry
set ok [analyze 1]

if {$ok == 0} {
puts "smaller Krylov step worked;finished step $stepCount"
} else {puts "analysis failed, let it go"
}
}

if {$ok != 0} {
set failTog 1
break
}

algorithm Newton
incr stepCount
# differentiates between analyses that need iteration of stepsize and those that do not
if {$tryTog > 0} {set delta $Dtry} else {set delta $Dincr}

set Dtot [expr $Dtot + $delta]

if {$Dincr > 0 && $Dtot > $ii} {break}
if {$Dincr < 0 && $Dtot < $ii} {break}
}

if {$failTog > 0} {
puts "Wall Analysis Failed"
break
}

}
puts "Wall Analysis complete"
wipe

