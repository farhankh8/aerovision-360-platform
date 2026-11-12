"""Default component registry for AEROVISION 360.

Provides the create_default_registry() function that registers all existing
curated dimensions and the three verified fact tables. FactBookingTransactions
and FactOperatingCosts are NOT registered because OD-04 (exchange-rate policy)
remains pending owner approval.
"""

from pathlib import Path


class _Component:
    """Internal helper class for default registry components.

    Avoids circular import with pipeline.py by not importing PipelineComponent
    at module level. The create_default_registry() function uses a lazy import.
    """

    def __init__(self, component_id, builder_script=None, depends_on=None):
        self.component_id = component_id
        self.builder_script = builder_script if builder_script else Path("")
        self.depends_on = depends_on if depends_on else []


def create_default_registry():
    """Create the default component registry for AEROVISION 360.

    Registers all existing curated dimensions and the three verified
    fact tables. FactBookingTransactions and FactOperatingCosts are
    NOT registered because OD-04 (exchange-rate policy) remains
    pending owner approval.

    Dependency model:
        Dimensions -> FactFlightOperations -> FactDisruptions,
        FactCustomerFeedback

    Returns:
        A list of _Component objects ready for registration.
    """
    from src.orchestration.pipeline import PipelineComponent

    base_builder = Path("scripts") / "build_curated.py"

    dims = [
        "dim_airport",
        "dim_aircraft_type",
        "dim_airline",
        "dim_booking_channel",
        "dim_currency",
        "dim_customer",
        "dim_date",
        "dim_disruption_type",
        "dim_fare_class",
        "dim_route",
        "dim_aircraft",
    ]

    facts = [
        "fact_flight_operations",
        "fact_disruptions",
        "fact_customer_feedback",
    ]

    components = []

    # Register dimensions (no dependencies)
    for dim_id in dims:
        components.append(
            PipelineComponent(
                component_id=dim_id,
                name=dim_id.replace("dim_", "").replace("_", " ").title(),
                builder_script=base_builder,
                depends_on=[],
            )
        )

    # Register facts with dependencies on dimensions
    # FactFlightOperations depends on dim_aircraft, dim_airline, dim_date
    components.append(
        PipelineComponent(
            component_id="fact_flight_operations",
            name="FactFlightOperations",
            builder_script=base_builder,
            depends_on=["dim_aircraft", "dim_airline", "dim_date"],
        )
    )

    # FactDisruptions depends on dim_disruption_type, dim_route, fact_flight_operations
    components.append(
        PipelineComponent(
            component_id="fact_disruptions",
            name="FactDisruptions",
            builder_script=base_builder,
            depends_on=["dim_disruption_type", "dim_route", "fact_flight_operations"],
        )
    )

    # FactCustomerFeedback depends on dim_customer, fact_flight_operations
    components.append(
        PipelineComponent(
            component_id="fact_customer_feedback",
            name="FactCustomerFeedback",
            builder_script=base_builder,
            depends_on=["dim_customer", "fact_flight_operations"],
        )
    )

    return components