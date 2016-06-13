"""
Scrape a behave path and build a dependency graph.
"""
from ruruki.graphs import Graph

__all__ = [
    "GRAPH",
    "scrape_features",
    "scrape_scenarios",
    "scrape_steps",
    "scrape_background",
]

GRAPH = Graph()
GRAPH.add_vertex_constraint("FEATURE", "name")
GRAPH.add_vertex_constraint("BACKGROUND", "name")
GRAPH.add_vertex_constraint("SCENARIO", "name")
GRAPH.add_vertex_constraint("STEP", "name")
GRAPH.add_vertex_constraint("FILE", "name")


def scrape_steps(steps, parent_node=None):
    """
    Scrape interesting information from the given steps.

    :param steps: Iterable of steps to scrape.
    :type steps: Iterable of :class:`behave.model.Step`
    :param parent_node: Parent node that contained the step.
    :type parent_node: :class:`ruruki.entities.Vertex`
    """
    for step in steps:
        node = GRAPH.get_or_create_vertex(
            "STEP",
            name=step.name,
            keyword=step.keyword,
            step_type=step.step_type,
        )

        GRAPH.get_or_create_edge(
            node,
            "CITATION",
            (
                "FILE", {
                    "name": step.filename,
                }
            ),
            line=step.line,
        )

        if parent_node is not None:
            GRAPH.get_or_create_edge(
                parent_node,
                "HAS-STEP",
                node
            )


def scrape_background(background, parent_node=None):
    """
    Scrape interesting information from the given background.

    :param background: Backgrounds to scrape.
    :type background: :class:`behave.model.Background`
    :param parent_node: Parent node that contained the step.
    :type parent_node: :class:`ruruki.entities.Vertex`
    """
    node = GRAPH.get_or_create_vertex(
        "BACKGROUND",
        name=background.name,
        keyword=background.keyword,
    )

    GRAPH.get_or_create_edge(
        node,
        "CITATION",
        (
            "FILE", {
                "name": background.filename,
            }
        ),
        line=background.line,
    )

    if parent_node is not None:
        GRAPH.get_or_create_edge(
            parent_node,
            "HAS-STEP",
            node
        )

    scrape_steps(background.steps, node)


def scrape_scenarios(scenarios, parent_node=None):
    """
    Scrape interesting information from the given scenarios.

    :param features: Iterable of scenarios to scrape.
    :type features: Iterable of :class:`behave.model.Scenario`
    :param parent_node: Parent node that contained the scenario.
    :type parent_node: :class:`ruruki.entities.Vertex`
    """
    for scenario in scenarios:
        node = GRAPH.get_or_create_vertex(
            "SCENARIO",
            name=scenario.name,
            keyword=scenario.keyword,
        )

        GRAPH.get_or_create_edge(
            node,
            "CITATION",
            (
                "FILE", {
                    "name": scenario.filename,
                }
            ),
            line=scenario.line,
        )

        for tag in scenario.tags:
            GRAPH.get_or_create_edge(
                node,
                "HAS-TAG",
                ("TAG", {"name": tag})
            )

        if parent_node is not None:
            GRAPH.get_or_create_edge(
                parent_node,
                "HAS-SCENARIO",
                node
            )

        scrape_steps(scenario.steps, node)



def scrape_features(features):
    """
    Scrape interesting information from the given features.

    :param features: Iterable of features to scrape.
    :type features: Iterable of :class:`behave.model.Feature`
    """
    for feature in features:
        node = GRAPH.get_or_create_vertex(
            "FEATURE",
            name=feature.name,
            description=feature.description,
        )

        GRAPH.get_or_create_edge(
            node,
            "CITATION",
            (
                "FILE", {
                    "name": feature.filename,
                }
            ),
            line=feature.line,
        )

        scrape_scenarios(feature.walk_scenarios(), node)

        if feature.background is not None:
            scrape_background(feature.background, node)
