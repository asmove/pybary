from __future__ import annotations


# For a new value newValue, compute the new (count, mean, M2).
# Each metric aggregates dataset sofar:
#   - mean: the values average;
#   - M2: the squared distance from the mean;
#   - count: the number of samples;
def update_aggregate_stats(aggregateStats, newValue):
    (count, mean, M2) = aggregateStats

    count += 1
    delta = newValue - mean
    mean += delta / count
    delta2 = newValue - mean
    M2 += delta * delta2

    return (count, mean, M2)


# Retrieve the mean, variance and sample variance from an aggregate
def finalize_stats(aggregateStats):
    (count, mean, M2) = aggregateStats

    if count < 2:
        return float("nan")
    else:
        (mean, variance, sampleVariance) = (mean, M2 / count, M2 / (count - 1))
        return (mean, variance, sampleVariance)
