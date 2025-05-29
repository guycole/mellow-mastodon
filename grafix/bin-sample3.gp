# plot bin-sample2
set title 'bin-sample3 (rolling mean vs actual)'
set xlabel 'frequency'
set ylabel 'dbm'
set grid
#
set terminal png size 1200,800
set output 'bin-sample3.png'
set key outside
plot for [col=2:3] 'bin-sample3.dat' using 1:col
#plot 'bin-sample2.dat'
#
