"""Functions related to FVA."""
from cobra.flux_analysis import flux_variability_analysis
import logging
import time
log = logging.getLogger(__name__)


def run_fva(model, rxnsOfInterest, proc, fraction_opt):
    log.info("Starting FVA...")
    start_time = time.time()
    s = flux_variability_analysis(model, reaction_list=rxnsOfInterest, fraction_of_optimum=fraction_opt,
                                  processes=proc)
    elapsed_time = time.time() - start_time
    log.info("Total elapsed FVA time: {:.2f} sec".format(elapsed_time))
    return s


def calculate_score(fva_wt_mut_merged):
    rxns_of_interest = fva_wt_mut_merged.index
    # Format the flux ranges to be more usable:
    WTint = {}
    mutantint = {}
    for rn in rxns_of_interest:
        WTint[rn] = [round(fva_wt_mut_merged.loc[rn]["minWT"], 3), round(fva_wt_mut_merged.loc[rn]["maxWT"], 3)]
        mutantint[rn] = [round(fva_wt_mut_merged.loc[rn]["minKO"], 3), round(fva_wt_mut_merged.loc[rn]["maxKO"], 3)]

    # Calculate a score for each pair of flux ranges (WT and mutant):
    score = []  # Score to be compared to the score threshold
    flux_change = {}  # Flux change direction
    for r in rxns_of_interest:  # For the one KO or for each reaction in the group of KOs
        lb = [WTint[r][0], mutantint[r][0]]  # Store the two lower bounds (WT and mutant)
        ub = [WTint[r][1], mutantint[r][1]]  # Store the two upper bounds (WT and mutant)
        if lb == [0, 0]:
            change_lower_bound = 0
        else:
            # Calculate the difference between the lower bounds divided by the biggest absolute lower
            # bound Ex: WT = [-20, 50] mutant = [1, 30] change_lower_bound = abs(1 - 20) / 20 = 0.95
            # change_upper_bound = abs(50 - 30) / 50 = 0.4 ==> score will be 0.95
            change_lower_bound = abs(max(lb) - min(lb)) / max([abs(el) for el in lb])
        if ub == [0, 0]:
            change_upper_bound = 0
        else:
            change_upper_bound = abs(max(ub) - min(ub)) / max([abs(el) for el in ub])
        score.append(max(change_lower_bound, change_upper_bound))  # Choose the max change as the score

        # Determine direction of change
        # If both lower bounds are the same, and both upper bounds are the same ==> no change
        if WTint[r][0] == mutantint[r][0] and WTint[r][1] == mutantint[r][1]:
            flux_change[r] = 0
        # If the WT upper bound is lower than the mutant lower bound ==> significant change
        elif WTint[r][1] < mutantint[r][0]:
            flux_change[r] = 1
        elif WTint[r][0] > mutantint[r][1]:
            flux_change[r] = -1
        elif ((WTint[r][0] <= mutantint[r][0])
              and (WTint[r][1] <= mutantint[r][1])
              and (max(abs(WTint[r][0] - mutantint[r][0]),
                       abs(WTint[r][1] - mutantint[r][1])) > 0)):
            flux_change[r] = 1
        elif ((WTint[r][0] >= mutantint[r][0])
              and (WTint[r][1] >= mutantint[r][1])
              and (abs(WTint[r][0] - mutantint[r][0]) > 0
                   or abs(WTint[r][1] - mutantint[r][1]) > 0)):
            flux_change[r] = -1
        else:
            flux_change[r] = 0
    score_dict = dict(zip(rxns_of_interest, score))
    return score_dict, flux_change
