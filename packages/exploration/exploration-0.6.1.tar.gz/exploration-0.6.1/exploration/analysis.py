"""
- Authors: Peter Mawhorter
- Consulted:
- Date: 2022-10-24
- Purpose: Analysis functions for decision graphs an explorations.
"""

from typing import (
    List, Dict, Tuple, Optional, TypeVar, Callable, Union, Any,
    ParamSpec, Concatenate, Set
)

from exploration import core, journal

import textwrap


def describeEffects(effects: List[core.TransitionEffect]) -> str:
    """
    Returns a string which concisely describes a list of transition
    effects. Returns an empty string if given an empty list. Examples:

    >>> describeEffects([])
    ''
    >>> describeEffects([
    ...     { 'type': 'gain', 'value': ('gold', 5), 'delay': 2, 'charges': 3},
    ...     {
    ...         'type': 'lose',
    ...         'value': 'flight',
    ...         'delay': None,
    ...         'charges': None
    ...     },
    ... ])
    'gain gold*5 *3 ,2; lose flight'
    >>> d = describeEffects([
    ...     {
    ...         'type': 'edit',
    ...         'value': [
    ...             [
    ...                 core.command('val', 5),
    ...                 core.command('empty', 'list'),
    ...                 core.command('append')
    ...             ],
    ...             [
    ...                 core.command('val', 11),
    ...                 core.command('assign', 'var'),
    ...                 core.command('op', '+', '$var', '$var')
    ...             ],
    ...         ],
    ...         'delay': None,
    ...         'charges': None
    ...     },
    ... ])
    >>> d[:53]
    'with effects:\\n    edit [\\n      val 5\\n      empty list'
    >>> d[53:90]
    '\\n      append $_\\n    ] [\\n      val 11'
    >>> d[90:]
    '\\n      assign var $_\\n      op + $var $var\\n    ]\\n'
    >>> for line in d.splitlines():
    ...     print(line)
    with effects:
        edit [
          val 5
          empty list
          append $_
        ] [
          val 11
          assign var $_
          op + $var $var
        ]
    """
    edesc = ''
    pf = journal.ParseFormat()
    if effects:
        for effect in effects:
            edesc += '; ' + pf.argsString(pf.unparseEffect(effect))
        if len(edesc) > 60 or '\n' in edesc:
            edesc = (
                '; with effects:\n'
              + ';\n'.join(
                    textwrap.indent(
                        pf.argsString(pf.unparseEffect(effect)),
                        '    '
                    )
                    for effect in effects
                )
              + '\n'
            )

    return edesc[2:]  # chop off initial '; '


def describeProgress(exploration: core.Exploration) -> str:
    """
    Describes the progress of an exploration by noting each room/zone
    visited and explaining the options visible at each point plus which
    option was taken. Notes powers/tokens gained/lost along the way.
    Returns a string.

    Example:
    >>> from exploration import journal
    >>> e = journal.convertJournal('''\\
    ... S pit Start
    ... A gain jump
    ... A gain attack
    ... n button check
    ... zz Wilds
    ... o up
    ...   q _flight
    ... o left
    ... x left left_nook right
    ... a geo_rock
    ...   At gain geo*15
    ...   At deactivate
    ... o up
    ...   q _tall_narrow
    ... t right
    ... o right
    ...   q attack
    ... ''')
    >>> for line in describeProgress(e).splitlines():
    ...    print(line)
    Start of the exploration
    At decision pit
    In zone Start
    In region Wilds
    Gained power 'attack'
    Gained power 'jump'
    1 note(s) at this step
    There are transitions:
      left (leads to unknown)
      up (leads to unknown; requires _flight)
    Explore left to left_nook
    There are transitions:
      right (leads to pit)
    Gained 15 geo(s)
    There are transitions:
      right (leads to pit)
      up (leads to unknown; requires _tall_narrow)
    There are actions:
      geo_rock (requires X; gain geo*15; deactivate)
    Retrace right to pit
    There are transitions:
      left (leads to left_nook)
      right (leads to unknown; requires attack)
      up (leads to unknown; requires _flight)

    """
    result = ''

    prev = None
    regions: Set[core.Zone] = set()
    zones: Set[core.Zone] = set()
    last = None
    taken = None
    seenTransitions: Dict[core.Decision, Set[core.Transition]] = {}
    lastState: core.State = {}
    for i, situation in enumerate(exploration):
        if i == 0:  # skip empty situation at the start
            result += "Start of the exploration\n"
            taken = situation.transition
            continue

        # Extract info
        now = situation.graph
        here = situation.position
        nowZones: Set[core.Zone] = now.zoneAncestors(here)
        regionsHere = set(
            z
            for z in nowZones
            if now.zoneHierarchyLevel(z) == 1
        )
        zonesHere = set(
            z
            for z in nowZones
            if now.zoneHierarchyLevel(z) == 0
        )
        outgoing = now.destinationsFrom(here)
        state = situation.state

        # Print location info
        if here != last:
            if prev is None:
                result += f"At decision {here}\n"
            elif (
                prev.getDestination(last, taken) is None
             or prev.isUnknown(prev.getDestination(last, taken))
            ):
                if here not in prev:
                    result += f"Explore {taken} to {here}\n"
                else:
                    result += f"Return to {here} via {taken}\n"
            else:
                result += f"Retrace {taken} to {here}\n"
        newZones = zonesHere - zones
        for zone in sorted(newZones):
            result += f"In zone {zone}\n"
        newRegions = regionsHere - regions
        for region in sorted(newRegions):
            result += f"In region {region}\n"

        gained = state.get('powers', set()) - lastState.get('powers', set())
        gainedTokens = []
        for tokenType in state.get('tokens', {}):
            net = (
                state.get('tokens', {})[tokenType]
              - lastState.get('tokens', {}).get(tokenType, 0)
            )
            if net != 0:
                gainedTokens.append((tokenType, net))

        for power in sorted(gained):
            result += f"Gained power '{power}'\n"

        for tokenType, net in gainedTokens:
            if net > 0:
                result += f"Gained {net} {tokenType}(s)\n"
            else:
                result += f"Lost {-net} {tokenType}(s)\n"

        if len(situation.annotations) > 0:
            result += f"{len(situation.annotations)} note(s) at this step\n"

        transitions = {t: d for (t, d) in outgoing.items() if d != here}
        actions = {t: d for (t, d) in outgoing.items() if d == here}
        if transitions:
            result += "There are transitions:\n"
            for transition in sorted(transitions):
                dest = transitions[transition]
                if now.isUnknown(dest):
                    dest = 'unknown'
                req = now.getTransitionRequirement(here, transition)
                rdesc = ''
                if req != core.ReqNothing():
                    rdesc = f"; requires {req.unparse()}"
                eff = now.getTransitionEffects(here, transition)
                edesc = describeEffects(eff)
                if edesc:
                    edesc = '; ' + edesc
                result += f"  {transition} (leads to {dest}{rdesc}{edesc})\n"

        if actions:
            result += "There are actions:\n"
            for action in sorted(actions):
                req = now.getTransitionRequirement(here, action)
                rdesc = ''
                if req != core.ReqNothing():
                    rdesc = f"; requires {req.unparse()}"
                eff = now.getTransitionEffects(here, action)
                edesc = describeEffects(eff)
                if edesc:
                    edesc = '; ' + edesc
                if rdesc or edesc:
                    desc = (rdesc + edesc)[2:]  # chop '; ' from either
                    result += f"  {action} ({desc})\n"
                else:
                    result += f"  {action}\n"

        # Update state variables
        prev = now
        regions = regionsHere
        zones = zonesHere
        last = here
        lastState = state
        taken = situation.transition
        for transition in outgoing:
            seenTransitions.setdefault(here, set()).add(transition)

    return result


def unexploredBranches(
    graph: core.DecisionGraph,
    gameState: Optional[core.State] = None
) -> List[Tuple[core.Decision, core.Transition]]:
    """
    Returns a list of from-decision, transition-at-that-decision pairs
    which each identify an unexplored branch in the given graph.

    When a `gameState` is provided it only counts options whose
    requirements are satisfied by the given game state. Note that this
    doesn't perfectly map onto actually reachability since nodes between
    where the player is and where the option is might force changes in
    the game state that make it un-takeable.

    TODO: add logic to detect trivially-unblocked edges?
    """
    result = []
    for (src, dst, transition) in graph.edges(keys=True):
        req = graph.getTransitionRequirement(src, transition)
        # Check if this edge goes from a known to an unknown node
        if (
            not graph.isUnknown(src)
        and graph.isUnknown(dst)
        and (
                gameState is None
             or req.satisfied(gameState, graph.equivalences)
            )
        ):
            result.append((src, transition))
    return result


def countAllUnexploredBranches(situation: core.Situation) -> int:
    """
    Counts the number of unexplored branches in the given situation's
    graph, regardless of traversibility (see `unexploredBranches`).
    """
    return len(unexploredBranches(situation.graph))


def countTraversableUnexploredBranches(situation: core.Situation) -> int:
    """
    Counts the number of traversable unexplored branches (see
    `unexploredBranches`) in a given situation, using the situation's
    game state to determine which branches are traversable or not
    (although this isn't strictly perfect TODO: Fix that).
    """
    return len(unexploredBranches(situation.graph, situation.state))


def countActionsAtDecision(
    graph: core.DecisionGraph,
    decision: core.Decision
) -> Optional[int]:
    """
    Given a graph and a particular decision within that graph, returns
    the number of actions available at that decision. Returns None if the
    specified decision does not exist.
    """
    if decision not in graph:
        return None
    return len(graph.decisionActions(decision))


def countBranches(
    graph: core.DecisionGraph,
    decision: core.Decision
) -> Optional[int]:
    """
    Computes the number of branches at a particular decision, not
    counting actions. Returns `None` for unknown and nonexistent
    decisions so that they aren't counted as part of averages.
    """
    if decision not in graph or graph.isUnknown(decision):
        return None

    dests = graph.destinationsFrom(decision)
    branches = 0
    for transition, dest in dests.items():
        if dest != decision:
            branches += 1

    return branches


def countRevisits(
    exploration: core.Exploration,
    decision: core.Decision
) -> int:
    """
    Given an `Exploration` object and a particular `Decision` which
    exists at some point during that exploration, counts the number of
    times that decision was entered after its initial discovery (not
    counting steps where we remain in it due to a wait or action).

    Returns 0 even for decisions that aren't part of the exploration.
    """
    result = 0
    last = None
    for situation in exploration:
        here = situation.position
        if here == decision and last != decision:
            result += 1
        last = here

    # Make sure not to return -1 for decisions that were never visited
    if result >= 1:
        return result - 1
    else:
        return 0


#-----------------------#
# Generalizer Functions #
#-----------------------#

# Some type variables to make type annotations work
T = TypeVar('T')
P = ParamSpec('P')


def analyzeGraph(
    routine: Callable[Concatenate[core.DecisionGraph, P], T]
) -> Callable[Concatenate[core.Situation, P], T]:
    """
    Wraps a `DecisionGraph` analysis routine (possibly with extra
    arguments), returning a function which applies that analysis to a
    `Situation`.
    """
    def analyzesGraph(
        situation: core.Situation,
        *args: P.args,
        **kwargs: P.kwargs
    ) -> T:
        "Created by `analyzeGraph`."
        return routine(situation.graph, *args, **kwargs)

    analyzesGraph.__name__ = routine.__name__ + "InSituation"
    analyzesGraph.__doc__ = f"""
    Application of a graph analysis routine to a situation.

    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return analyzesGraph


def perDecision(
    routine: Callable[[core.Situation, core.Decision], T]
) -> Callable[[core.Situation], Dict[core.Decision, T]]:
    """
    Returns a wrapped function that applies the given
    individual-decision analysis routine to each decision in a
    situation, returning a dictionary mapping decisions to results.
    """
    def appliedPerDecision(
        situation: core.Situation,
    ) -> Dict[core.Decision, T]:
        'Created by `perDecision`.'
        result = {}
        for decision in situation.graph:
            result[decision] = routine(situation, decision)
        return result
    appliedPerDecision.__name__ = routine.__name__ + "PerDecision"
    appliedPerDecision.__doc__ = f"""
    Application of an analysis routine to each decision in a situation,
    returning a dictionary mapping decisions to results. The analysis
    routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerDecision


def perExplorationDecision(
    routine: Callable[[core.Exploration, core.Decision], T],
    mode: str = "all"
) -> Callable[[core.Exploration], Dict[core.Decision, T]]:
    """
    Returns a wrapped function that applies the given
    decision-in-exploration analysis routine to each decision in an
    exploration, returning a dictionary mapping decisions to results.

    The `mode` argument controls what we mean by "each decision:" use
    "all" to apply it to all decisions which ever existed, "known" to
    apply it to all decisions which were known at any point, "visited"
    to apply it to all visited decisions, and "final" to apply it to
    each decision in the final decision graph.
    """
    def appliedPerDecision(
        exploration: core.Exploration,
    ) -> Dict[core.Decision, T]:
        'Created by `perExplorationDecision`.'
        result = {}
        if mode == "all":
            applyTo = exploration.allDecisions()
        elif mode == "known":
            applyTo = exploration.allKnownDecisions()
        elif mode == "visited":
            applyTo = exploration.allVisistedDecisions()
        elif mode == "final":
            applyTo = list(exploration.currentGraph())

        for decision in applyTo:
            result[decision] = routine(exploration, decision)
        return result

    appliedPerDecision.__name__ = routine.__name__ + "PerExplorationDecision"
    desc = mode + ' '
    if desc == "all ":
        desc = ''
    appliedPerDecision.__doc__ = f"""
    Application of an analysis routine to each {desc}decision in an
    exploration, returning a dictionary mapping decisions to results. The
    analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerDecision


Base = TypeVar('Base', core.Situation, core.Exploration)
"Either a situation or an exploration."


def sumOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, complex, None]]
    ]
) -> Callable[[Base], Union[int, float, complex]]:
    """
    Given an analysis routine that applies to either a situation or an
    exploration and which returns a dictionary mapping some analysis
    units to individual numerical results, returns a new analysis
    routine which applies to the same input and which returns a single
    number that's the sum of the individual results, ignoring `None`s.
    Returns 0 if there are no results.
    """
    def sumResults(base: Base) -> Union[int, float, complex]:
        "Created by sumOfResults"
        results = routine(base)
        return sum(v for v in results.values() if v is not None)

    sumResults.__name__ = routine.__name__ + "Sum"
    sumResults.__doc__ = f"""
    Sum of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return sumResults


def meanOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, complex, None]]
    ]
) -> Callable[[Base], Union[int, float, complex, None]]:
    """
    Works like `sumOfResults` but returns a function which gives the
    mean, not the sum. The function will return `None` if there are no
    results.
    """
    def meanResult(base: Base) -> Union[int, float, complex, None]:
        "Created by meanOfResults"
        results = routine(base)
        nums = [v for v in results.values() if v is not None]
        if len(nums) == 0:
            return None
        else:
            return sum(nums) / len(nums)

    meanResult.__name__ = routine.__name__ + "Mean"
    meanResult.__doc__ = f"""
    Mean of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return meanResult


def medianOfResults(
    routine: Callable[
        [Base],
        Dict[Any, Union[int, float, None]]
    ]
) -> Callable[[Base], Union[int, float, None]]:
    """
    Works like `sumOfResults` but returns a function which gives the
    median, not the sum. The function will return `None` if there are no
    results.
    """
    def medianResult(base: Base) -> Union[int, float, None]:
        "Created by medianOfResults"
        results = routine(base)
        nums = sorted(v for v in results.values() if v is not None)
        half = len(nums) // 2
        if len(nums) == 0:
            return None
        elif len(nums) % 2 == 0:
            return (nums[half] + nums[half + 1]) / 2
        else:
            return nums[half]

    medianResult.__name__ = routine.__name__ + "Mean"
    medianResult.__doc__ = f"""
    Mean of analysis results over analysis units.
    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return medianResult


def perSituation(
    routine: Callable[[core.Situation], T]
) -> Callable[[core.Exploration], List[T]]:
    """
    Returns a function which will apply an analysis routine to each
    situation in an exploration, returning a list of results.
    """
    def appliedPerSituation(
        exploration: core.Exploration
    ) -> List[T]:
        result = []
        for situ in exploration:
            result.append(routine(situ))
        return result

    appliedPerSituation.__name__ = routine.__name__ + "PerSituation"
    appliedPerSituation.__doc__ = f"""
    Analysis routine applied to each situation in an exploration,
    returning a list of results.

    The analysis routine applied is: {routine.__name__}
    """ + (routine.__doc__ or '')
    return appliedPerSituation
