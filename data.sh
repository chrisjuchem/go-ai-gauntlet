NAMES=("00-random"\
  "01-odd-diagonal"\
  "02-even-diagonal"\
  "03-alphabetical"\
  "04-reverse-alphabetical"\
  "05-center"\
  "06-anti-center"\
  "70-leela"\
  "75-50.0%-leela-(random)"\
  "79-1.0%-leela-(random)"\
)

for N1 in ${NAMES[@]}; do
  for N2 in ${NAMES[@]}; do
    MYPATH="results/${N1}/${N2}"
    mkdir -p $MYPATH
    mv results/gifs/${N1}__${N2}* $MYPATH
  done
done