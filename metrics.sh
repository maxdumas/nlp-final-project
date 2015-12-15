find output -type f -name '*.score' | cut -d '.' -f 1 - | xargs basename > _files.metrics

cat output/*.score | sed -nE 's/█ Correct Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in both, equal\]/\1/p' > _correct.real.metrics
cat output/*.baseline_score | sed -nE 's/█ Correct Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in both, equal\]/\1/p' > _correct.baseline.metrics

cat output/*.score | sed -nE 's/• Incorrect Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in both but unequal\]/\1/p' > _incorrect.real.metrics
cat output/*.baseline_score | sed -nE 's/• Incorrect Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in both but unequal\]/\1/p' > _incorrect.baseline.metrics

cat output/*.score | sed -nE 's/░ Missing Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in key, not in result\]/\1/p' > _missed.real.metrics
cat output/*.baseline_score | sed -nE 's/░ Missing Matches: [0-9]+\/[0-9]+ \(([0-9]+)%\) \[in key, not in result\]/\1/p' > _missed.baseline.metrics

echo 'file_name,real,baseline' > paper/metrics_correct.csv
paste -d ',' _files.metrics _correct.real.metrics _correct.baseline.metrics >> paper/metrics_correct.csv

echo 'file_name,real,baseline' > paper/metrics_incorrect.csv
paste -d ',' _files.metrics _incorrect.real.metrics _incorrect.baseline.metrics >> paper/metrics_incorrect.csv

echo 'file_name,real,baseline' > paper/metrics_missed.csv
paste -d ',' _files.metrics _missed.real.metrics _missed.baseline.metrics >> paper/metrics_missed.csv

rm *.metrics
