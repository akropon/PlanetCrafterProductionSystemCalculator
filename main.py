import math
from types import SimpleNamespace


def calculateAndPrintMinimalSetup(resource2source,
                                  source2productivity,
                                  resource2normalizerNeededProductivity,
                                  neededProductivityMultiplier):

    resource2calculatedData = {}

    for resource, resourceNormalizedNeededProductivity in resource2normalizerNeededProductivity.items():
        resourceNeededProductivity = resourceNormalizedNeededProductivity * neededProductivityMultiplier
        source = resource2source.get(resource)
        sourceProductivity = source2productivity.get(source)
        theoreticalCountOfNeededSources =  resourceNeededProductivity / sourceProductivity
        countOfNeededSources = math.ceil(theoreticalCountOfNeededSources)
        excessiveSourceProductivity = countOfNeededSources - theoreticalCountOfNeededSources
        roundedExcessiveSourceProductivityInPercents = round(excessiveSourceProductivity * 100)

        data = SimpleNamespace()
        data.resource = resource
        data.source = source
        data.countOfNeededSources = countOfNeededSources
        data.excessiveSourceProductivity = excessiveSourceProductivity
        data.roundedExcessiveSourceProductivityInPercents = roundedExcessiveSourceProductivityInPercents

        resource2calculatedData[resource] = data

    return resource2calculatedData

def do():
    t3oreExtractor = "T3OE"
    t2gasExtractor = "T2GE"
    t1outdoorFarm = "T1OF"
    lakeWaterCollector = "LWC"

    si = "Si"
    fe = "Fe"
    al = "Al"
    zeolite = "Zeolite"
    n = "N"
    h2o = "H2O"
    mushroom = "Mushroom"

    resource2source = {
        si: t3oreExtractor,
        fe: t3oreExtractor,
        al: t3oreExtractor,
        zeolite: t3oreExtractor,
        n: t2gasExtractor,
        h2o: lakeWaterCollector,
        mushroom: t1outdoorFarm,
    }

    # productivity is a count of produced items per 1 second
    source2productivity = {
        t3oreExtractor: 1.0 / 75.0,
        t2gasExtractor: 1.0 / 80.0,
        lakeWaterCollector: 1.0 / 100.0,
        t1outdoorFarm: 5.0 / 100.0,
    }

    # per second
    resource2normalizedNeededProductivity = {
        si: 2,
        fe: 1,
        al: 1,
        zeolite: 1,
        n: 1,
        h2o: 1,
        mushroom: 2,
    }

    # neededProductivityMultiplier = 0.6 / 60
    #
    # resource2calculatedData = calculateAndPrintMinimalSetup(resource2source,
    #                               source2productivity,
    #                               resource2normalizedNeededProductivity,
    #                               neededProductivityMultiplier)
    #
    # for d in resource2calculatedData.values():
    #     print(f"{d.countOfNeededSources} x {d.source}[{d.resource}] "
    #           f"(unused: {d.roundedExcessiveSourceProductivityInPercents}%)")

    source2unusedProductivityEvaluationWeight = {
        t3oreExtractor: 1.0,
        t2gasExtractor: 0.1,
        lakeWaterCollector: 0.1,
        t1outdoorFarm: 0.1,
    }

    minMultiplier = 0.5/60
    maxMultiplier = 3.0/60
    multiplierStep = 0.1/60

    bestMultiplier = minMultiplier
    bestUnusedProductivityEvaluation = None
    bestResource2CalculatedData = None

    currentMultiplier = minMultiplier
    while currentMultiplier <= maxMultiplier:
        resource2calculatedData = calculateAndPrintMinimalSetup(resource2source,
                                                                source2productivity,
                                                                resource2normalizedNeededProductivity,
                                                                currentMultiplier)
        unusedProductivityEvaluation = 0.0
        for data in resource2calculatedData.values():
            unusedProductivityEvaluation += data.excessiveSourceProductivity * source2unusedProductivityEvaluationWeight[data.source]

        if bestUnusedProductivityEvaluation is None or unusedProductivityEvaluation < bestUnusedProductivityEvaluation:
            bestUnusedProductivityEvaluation = unusedProductivityEvaluation
            bestMultiplier = currentMultiplier
            bestResource2CalculatedData = resource2calculatedData


        print(f"multiplier = {currentMultiplier} (i.e. {currentMultiplier * 60:.2f} sets per 1 minute)")
        print(f"unusedProductivityEvaluation = {round(unusedProductivityEvaluation * 100)}%")
        for d in resource2calculatedData.values():
            print(f"{d.countOfNeededSources} x {d.source}[{d.resource}] "
                  f"(unused: {d.roundedExcessiveSourceProductivityInPercents}%)")
        print()

        currentMultiplier += multiplierStep

    print(f"best multiplier = {bestMultiplier} (i.e. {bestMultiplier * 60:.2f} sets per 1 minute)")
    print(f"best bestUnusedProductivityEvaluation = {round(bestUnusedProductivityEvaluation * 100)}%")
    for d in bestResource2CalculatedData.values():
        print(f"{d.countOfNeededSources} x {d.source}[{d.resource}] "
              f"(unused: {d.roundedExcessiveSourceProductivityInPercents}%)")


do()
