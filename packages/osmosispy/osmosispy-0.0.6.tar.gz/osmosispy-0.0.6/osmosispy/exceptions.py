class OsmosisError(Exception):
    pass


class SimulationError(OsmosisError):
    pass


class TxError(OsmosisError):
    pass


class QueryError(OsmosisError):
    pass
